from typing import ClassVar, List
from jupyter_ai_magics import BaseProvider
from jupyter_ai_magics.providers import EnvAuthStrategy, Field, TextField, MultilineTextField
from jupyter_ydoc import YNotebook
from .llm import TabbyLLM
from .models import InlineCompletionRequest, InlineCompletionReply, InlineCompletionList

class TabbyProvider(BaseProvider, TabbyLLM):
    id: ClassVar[str] = "Tabby_Local"
    name: ClassVar[str] = "Tabby"
    models: ClassVar[List[str]] = ["Tabby"]
    help: ClassVar[str] = "Use Tabby for Python code completions"
    model_id_key: ClassVar[str] = "model_id"
    model_id_label: ClassVar[str] = "Model ID"
    pypi_package_deps: ClassVar[List[str]] = ["requests"]
    auth_strategy = EnvAuthStrategy(name="TABBY_API_KEY", keyword_param="api_key")
    registry: ClassVar[bool] = False
    fields: ClassVar[List[Field]] = [
        TextField(key="url", label="URL", required=True, format="text"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def _get_prefix_and_suffix(self, request: InlineCompletionRequest):
        prefix = request.prefix
        suffix = request.suffix.strip()
        
        server_ydoc = self.server_settings.get("jupyter_server_ydoc", None)
        if not server_ydoc:
            # fallback to prefix/suffix from single cell
            return prefix, suffix

        is_notebook = request.path.endswith("ipynb")
        document = await server_ydoc.get_document(
            path=request.path,
            content_type="notebook" if is_notebook else "file",
            file_format="json" if is_notebook else "text"
        )
        if not document or not isinstance(document, YNotebook):
            return prefix, suffix
        
        cell_type = "markdown" if request.language == "markdown" else "code"

        is_before_request_cell = True
        before = []
        after = [suffix]

        for cell in document.ycells:
            if is_before_request_cell and cell["id"] == request.cell_id:
                is_before_request_cell = False
                continue
            if cell["cell_type"] != cell_type:
                continue
            source = cell["source"].to_py()
            if is_before_request_cell:
                before.append(source)
            else:
                after.append(source)

        before.append(prefix)
        prefix = "\n\n".join(before)
        suffix = "\n\n".join(after)
        
        return prefix, suffix

    async def generate_inline_completions(self, request: InlineCompletionRequest):
        prefix, suffix = await self._get_prefix_and_suffix(request)
        response_text = self._call(prefix, suffix)
        return InlineCompletionReply(
            list=InlineCompletionList(items=[{"insertText": response_text}]),
            reply_to=request.number,
        )

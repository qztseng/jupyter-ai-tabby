from typing import Any, List, Optional
import json
import requests
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

class TabbyLLM(LLM):
    model_id: str
    url: str
    api_key: Optional[str] = None
    max_length: int

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prefix: str,
        suffix: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        url = self.url
        payload = json.dumps({
            "language": "python",
            "segments": {"prefix": prefix, "suffix": suffix}
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        else:
            return "Error: api key for tabby is not set!"
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "")
        else:
            return f"Error: {response.status_code}"

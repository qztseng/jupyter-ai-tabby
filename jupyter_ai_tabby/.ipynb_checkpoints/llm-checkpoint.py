from typing import Any, List, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM


class TabbyLLM(LLM):
    model_id: str
    tabby_url: str
    api_key: Optional[str] = None
    
    @property
    def _llm_type(self) -> str:
        return "tabby"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        url = f"{self.tabby_url}/v1/completions"
        payload = json.dumps({
            "language": "python",
            "segments": {"prefix": prompt, "suffix": ""}
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "")
        else:
            return f"Error: {response.status_code}, {response.text}"
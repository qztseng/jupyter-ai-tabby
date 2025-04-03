from pydantic import BaseModel

class InlineCompletionRequest(BaseModel):
    prefix: str
    suffix: str
    path: str
    language: str
    cell_id: str
    number: int

class InlineCompletionList(BaseModel):
    items: list

class InlineCompletionReply(BaseModel):
    list: InlineCompletionList
    reply_to: int

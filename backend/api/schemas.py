# Pydantic请求/响应模型
from pydantic import BaseModel
from typing import List,Optional

class Message(BaseModel):
    role:str #user或者 assistant
    content:str
class ChatRequest(BaseModel):
    message:str
    chat_history:Optional[List[Message]]= []
class ChatResponse(BaseModel):
    intent:str
    reply:str



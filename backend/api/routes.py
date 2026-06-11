# FastAPI路由定义
# backend/api/routes.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from backend.api.schemas import ChatRequest,ChatResponse
from backend.graph.workflow import build_workflow
import os

router = APIRouter()
workflow_app = build_workflow()

@router.post("/chat",response_model = ChatResponse)
def chat(request:ChatRequest):
    """核心接口:接受用户的消息,返回意图和恢复"""
    #将chat_history转为工作流需要的格式
    history = [
        {"role":m.role,"content":m.content} for m in request.chat_history
    ]
    result = workflow_app.invoke({
        "user_message":request.message,
        "chat_history":history,
        "intent":"",
        "final_response":None
    })

    return ChatResponse(
        intent=result["intent"],
        reply=result["final_response"]
    )

@router.get("/health")
def health():
    """健康检查接口"""
    return {"status":"ok"}

@router.get("/",response_class=HTMLResponse)
def serve_frontend():
    """返回聊天界面(避免静态文件挂载的各种坑)"""
    html_path = os.path.join(os.path.dirname(__file__),"..","frontend/src/pages","index.tsx")
    try:
        with open(html_path,"r",encoding="utf-8") as f:
            return  f.read()

    except FileNotFoundError:
        return HTMLResponse(content="<h1>页面未找到</h1>",status_code=404)

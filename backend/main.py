# FastAPI 入口
# backend/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.data.vector_store import init_vector_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    #启动时执行
    init_vector_store()
    yield
    #关闭时执行
app = FastAPI(
    title="Cross-Border E-Commerce AI Copilot",
    lifespan=lifespan
)

#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
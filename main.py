# # backend/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from backend.api.routes import router
# import os
#
# app = FastAPI(title="Cross-Border E-Commerce AI Copilot")
#
# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # 注册 API 路由
# app.include_router(router)
#
# # ⚠️ 静态文件挂载必须放在最后
# static_dir = os.path.join(os.path.dirname(__file__), "static")
# if os.path.isdir(static_dir):
#     app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
# else:
#     print(f"❌ 错误：静态文件目录不存在 -> {static_dir}")

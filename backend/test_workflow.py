from backend.graph.workflow import build_workflow

#编辑工作流
app = build_workflow()

test_messages=[
    "你们有运动短裤吗？",
    "帮我查一下订单ORD-20240501-001",
    "给客户张三发一封促销邮件",
    "今天天气怎么样",  # 兜底测试
]
print("🚀 多 Agent 工作流端到端测试\n")

for msg in test_messages:
    print(f"📤 用户: {msg}")
    # 初始状态
    result = app.invoke({
        "user_message": msg,
        "chat_history": [],
        "intent": "",
        "final_response": None
    })
    print(f"🧭 路由意图: {result['intent']}")
    print(f"📥 最终回复:\n{result['final_response']}\n")
    print("-" * 50)

print("✅ 工作流集成测试完成")
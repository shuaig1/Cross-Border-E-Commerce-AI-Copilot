from backend.agents.aftersale_agent import AftersaleAgent
from backend.test_router import test_cases

agent = AftersaleAgent()

test_cases =[
    "我的订单ORD-20240501-001到哪里了？",
    "帮我查一下物流单号LX20240501CN",
    "我收到的耳机有杂音，想退货",
    "我的订单ORD-999999还没收到"  # 不存在的订单号，测试兜底
]
print("📦 售后 Agent 测试\n")
for q in test_cases:
    print(f"📤 用户: {q}")
    reply = agent.invoke(q)
    print(f"📥 售后Agent: {reply}\n")
    print("-" * 50)

print("✅ 售后 Agent 测试完成")
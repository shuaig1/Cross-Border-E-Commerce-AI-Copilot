from backend.agents.marketing_agent import MarketingAgent


agent = MarketingAgent()

test_cases = [
     "帮我给客户张三生成一封促销邮件，他对健身器材感兴趣",
    "用户李四把跑鞋加入购物车但没付款，帮我写个召回文案",
    "给王五发一封通用优惠邮件"
 ]
print("📧 营销 Agent 测试\n")
for q in test_cases:
    print(f"📤 用户: {q}")
    reply = agent.invoke(q)
    print(f"📥 营销Agent:\n{reply}\n")
    print("-" * 50)

print("✅ 营销 Agent 测试完成")
from backend.agents.router_agent import RouterAgent

router = RouterAgent()

test_cases = [
    ("这个蓝牙耳机多少钱?","PRESALE"),
    ("我刚下的单什么时候发货?","AFTERSALE"),
    ("上次发我的优惠卷还能用吗?","MARKETING"),
    ("今天天气真不错","GENERAL"),
]
print("🕒路由 Agent 测试:")
for msg,expected in test_cases:
    result = router.route(msg)
    status = "✅" if result == expected else "❌"
    print(f"{status} 输入:{msg} -> 输出:{result}(预期:{expected})")
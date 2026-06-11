# from backend.tools.product_search_spider import search_products_online
from backend.tools.product_search_local import search_products_local
#直接调用工具函数传一个商品关键字进去
print("🔍 测试商品搜索工具：\n")

# 测试1：应该命中 Gymshark（关键词：运动）
print("📤 搜索: '运动短裤'")
result = search_products_local.invoke({"query": "运动短裤"})
print(f"📥 结果:\n{result}\n")

# 测试2：应该命中 Allbirds（关键词：跑鞋）
print("📤 搜索: '跑鞋'")
result = search_products_local.invoke({"query": "跑鞋"})
print(f"📥 结果:\n{result}\n")

# 测试3：默认命中 Fashion Nova（关键词不匹配任何特定店铺）
print("📤 搜索: '连衣裙'")
result = search_products_local.invoke({"query": "连衣裙"})
print(f"📥 结果:\n{result}\n")

print("✅ 工具函数测试完成")
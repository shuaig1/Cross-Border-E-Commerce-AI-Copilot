# 配置加载（环境变量、模型参数等）
import os
from dotenv import load_dotenv
#加载 .env 文件
load_dotenv()

class Config:
    """集中管理所有配置项目"""

    #DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL","https://api.deepseek.com")
    # 商品搜索目标店铺(完全抽离，按需要增减)
    TARGET_STORES ={
        "Gymshark": "https://www.gymshark.com/products.json",
        "Allbirds": "https://www.allbirds.com/products.json",
        "Kylie Cosmetics": "https://kyliecosmetics.com/products.json",  # 新增
        "Fashion Nova": "https://www.fashionnova.com/products.json",
    }
    # 商品搜索意图关键词映射（方便调整策略）
    STORE_KEYWORDS = {
        "Gymshark": ["gym", "健身", "运动", "瑜伽", "短裤", "背心"],
        "Allbirds": ["环保", "羊毛", "跑鞋", "拖鞋", "桉树"],
    }
    DEFAULT_STORE = "Fashion Nova"
    #后续可以扩展
    #SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
    #REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379")
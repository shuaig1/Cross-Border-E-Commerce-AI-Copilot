# 售前咨询Agent
from backend.agents.base_agent import BaseAgent
from langchain.tools import tool
from backend.tools.product_search_local import search_products_local_database,search_products_local_Json,search_products_local_vector_store

#1.定义一个模拟的产品查询工具(后续可替换为真实的数据库/API)
@tool
def lookup_product_info(query:str)->str:
    """查询商品信息，输入商品名称或关键字，返回商品详情"""
    # 模拟商品库
    mock_products = {
        "蓝牙耳机": "型号：EcoBuds Pro，价格：$49.99，蓝牙5.3，续航30小时，IPX5防水，库存充足。",
        "充电宝": "型号：PowerBoost 20000，价格：$29.99，20000mAh，支持快充，带LED显示屏。",
        "手机壳": "型号：FlexGuard，价格：$12.99，防摔硅胶，适配iPhone 15全系列，颜色：黑/蓝/红。",
        "数据线": "型号：TurboCharge Cable，价格：$9.99，USB-C to USB-C，1米，支持100W快充。",
    }
    for key, info in mock_products.items():
        if key in query:
            return info
    return f"未找到关于'{query}'的商品信息，建议引导用户查看全品类目录或联系人工客服。"

class PresaleAgent(BaseAgent):
    """售前咨询Agent，负责回答产品、价格、库存等问题"""
    def __init__(self):
        system_prompt="""
        你是一个友好的跨境电商售前客服专家。
        - 你可以使用提供的工具查询商品信息。
        - 如果用户询问商品，请调用工具获取详情，然后用自然、热情的语言回复。
        - 如果工具没有找到信息，请告诉用户你暂时无法解答，并建议对方提供更多细节或联系人工客服。
        - 回复中请包含商品的主要卖点和价格。
        - 始终使用用户提问的语言进行回复。
        """
        super().__init__(
            name="PresaleAgent",
            system_prompt=system_prompt,
            #绑定工具
            # search_products_local_database, search_products_local_Json,
            tools=[search_products_local_vector_store]
        )


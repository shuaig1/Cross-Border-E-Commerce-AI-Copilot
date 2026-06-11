# 邮件营销Agent
from backend.agents.base_agent import  BaseAgent
from backend.tools.marketing_tools import generate_promp_email,recall_abandoned_cart

class MarketingAgent(BaseAgent):
    """邮件营销客服Agent，负责生成促销邮件和弃购召回话术"""

    def __init__(self):
        system_prompt = """你是一名跨境电商营销专家。你的任务是帮助运营人员撰写营销文案。
    1. 当用户要求“给某人发一封促销邮件”或类似请求时，调用 generate_promp_email 工具生成邮件。
    2. 当用户提到“召回”、“弃购”、“加购未付”等关键词时，调用 recall_abandoned_cart 工具生成召回文案。
    3. 将工具返回的内容直接呈现给用户，可以添加简短的说明，但不要修改文案核心。
    4. 语气应专业、亲切，始终使用用户提问的语言回复。
    """
        super().__init__(
            name="MarketingAgent",
            system_prompt=system_prompt,
            tools=[generate_promp_email, recall_abandoned_cart]
        )
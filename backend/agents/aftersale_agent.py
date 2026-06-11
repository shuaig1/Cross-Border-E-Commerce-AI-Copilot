# 售后处理Agent
from backend.agents.base_agent import BaseAgent
from backend.tools.order_tracking_json import lookup_order,lookup_logistics

class AftersaleAgent(BaseAgent):
    """售后客服Agent，处理订单查询、物流追踪、退换货等"""
    def __init__(self):
        system_prompt = """你是一名专业的跨境电商售后客服专员。请遵循以下规则：
        1. 如果用户询问订单状态，使用 lookup_order 工具查询，并将信息整理成自然语言回复。
        2. 如果用户想知道物流详情，使用 lookup_logistics 工具查询，并告知最新动态。
        3. 如果用户要求退换货，询问订单号并记录原因，告知后续流程（会产生退货标签等，因为是模拟，可以说“已将您的请求提交，稍后会有客服邮件联系”）。
        4. 对任何投诉或不满，先道歉再解决问题。
        5. 始终用用户使用的语言回复，语气专业且有同理心。
        """
        super().__init__(
            name="AftersaleAgent",
            system_prompt=system_prompt,
            tools=[lookup_order, lookup_logistics]
        )

# 路由Agent，意图识别与分发
from backend.agents.base_agent import BaseAgent
from backend.test_agent import response


class RouterAgent(BaseAgent):
    """意图识别与任务分发Agent"""
    def __init__(self):
        system_prompt="""
        你是一个跨境电商独立站的智能路由专家。
        请分析用户发送的消息，并严格只输出一下四个英文标签之一:
        
        - PRESALE:用户询问商品信息、价格、库存、参数、优惠活动等售前问题
        - AFTERSALE:用户询问订单状态、物流进度、退换货、退款、投诉等售后问题
        - MARKETING:用户对促销邮件、折扣码、推荐商品、弃购召回等营销内容有响应或询问
        - GENERAL:无法归类到以上三类的闲聊或一般性问题
        
        输出规则:
        - 只回复一个单词，不加标点，不加解释
        - 如果一句话里同时涉及售前和售后，优先判断为AFTERSALE
        """
        #路由不需要工具只做文本判断
        super().__init__(name="RouterAgent",system_prompt=system_prompt,tools=[])

    def route(self,user_message:str)->str:
        """识别用户意图，返回标准化的标签"""
        response = self.invoke(user_message)
        #清洗并标准化，去除可能的多余符号和空白
        label = response.strip().upper()
        #兜底保护:如果模型不听话，强行归类为GENERAL
        valid_label = {"PRESALE","AFTERSALE","MARKETING","GENERAL"}
        if label not in valid_label:
            label = "GENERAL"
        return label



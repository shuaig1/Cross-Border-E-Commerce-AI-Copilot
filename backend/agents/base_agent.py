"""
# Agent基类，封装通用逻辑
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
# from langgraph.prebuilt import create_react_agent
from  typing import List,Optional
from backend.config import Config

class BaseAgent:
    """
    所有Agent的基类，封装LLM与工具的绑定逻辑
    """
    def __init__(
            self,
            name:str,
            system_prompt:str,
            tools:Optional[List]=None,
            model_name:str="deepseek-chat"
    ):
        self.name =name
        self.system_prompt = system_prompt
        #使用DeepSeek兼容OpenAI接口
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=Config.DEEPSEEK_API_KEY,
            base_url=Config.DEEPSEEK_BASE_URL,
            temperature=0.3,
        )
        self.tools = tools or []
        self.agent = create_agent(
            model= self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )

    def invoke(self,user_message:str,chat_history:Optional[List]=None)->str:
        """
        调用Agent
        """
        #1.准备消息列表
        messages = []
        #2.如果有历史对话，先放进去
        if chat_history:
            messages.extend(chat_history)
        #3.最后放入当前用户信息
        messages.append({"role":"user","content":user_message})
        #4.调用Agent，传入消息
        result =self.agent.invoke({"messages":messages})
        #5.从结果中取出最后一条信息（AI的回复）
        last_msg = result["messages"][-1]
        return last_msg.content
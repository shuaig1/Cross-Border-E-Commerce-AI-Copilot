from openai.types.responses import response_input

from backend.agents.base_agent import BaseAgent
from backend.config import Config

#1.验证配置
print("🔑正在检查配置...")
print(f"    Base URL:{Config.DEEPSEEK_BASE_URL}")
print(f"    API Key:{Config.DEEPSEEK_API_KEY[:12]}...{Config.DEEPSEEK_API_KEY[-4:]}")
#2.创建一个测试Agent(暂不绑定工具)
agent = BaseAgent(
    name="测试",
    system_prompt="你是一个助手，请回答用户问题",
    model_name="deepseek-chat",
    tools = []
)
#3.发送一条消息
print("\n📤发送消息:你好，请用一句话介绍你自己")
response = agent.invoke("你好，请用一句话介绍你自己")
print(f"\n📥Agent 回复:\n{response}")
print("\n✔ 基础链路验证通过")
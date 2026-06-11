# LangGraph 状态图编排逻辑
from typing import TypedDict,List,Optional
from langgraph.graph import StateGraph,END
from backend.agents.router_agent import RouterAgent
from backend.agents.presale_agent import PresaleAgent
from backend.agents.aftersale_agent import AftersaleAgent
from backend.agents.marketing_agent import MarketingAgent

class AgentState(TypedDict):
    # 用户最新消息
    user_message:str
    # 对话历史
    chat_history:List[dict]
    # 路由结果:PRESALE/AFTERSALE/MARKETING/GENERAL
    intent:str
    #最终回复
    final_response:Optional[str]
#初始化四个Agent(全局单例)
router = RouterAgent()
presale = PresaleAgent()
aftersale = AftersaleAgent()
marketing = MarketingAgent()
#节点1
def route_node(state:AgentState)->AgentState:
    intent =router.route(state["user_message"])
    state["intent"]= intent
    return state

#节点2-4：专业Agent处理节点
def presale_node(state:AgentState)->AgentState:
    response = presale.invoke(
        state["user_message"],
        chat_history = state.get("chat_history")
        )
    state["final_response"] =response
    return state
def aftersale_node(state:AgentState)->AgentState:
    response = aftersale.invoke(
        state["user_message"],
        chat_history = state.get("chat_history")
        )
    state["final_response"] =response
    return state
def marketing_node(state:AgentState)->AgentState:
    response = marketing.invoke(
        state["user_message"],
        chat_history = state.get("chat_history")
        )
    state["final_response"] =response
    return state
def general_node(state:AgentState)->AgentState:
    #兜底:通用回复
    state["final_response"] ="感谢您的咨询!我是您的AI助理，请问有什么可以帮您？"
    return state

#路由决策:根据intent 选择下一个节点
def decide_next_node(state:AgentState)->str:
    intent = state.get("intent","GENERAL")
    if intent == "PRESALE":
        return "presale"
    elif intent == "AFTERSALE":
        return "aftersale"
    elif intent == "MARKETING":
        return "marketing"
    else:
        return "general"

#构建状态图
def build_workflow()->StateGraph:
    workflow = StateGraph(AgentState)
    #添加节点
    workflow.add_node("router",route_node)
    workflow.add_node("presale",presale_node)
    workflow.add_node("aftersale",aftersale_node)
    workflow.add_node("marketing",marketing_node)
    workflow.add_node("general",general_node)
    #设置入口
    workflow.set_entry_point("router")
    #条件边:根据路由结果分发
    workflow.add_conditional_edges(
        "router",
        decide_next_node,
    {
        "presale":"presale",
        "aftersale":"aftersale",
        "marketing":"marketing",
        "general":"general",
        }
    )
    #所有专业节点处理完后直接结束
    workflow.add_edge("presale",END)
    workflow.add_edge("aftersale",END)
    workflow.add_edge("marketing",END)
    workflow.add_edge("general",END)
    return workflow.compile()




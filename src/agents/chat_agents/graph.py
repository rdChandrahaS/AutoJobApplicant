from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver 
from langgraph.prebuilt import ToolNode, tools_condition
from src.agents.chat_agents.states.chat_agent_state import ChatAgentState
from src.tools.custom_tools import get_current_time
from src.agents.chat_agents.nodes.general_chat import general_chat_node
from src.agents.chat_agents.nodes.summarizer import summarize_resume_node
# Clean Import
from src.agents.chat_agents.nodes.application_flow import ask_platform_node, ask_credentials_node, run_automation_node

def router(state: ChatAgentState):
    if not state.get("messages"): return "general_chat"
    msg = state["messages"][-1]
    if hasattr(msg, "content"):
        text = msg.content.lower()
        if "apply" in text or "job" in text:
            return "summarize_resume"
    return "general_chat"

workflow = StateGraph(ChatAgentState)
workflow.add_node("general_chat", general_chat_node)
workflow.add_node("tools", ToolNode([get_current_time]))
workflow.add_node("summarize_resume", summarize_resume_node)
workflow.add_node("ask_platform", ask_platform_node)
workflow.add_node("ask_credentials", ask_credentials_node)
workflow.add_node("run_automation", run_automation_node)

workflow.add_conditional_edges(START, router)
workflow.add_conditional_edges("general_chat", tools_condition)
workflow.add_edge("tools", "general_chat")
workflow.add_edge("summarize_resume", "ask_platform")
workflow.add_edge("ask_platform", "ask_credentials")
workflow.add_edge("ask_credentials", "run_automation")
workflow.add_edge("run_automation", END)

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
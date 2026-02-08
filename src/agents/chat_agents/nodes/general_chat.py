from langchain_core.messages import SystemMessage, AIMessage
from src.agents.chat_agents.states.chat_agent_state import ChatAgentState
from src.tools.custom_tools import get_current_time
from src.services.container import ServiceContainer 

def general_chat_node(state: ChatAgentState, config):
    # 1. Get the Model from Container (We don't know if it's Gemini or OpenAI, and we don't care!)
    llm = ServiceContainer.get_llm() 
    
    tools = [get_current_time]
    resume_context = state.get("resume_text", "No resume uploaded yet.")
    system_instruction = f"""
    You are a helpful career assistant named 'AutoJob Bot'.
    CONTEXT FROM USER RESUME:
    {resume_context}
    INSTRUCTIONS:
    - If asked for time, call 'get_current_time'.
    - If asked about name/skills, use RESUME CONTEXT.
    """
    messages = [SystemMessage(content=system_instruction)] + state["messages"]
    
    try:
        # Bind tools via the interface
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(messages, config=config)
        return {"messages": [response]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"⚠️ System Error: {str(e)}")]}
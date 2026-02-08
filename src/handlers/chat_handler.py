from langchain_core.messages import HumanMessage
from langgraph.types import Command
from src.agents.chat_agents.graph import graph
from src.services.container import ServiceContainer

class ChatHandler:
    @staticmethod
    def _extract_text(message):
        """Helper to extract clean text from AI message."""
        content = message.content
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # Handle list of blocks (e.g. [{'text': 'Hello'}, ...])
            return "".join([block.get("text", "") for block in content if isinstance(block, dict) and "text" in block])
        return str(content)

    @staticmethod
    def process_chat(session_id: str, user_input: str, resume_text: str = ""):
        db = ServiceContainer.get_database()
        config = {"configurable": {"thread_id": session_id}}
        
        snapshot = graph.get_state(config)
        
        if snapshot.next:
            print(f"--- 🔄 Resuming Session {session_id} ---")
            payload = Command(resume=user_input)
        else:
            print(f"--- 💬 New Message for {session_id} ---")
            db.add_user_message(session_id, user_input)
            
            payload = {
                "messages": [HumanMessage(content=user_input)],
                "resume_text": resume_text
            }

        final_state = graph.invoke(payload, config)
        
        if final_state and "messages" in final_state:
            last_message = final_state["messages"][-1]
            
            # FIX: Use helper to extract clean text
            response_text = ChatHandler._extract_text(last_message)
            
            db.add_ai_message(session_id, response_text)
            return response_text
            
        return "⚠️ No response generated."
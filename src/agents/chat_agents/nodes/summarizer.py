from langchain_core.prompts import ChatPromptTemplate
from langgraph.types import interrupt
from src.agents.chat_agents.states.chat_agent_state import ChatAgentState
from src.services.container import ServiceContainer

def summarize_resume_node(state: ChatAgentState, config):
    print("--- Generating Summary via RAG ---")
    
    # 1. Retrieve via Container
    try:
        vector_store = ServiceContainer.get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        
        # Invoke retrieval
        docs = retriever.invoke("professional summary, key technical skills, and experience")
        context_text = "\n\n".join([d.page_content for d in docs])
    except Exception as e:
        print(f"⚠️ RAG Error: {e}")
        context_text = state.get("resume_text", "")

    # 2. Get LLM via Container
    llm_provider = ServiceContainer.get_llm()
    
    prompt = ChatPromptTemplate.from_template("""
    You are an expert career assistant. Based ONLY on the following resume context, 
    create a professional summary and list the top 5 skills.
    
    Context:
    {context}
    
    Output Format:
    Summary: [Your summary here]
    Top Skills: [Skill 1, Skill 2, ...]
    """)

    try:
        # FIX: We cannot use pipe (|) because llm_provider is a wrapper class.
        # Instead, we invoke the prompt to get messages, then pass them to the LLM.
        
        # 1. Generate formatted messages
        messages = prompt.invoke({"context": context_text})
        
        # 2. Send to LLM
        response = llm_provider.invoke(messages, config=config)
        
        summary = response.content
        
        interrupt({
            "question": "I've extracted this profile from your resume. Is it accurate?",
            "data": summary
        })
        return {"summary": summary}

    except Exception as e:
        return {"summary": f"⚠️ Error generating summary: {str(e)}"}
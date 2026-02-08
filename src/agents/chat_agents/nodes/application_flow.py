from langgraph.types import interrupt
from langchain_core.messages import SystemMessage, HumanMessage
from src.agents.chat_agents.states.chat_agent_state import ChatAgentState
from src.services.container import ServiceContainer # <--- Dependency Injection
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def ask_platform_node(state: ChatAgentState):
    # Ask Container for LLM
    llm = ServiceContainer.get_llm()
    
    last_msg = state["messages"][-1].content
    resume_summary = state.get("summary", "")
    
    extraction_prompt = f"""
    User Request: "{last_msg}"
    User Resume Summary: "{resume_summary}"
    Extract: Platform (Default Unstop) and Query.
    Return Format: Platform: [P] | Query: [Q]
    """
    try:
        # Using abstract .invoke method
        response = llm.invoke([HumanMessage(content=extraction_prompt)]).content
        if "Platform:" in response:
            parts = response.split("|")
            platform = parts[0].replace("Platform:", "").strip().lower()
            query = parts[1].replace("Query:", "").strip()
        else:
            platform = "unstop"; query = "Software Engineer"
    except: platform = "unstop"; query = "Software Engineer"

    return {"messages": [SystemMessage(content=f"Applying for '{query}' on {platform}...")], "platform": platform, "job_query": query}

def ask_credentials_node(state: ChatAgentState):
    platform = state.get("platform", "Unstop")
    credentials = interrupt({"question": f"Login for {platform}", "type": "fields", "fields": ["username", "password"]})
    return {"messages": [SystemMessage(content="Credentials received.")], "credentials": credentials}

def run_automation_node(state: ChatAgentState):
    platform = state.get("platform", "unstop")
    query = state.get("job_query", "")
    username = state["credentials"]["username"]
    password = state["credentials"]["password"]
    messages = []

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Ask Container for the correct Scraper Provider
        scraper = ServiceContainer.get_scraper(platform, driver)
        
        success, msg = scraper.login(username, password)
        messages.append(msg)
        if success:
            success, msg = scraper.search_jobs(query)
            messages.append(msg)
    except Exception as e:
        messages.append(f"❌ Error: {str(e)}")
        try: driver.quit()
        except: pass

    return {"messages": messages}
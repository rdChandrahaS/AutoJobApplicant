import streamlit as st
import uuid
from pypdf import PdfReader
from langchain_core.messages import HumanMessage
from langgraph.types import Command 
from langchain_core.callbacks import BaseCallbackHandler
from src.agents.chat_agents.graph import graph
from src.services.container import ServiceContainer
from src.services.rag.ingestion import ingest_resume_text

# --- HELPER ---
def extract_clean_content(msg):
    """Helper to extract text if content is a list of objects."""
    if hasattr(msg, "content"):
        content = msg.content
    else:
        content = msg
        
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return "".join([c.get("text", "") for c in content if isinstance(c, dict) and "text" in c])
    return str(content)

# --- SETUP DI ---
db = ServiceContainer.get_database()

st.set_page_config(page_title="AutoJob Bot", layout="wide")

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = str(uuid.uuid4())
    st.session_state.is_new_chat = True
    st.session_state.resume_required = False 

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

with st.sidebar:
    st.title("🗂️ Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_session_id = str(uuid.uuid4())
        st.session_state.is_new_chat = True
        st.session_state.resume_required = False
        st.session_state.messages = []
        st.rerun()

    st.divider()
    
    sessions = db.get_all_sessions()
    session_options = {s["title"]: s["id"] for s in sessions}
    
    current_index = 0
    if not st.session_state.get("is_new_chat", False):
         ids = [s["id"] for s in sessions]
         if st.session_state.current_session_id in ids:
             current_index = ids.index(st.session_state.current_session_id)

    if sessions:
        selected_title = st.radio("Recent Conversations:", options=list(session_options.keys()), index=current_index, key="session_radio")
        selected_id = session_options[selected_title]
        if selected_id != st.session_state.current_session_id:
            st.session_state.current_session_id = selected_id
            st.session_state.is_new_chat = False
            st.session_state.resume_required = False
            st.rerun()
            
        if st.button("🗑️ Delete Selected Chat", type="primary"):
            db.delete_session(st.session_state.current_session_id)
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.is_new_chat = True
            st.session_state.resume_required = False
            st.rerun()
    else:
        st.info("No saved chats yet.")

    st.divider()
    
    st.header("📄 Documents")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    if uploaded_file:
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
            reader = PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in reader.pages])
            st.session_state.resume_text = text 
            st.session_state.last_uploaded = uploaded_file.name
            ingest_resume_text(text)
            st.success("Resume Analyzed!")

# Load History
history = db.get_history(st.session_state.current_session_id)
current_messages = history.messages

# Sync DB history to Session State on load (prevents losing history on refresh)
if not st.session_state.get("is_new_chat", False):
    st.session_state.messages = current_messages
elif "messages" not in st.session_state:
    st.session_state.messages = []

display_title = "New Conversation"
if not st.session_state.is_new_chat and sessions:
    for s in sessions:
        if s["id"] == st.session_state.current_session_id:
            display_title = s["title"]
            break
st.header(f"💬 {display_title}")

# Display Chat
for msg in st.session_state.messages:
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        st.write(extract_clean_content(msg))

if user_input := st.chat_input("Type here..."):
    if st.session_state.is_new_chat:
        db.save_session_title(st.session_state.current_session_id, user_input)
        st.session_state.is_new_chat = False

    # Add to DB and Local State immediately
    history.add_user_message(user_input)
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        stream_handler = StreamHandler(response_placeholder)
        
        config = {
            "configurable": {"thread_id": st.session_state.current_session_id},
            "callbacks": [stream_handler]
        }
        
        if st.session_state.resume_required:
            payload = Command(resume=user_input)
            st.session_state.resume_required = False 
        else:
            payload = {
                "messages": st.session_state.messages,
                "resume_text": st.session_state.resume_text 
            }

        for event in graph.stream(payload, config):
            if "__interrupt__" in event:
                data = event["__interrupt__"][0].value
                question = data.get("question")
                int_type = data.get("type")
                
                if int_type == "upload_request":
                    response_placeholder.write(f"📂 **{question}**")
                    response_placeholder.info("Please upload PDF in sidebar.")
                    st.session_state.resume_required = True 
                elif "fields" in data:
                    response_placeholder.write(f"🔐 **{question}**")
                    with st.form("credentials_form"):
                        username = st.text_input("Username/Email")
                        password = st.text_input("Password", type="password")
                        submitted = st.form_submit_button("Submit Credentials")
                        
                        if submitted:
                            graph.invoke(Command(resume={"username": username, "password": password}), config)
                            st.rerun()
                    st.stop()
                else:
                    response_placeholder.write(f"**Action Required:** {question}")
                    st.session_state.resume_required = True 
                break 
            
            for node_name, node_output in event.items():
                if isinstance(node_output, dict) and "messages" in node_output:
                    msg = node_output["messages"][0]
                    clean_text = extract_clean_content(msg)
                    # Only add to DB here. The StreamHandler has already displayed it.
                    history.add_ai_message(clean_text)
                elif isinstance(node_output, dict) and "summary" in node_output:
                     msg = node_output["summary"]
                     response_placeholder.markdown(msg) 
                     history.add_ai_message(msg)
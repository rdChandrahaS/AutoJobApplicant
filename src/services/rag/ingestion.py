from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.services.container import ServiceContainer # <--- Dependency Injection

def ingest_resume_text(text: str):
    """
    Splits the resume text into chunks and saves them via the Vector Provider.
    """
    # 1. Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    # 2. Convert to Documents
    docs = [Document(page_content=chunk) for chunk in chunks]
    
    # 3. Store via Container (No hard imports!)
    vector_store = ServiceContainer.get_vector_store()
    vector_store.add_documents(docs)
    
    print(f"✅ Ingested {len(docs)} chunks into Vector DB.")
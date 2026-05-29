import streamlit as st
import chromadb
from chromadb.config import Settings
import os
from pathlib import Path
import json
from datetime import datetime
import requests

# Page configuration
st.set_page_config(
    page_title="Setup & Configuration Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize ChromaDB
@st.cache_resource
def init_chromadb():
    db_path = Path("./chatbot_data")
    db_path.mkdir(exist_ok=True)
    
    client = chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(db_path),
            anonymized_telemetry=False
        )
    )
    return client

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "knowledge_loaded" not in st.session_state:
    st.session_state.knowledge_loaded = False
if "client" not in st.session_state:
    st.session_state.client = init_chromadb()

# Function to load knowledge from conw.txt
def load_knowledge_base():
    conw_path = Path("conw.txt")
    
    if not conw_path.exists():
        st.warning("File conw.txt không tìm thấy")
        return False
    
    # Read the content
    with open(conw_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create or get collection
    try:
        collection = st.session_state.client.delete_collection(name="setup_guide")
    except:
        pass
    
    collection = st.session_state.client.get_or_create_collection(
        name="setup_guide",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Split content into chunks
    chunks = split_text(content)
    
    # Add documents
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            metadatas=[{"source": "conw.txt", "chunk_index": i}]
        )
    
    st.session_state.knowledge_loaded = True
    return True

def split_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks"""
    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            # Keep last few words for overlap
            current_chunk = current_chunk[-int(overlap/5):]
            current_length = sum(len(w) + 1 for w in current_chunk)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def retrieve_context(query, top_k=3):
    """Retrieve relevant documents from ChromaDB"""
    try:
        collection = st.session_state.client.get_collection(name="setup_guide")
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if results and results['documents'] and len(results['documents']) > 0:
            return "\n\n".join(results['documents'][0])
        return None
    except Exception as e:
        st.error(f"Lỗi khi retrieve: {e}")
        return None

def generate_response(query, context):
    """Generate response using retrieved context (simple template-based approach)"""
    # Try to use OpenAI API if available
    api_key = st.secrets.get("openai_api_key", None)
    
    if api_key:
        return generate_with_openai(query, context, api_key)
    else:
        return generate_with_template(query, context)

def generate_with_openai(query, context, api_key):
    """Generate response using OpenAI API"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """Bạn là một trợ lý hữu ích chuyên về setup, configuration và installation. 
        Dựa vào context được cung cấp, hãy trả lời câu hỏi của user một cách chính xác và chi tiết.
        Nếu thông tin không có trong context, hãy nói rõ điều đó."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nCâu hỏi: {query}"}
        ]
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return generate_with_template(query, context)
    except:
        return generate_with_template(query, context)

def generate_with_template(query, context):
    """Generate response using simple template-based approach"""
    if not context:
        return """😕 Xin lỗi, tôi không tìm thấy thông tin liên quan trong knowledge base.
        
Câu hỏi của bạn: "{}"

Vui lòng thử:
- Rephrase câu hỏi
- Hỏi về các topic liên quan đến Google Cloud Setup, Vertex AI, Gemini
- Hoặc reload knowledge base""".format(query)
    
    return f"""📚 **Dựa trên knowledge base:**

{context}

---

**Trả lời cho câu hỏi của bạn:**
Các hướng dẫn trên bao gồm các bước chi tiết để setup Google Cloud, enable Vertex AI API, và test Gemini connection.

Nếu bạn cần thêm chi tiết, vui lòng hỏi cụ thể hơn về bước nào!"""

# Sidebar
with st.sidebar:
    st.markdown('<div class="main-header">⚙️ Setup & Config</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box"><b>📌 Chức năng:</b><br>Chatbot hỗ trợ setup Google Cloud + Vertex AI Gemini</div>', unsafe_allow_html=True)
    
    # Load knowledge base
    if st.button("🔄 Load Knowledge Base", use_container_width=True):
        with st.spinner("Loading..."):
            if load_knowledge_base():
                st.success("✅ Knowledge base loaded!")
            else:
                st.error("❌ Failed to load knowledge base")
    
    if st.session_state.knowledge_loaded:
        st.info("✓ Knowledge base ready")
    else:
        st.warning("⚠️ Please load knowledge base first")
    
    st.divider()
    
    # Settings
    st.markdown("### ⚙️ Settings")
    api_choice = st.radio(
        "LLM Source:",
        ["Local", "OpenAI (if configured)"],
        help="Local: sử dụng template. OpenAI: cần API key"
    )
    
    top_k = st.slider("Retrieve docs:", 1, 5, 3)
    
    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit + ChromaDB")

# Main chat interface
st.markdown('<div class="main-header">💬 Setup & Configuration Assistant</div>', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Hỏi gì đó về setup Google Cloud, Vertex AI, hoặc Gemini..."):
    # Check if knowledge is loaded
    if not st.session_state.knowledge_loaded:
        st.error("❌ Vui lòng load knowledge base trước (bấm nút ở sidebar)")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieve context
            context = retrieve_context(prompt, top_k=top_k)
            
            # Generate response
            response = generate_response(prompt, context)
            
            st.markdown(response)
            
            # Add to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Show source documents
            with st.expander("📄 Source Documents"):
                if context:
                    st.text_area(
                        "Retrieved context:",
                        value=context[:500] + "..." if len(context) > 500 else context,
                        height=150,
                        disabled=True
                    )

# Help section
st.divider()
st.markdown("""
## 📚 Hướng dẫn sử dụng

1. **Load Knowledge Base**: Bấm nút "Load Knowledge Base" ở sidebar để load dữ liệu từ `conw.txt`
2. **Đặt câu hỏi**: Nhập câu hỏi về setup Google Cloud, Vertex AI, hoặc Gemini
3. **Xem kết quả**: Chatbot sẽ retrieve relevant documents và trả lời câu hỏi

## 🚀 Ví dụ câu hỏi:
- "Làm sao để setup Google Cloud CLI?"
- "Vertex AI API cần enable những gì?"
- "Các library Python cần cài gì?"
- "Làm sao để test Gemini connection?"
""")

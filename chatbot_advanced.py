"""
Alternative Chatbot Version with more features
- Conversation memory
- Export chat history
- Knowledge base management
"""

import streamlit as st
import chromadb
from chromadb.config import Settings
import os
from pathlib import Path
import json
from datetime import datetime
import requests
import csv

# Page configuration
st.set_page_config(
    page_title="Advanced Chatbot - RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme
st.markdown("""
    <style>
    .main {
        max-width: 1000px;
        margin: 0 auto;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #1f77b4;
    }
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .info-card {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .stats-box {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 5px;
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
if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0

# Load knowledge from conw.txt
def load_knowledge_base():
    conw_path = Path("conw.txt")
    
    if not conw_path.exists():
        st.error("❌ File conw.txt not found!")
        return False
    
    try:
        with open(conw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clear old collection
        try:
            st.session_state.client.delete_collection(name="setup_guide")
        except:
            pass
        
        # Create new collection
        collection = st.session_state.client.get_or_create_collection(
            name="setup_guide",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Split and add documents
        chunks = split_text(content)
        
        for i, chunk in enumerate(chunks):
            collection.add(
                ids=[f"chunk_{i}"],
                documents=[chunk],
                metadatas=[{
                    "source": "conw.txt",
                    "chunk_index": i,
                    "timestamp": datetime.now().isoformat()
                }]
            )
        
        st.session_state.knowledge_loaded = True
        st.session_state.doc_count = len(chunks)
        return True
    except Exception as e:
        st.error(f"❌ Error loading knowledge base: {str(e)}")
        return False

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
            docs = results['documents'][0]
            metadata = results['metadatas'][0] if results['metadatas'] else []
            distances = results['distances'][0] if results['distances'] else []
            
            return {
                'documents': docs,
                'metadata': metadata,
                'distances': distances,
                'similarity_scores': [1 - d for d in distances]  # Convert distance to similarity
            }
        return None
    except Exception as e:
        st.error(f"Error retrieving: {e}")
        return None

def generate_response(query, context):
    """Generate response"""
    api_key = st.secrets.get("openai_api_key", None)
    
    if api_key:
        return generate_with_openai(query, context, api_key)
    else:
        return generate_with_template(query, context)

def generate_with_openai(query, context, api_key):
    """Generate with OpenAI"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        context_text = "\n\n".join(context['documents']) if context else ""
        
        system_prompt = """Bạn là trợ lý chuyên về setup Google Cloud và Vertex AI.
        Trả lời dựa vào context được cung cấp. Nếu không có thông tin, hãy nói rõ."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return generate_with_template(query, context)
    except:
        return generate_with_template(query, context)

def generate_with_template(query, context):
    """Generate with template"""
    if not context:
        return """😕 Xin lỗi, không tìm thấy thông tin liên quan trong knowledge base.
        
Hãy thử:
- Rephrase câu hỏi
- Hỏi cụ thể hơn
- Reload knowledge base"""
    
    similarity = context['similarity_scores'][0] if context['similarity_scores'] else 0
    
    response = f"""📚 **Dựa trên knowledge base:**\n\n"""
    response += f"{context['documents'][0][:300]}...\n\n"
    
    if similarity < 0.5:
        response += "⚠️ **(Liên quan thấp - kiểm tra lại câu hỏi)**"
    
    return response

def export_chat_history(format_type="json"):
    """Export chat history"""
    if not st.session_state.messages:
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "json":
        filename = f"chat_history_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
    elif format_type == "csv":
        filename = f"chat_history_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Role', 'Message', 'Timestamp'])
            for msg in st.session_state.messages:
                writer.writerow([msg['role'], msg['content'], msg.get('timestamp', '')])
    
    return filename

# Header
st.markdown('<div class="header-title"><h1>🤖 Advanced RAG Chatbot</h1></div>', unsafe_allow_html=True)

# Main layout: Sidebar + Chat
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### ⚙️ Control Panel")
    
    # Knowledge base section
    st.markdown('<div class="info-card"><b>📚 Knowledge Base</b></div>', unsafe_allow_html=True)
    
    if st.button("🔄 Load KB", use_container_width=True):
        with st.spinner("Loading..."):
            if load_knowledge_base():
                st.success(f"✅ Loaded {st.session_state.doc_count} chunks!")
            else:
                st.error("Failed!")
    
    if st.session_state.knowledge_loaded:
        st.metric("Documents", st.session_state.doc_count)
    else:
        st.warning("⚠️ Load KB first!")
    
    st.divider()
    
    # Settings
    st.markdown('<div class="info-card"><b>🎛️ Settings</b></div>', unsafe_allow_html=True)
    
    top_k = st.slider("Retrieve", 1, 5, 3, help="Number of documents to retrieve")
    model_choice = st.selectbox(
        "Model",
        ["Local", "OpenAI (if key set)"],
        help="LLM source"
    )
    
    st.divider()
    
    # Chat management
    st.markdown('<div class="info-card"><b>💾 Chat</b></div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col_b:
        export_format = st.selectbox("Export", ["JSON", "CSV"])
        if st.button("💾 Export", use_container_width=True):
            filename = export_chat_history(export_format.lower())
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    st.download_button(
                        "📥 Download",
                        f.read(),
                        filename,
                        use_container_width=True
                    )
    
    # Stats
    st.divider()
    st.markdown("### 📊 Stats")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Chunks", st.session_state.doc_count)

with col2:
    st.markdown("### 💬 Chat")
    
    # Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about Google Cloud setup..."):
        if not st.session_state.knowledge_loaded:
            st.error("❌ Please load knowledge base first!")
            st.stop()
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context = retrieve_context(prompt, top_k=top_k)
                response = generate_response(prompt, context)
                st.markdown(response)
                
                # Show sources
                if context:
                    with st.expander("📄 Sources"):
                        for i, doc in enumerate(context['documents']):
                            similarity = context['similarity_scores'][i] if i < len(context['similarity_scores']) else 0
                            st.text(f"Similarity: {similarity:.2%}")
                            st.text_area(f"Doc {i+1}", doc[:400], height=100, disabled=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })

# Footer
st.divider()
st.markdown("""
---
**Features:**
- 🔍 RAG with ChromaDB
- 💾 Chat history export
- 📊 Document statistics
- 🔗 OpenAI integration (optional)

**Tips:**
- Load KB first
- Ask specific questions
- Check source documents
- Adjust retrieve count for better results
""")

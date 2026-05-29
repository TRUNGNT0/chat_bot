# 🎯 RAG Optimization Guide

Hướng dẫn tối ưu hóa Retrieval-Augmented Generation (RAG) để chatbot trả lời tốt hơn.

---

## 📋 Cơ bản về RAG

```
User Query
    ↓
[Vector Embedding] ← Sentence Transformers
    ↓
[Similarity Search] ← ChromaDB FAISS
    ↓
[Top-K Documents] ← Retrieved context
    ↓
[LLM Generation] ← OpenAI / Template
    ↓
Answer
```

---

## 🔍 1. Retrieval Optimization

### A. Điều chỉnh `top_k` (số documents lấy ra)

**Trong sidebar:**
```
Retrieve docs: [1 ════════ 5]
```

| Value | Use Case | Kết quả |
|-------|----------|--------|
| **1-2** | Chính xác cao | Nhanh, nhưng có thể thiếu context |
| **3** ⭐ | Balanced | Mặc định tốt cho hầu hết |
| **4-5** | Context dày đặc | Chậm hơn, có thể bao gồm noise |

**Thử:**
```bash
# Quick/chính xác
slider = 2

# Balanced
slider = 3

# Comprehensive
slider = 4
```

### B. Chunk Size (kích thước text chunks)

Tại: `chatbot_app.py` → `split_text()` function

```python
def split_text(text, chunk_size=500, overlap=100):
    #         ↑                          ↑
    #      Size (words)            Overlap (words)
```

**Điều chỉnh:**

| Size | Overlap | Khi nào | Ưu/Nhược |
|------|---------|---------|----------|
| 300 | 50 | Câu hỏi ngắn | ✅ Chính xác, ❌ Nhiều chunks |
| **500** ⭐ | **100** | Balanced | ✅ Cân bằng |
| 800 | 150 | Long context | ✅ Semantic, ❌ Chậm |
| 1000 | 200 | Docs dài | ✅ Full context |

**Ví dụ thay đổi:**

```python
# Để lấy chunks nhỏ hơn (chính xác hơn)
chunks = split_text(content, chunk_size=300, overlap=50)

# Để lấy chunks lớn hơn (context đầy đủ)
chunks = split_text(content, chunk_size=800, overlap=150)
```

---

## 🧠 2. Embedding Optimization

### A. Model Embedding (tự động sử dụng Sentence Transformers)

ChromaDB mặc định dùng: `all-MiniLM-L6-v2`

**Đặc điểm:**
- ✅ Nhẹ (22MB)
- ✅ Nhanh
- ✅ Đủ tốt cho tiếng Anh
- ⚠️ Tiếng Việt kém hơn

### B. Cải thiện cho Tiếng Việt

Tạo file `advanced_embedding.py`:

```python
from chromadb.utils import embedding_functions

# Dùng model tốt cho tiếng Việt
vietnamese_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="VoiceOfCommunity/vietnamese-embedding"
)

collection = client.get_or_create_collection(
    name="setup_guide",
    embedding_function=vietnamese_ef
)
```

Cài: `pip install sentence-transformers`

---

## 🎯 3. Query Optimization

### A. Query Pre-processing

**Tốt:**
```
"Làm sao để setup Google Cloud CLI?"
"How to install gcloud?"
"Steps to configure Vertex AI API"
```

**Kém:**
```
"setup"
"???"
"hmmm ok so"
```

### B. Query Expansion (tìm kiếm mở rộng)

Thêm vào `chatbot_app.py`:

```python
def expand_query(query):
    """Mở rộng query để tìm tài liệu liên quan hơn"""
    # Thêm synonyms
    synonyms = {
        "install": ["setup", "configure", "install"],
        "api": ["API", "service", "endpoint"],
        "gcloud": ["Google Cloud CLI", "gcloud", "cloud SDK"]
    }
    
    # Implement synonym expansion
    return expanded_queries

# Dùng
expanded = expand_query(user_query)
results = collection.query(query_texts=expanded, n_results=top_k)
```

---

## 💾 4. Knowledge Base Optimization

### A. Cải thiện Quality

**Tốt:**
```
📄 Tài liệu có structure rõ ràng
- Tiêu đề chi tiết
- Từng bước cụ thể
- Code examples
- Troubleshooting
```

**Kém:**
```
📄 Tài liệu lộn xộn
- Thiếu format
- Không có structure
- Khó phân tách sections
```

### B. Metadata Optimization

Edit khi add documents:

```python
collection.add(
    ids=[f"chunk_{i}"],
    documents=[chunk],
    metadatas=[{
        "source": "conw.txt",
        "section": "Installation",  # ← thêm
        "difficulty": "beginner",    # ← thêm
        "chunk_index": i,
        "timestamp": datetime.now().isoformat()
    }]
)
```

Sau đó filter:
```python
results = collection.query(
    query_texts=[query],
    n_results=top_k,
    where={"section": {"$eq": "Installation"}}
)
```

---

## 🤖 5. LLM Generation Optimization

### A. Temperature (Creativity)

```python
payload = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,  # 0=chính xác, 1=creative
    #              ↑
}
```

| Temperature | Behavior | Khi nào |
|-------------|----------|---------|
| 0.0 | Deterministic | Câu trả lời chính xác |
| **0.7** ⭐ | Balanced | Mặc định tốt |
| 1.0 | Creative | Mở rộng thêm idea |

### B. System Prompt

Edit: `generate_with_openai()` function

**Tốt:**
```python
system_prompt = """Bạn là expert về Google Cloud Setup.
Trả lời dựa CHÍNH XÁC trên context được cung cấp.
Nếu không có info, hãy nói rõ.
Format answer như sau:
1. Giải thích ngắn
2. Các bước cụ thể
3. Troubleshooting
"""
```

**Kém:**
```python
system_prompt = "Help me"
```

---

## ⚡ 6. Performance Tuning

### A. Vector Search Speed

```python
# ChromaDB tự động optimize
# Nhưng có thể manually tune:

collection = client.get_or_create_collection(
    name="setup_guide",
    metadata={
        "hnsw:space": "cosine",  # similarity metric
        "hnsw:M": 16,            # graph connectivity
        "hnsw:ef_construction": 200  # construction param
    }
)
```

### B. Batch Processing

Nếu có nhiều queries:

```python
# Thay vì 1 query lúc
result = collection.query(query_texts=[q], n_results=3)

# Làm batch
results = collection.query(
    query_texts=[q1, q2, q3],
    n_results=3
)  # Nhanh hơn 3x
```

---

## 📊 7. Evaluation Metrics

### A. Similarity Score

```python
# Return trong retrieve_context
similarity_scores = [1 - d for d in distances]

# Evaluate
if similarity < 0.5:
    st.warning("Liên quan thấp - thử lại câu hỏi")
elif similarity > 0.8:
    st.success("Liên quan cao")
```

### B. Relevance Feedback Loop

```python
# Thêm feedback UI
feedback = st.radio("Câu trả lời có hữu ích không?",
    ["👍 Yes", "👎 No", "🤔 Partially"])

if feedback == "👎 No":
    # Log để cải thiện
    log_failed_query(query, context)
```

---

## 🚀 8. Advanced Techniques

### A. Reranking (sắp xếp lại results)

```python
# Pip: pip install sentence-transformers

from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/qnli-distilroberta-base')

# Rerank top results
pairs = [[query, doc] for doc in documents]
scores = reranker.predict(pairs)
sorted_docs = [docs[i] for i in np.argsort(scores)[::-1]]
```

### B. Hybrid Search

```python
# Kết hợp vector + keyword search
def hybrid_search(query, top_k=3):
    # Vector search
    vector_results = collection.query(query_texts=[query])
    
    # Keyword search
    keyword_results = full_text_search(query)
    
    # Merge & rank
    combined = merge_results(vector_results, keyword_results)
    
    return combined[:top_k]
```

---

## 🎓 Checklist Tối ưu hóa

- [ ] Thử `top_k` từ 1-5, tìm sweet spot
- [ ] Điều chỉnh `chunk_size` theo dữ liệu
- [ ] Kiểm tra quality của knowledge base
- [ ] Test với các câu hỏi khác nhau
- [ ] Nếu tiếng Việt, upgrade embedding model
- [ ] Optimize system prompt
- [ ] Monitor similarity scores
- [ ] Collect user feedback
- [ ] A/B test different settings

---

## 📈 Kết quả kỳ vọng

Sau tối ưu, chatbot sẽ:

✅ Trả lời nhanh hơn (< 2s)
✅ Kết quả relevant cao (>80% similarity)
✅ Ít hallucination
✅ Chi tiết đủ (không thiếu context)
✅ Chính xác (dựa trên real documents)

---

## 🔗 Tham khảo

- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [RAG Best Practices](https://arxiv.org/abs/2312.10997)
- [OpenAI API](https://platform.openai.com/docs/)

---

**Happy Optimizing! 🚀**

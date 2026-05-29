# 🔑 Nơi Điền API Key & Configuration

Hướng dẫn điền API key, credentials, và cấu hình cần thiết để chạy chatbot.

---

## 🎯 Nơi Cần Điền Thông Tin

### 1️⃣ OpenAI API Key (Optional - để dùng GPT-3.5)

**File:** `.streamlit/secrets.toml`

**Vị trí:**
```
chatbot_/
└── .streamlit/
    └── secrets.toml  ← Mở file này
```

**Nội dung (copy-paste vào file):**
```toml
openai_api_key = "sk-your-actual-api-key-here"
```

**Ví dụ:**
```toml
openai_api_key = "sk-proj-1234567890abcdefghijklmnop"
```

**Cách lấy API key:**
1. https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy key
4. Paste vào file trên
5. Lưu file

**⚠️ Quan trọng:**
- Không share key này với ai
- Thêm `.streamlit/secrets.toml` vào `.gitignore` (đã làm sẵn)

---

### 2️⃣ Google Cloud Project ID & Credentials

Nếu muốn dùng Google Cloud services (Vertex AI, Secret Manager...):

**File:** `.streamlit/secrets.toml` (thêm nữa)

**Nội dung:**
```toml
openai_api_key = "sk-xxx"
gcp_project_id = "my-project-id"
gcp_credentials = "/path/to/service-account.json"
```

**Cách lấy Project ID:**
1. GCP Console → Settings ⚙️
2. Copy "Project ID"
3. Paste vào file

---

## 📍 Danh Sách Tất Cả Nơi Cần Điền

### A. Streamlit Secrets (chính yếu)

**File:** `.streamlit/secrets.toml`

```toml
# ========== LLM Configuration ==========

# Option 1: Dùng OpenAI
openai_api_key = "sk-proj-xxxxx"

# Option 2: Nếu muốn dùng Vertex AI (Google Cloud)
google_application_credentials = "/path/to/key.json"
gcp_project_id = "my-project"
gcp_location = "us-central1"
```

### B. Streamlit Config

**File:** `.streamlit/config.toml` (đã setup sẵn, không cần change)

Nếu muốn thay đổi:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501

[browser]
serverAddress = "0.0.0.0"
```

### C. Chatbot Code (nếu customize)

**File:** `chatbot_app.py` hoặc `chatbot_advanced.py`

Nơi có thể edit:

```python
# Dòng ~250 - LLM Configuration
def generate_response(query, context):
    api_key = st.secrets.get("openai_api_key", None)  # ← Lấy từ secrets.toml
    
# Dòng ~300 - Model Selection
"model": "gpt-3.5-turbo",  # ← Có thể thay "gpt-4"

# Dòng ~310 - Temperature
"temperature": 0.7,  # ← Thay từ 0 (chính xác) đến 1 (creative)
```

---

## 🔧 Step-by-Step: Setup API Key

### Bước 1: Tạo OpenAI API Key

```
https://platform.openai.com/api/keys
    ↓
Click "Create new secret key"
    ↓
Copy key: sk-proj-xxxx...
    ↓
Lưu ở chỗ an toàn (note, password manager, etc.)
```

### Bước 2: Điền vào secrets.toml

1. Mở file `.streamlit/secrets.toml` (tạo nếu chưa có)
2. Paste nội dung:
```toml
openai_api_key = "sk-proj-xxxx"
```
3. Ctrl+S lưu file

### Bước 3: Restart Streamlit

```bash
# Stop chatbot (Ctrl+C)
# Rồi chạy lại
streamlit run chatbot_app.py --server.address=0.0.0.0 --server.port=8501
```

### Bước 4: Test

1. Load Knowledge Base
2. Gửi message
3. Nếu thấy response từ OpenAI = Success! ✅

---

## 📋 Tất Cả Configuration Locations

| Thông tin | File | Format | Bắt buộc? |
|-----------|------|--------|-----------|
| OpenAI API Key | `.streamlit/secrets.toml` | `openai_api_key = "sk-..."` | ❌ Optional |
| GCP Project ID | `.streamlit/secrets.toml` | `gcp_project_id = "my-id"` | ❌ Optional |
| Streamlit Port | `.streamlit/config.toml` | `port = 8501` | ❌ No (default 8501) |
| Streamlit Address | `.streamlit/config.toml` | `address = "0.0.0.0"` | ✅ (for GCP VM) |
| Top-K Documents | Sidebar slider | Visual | ❌ No (default 3) |
| Model Choice | Code: `"model": "gpt-3.5-turbo"` | String | ❌ No |
| Temperature | Code: `"temperature": 0.7` | Float 0-1 | ❌ No |

---

## ⚡ Quick Setup (2 phút)

### Minimal Setup (chỉ cần local chạy):
```bash
# Không cần điền gì, chạy luôn
streamlit run chatbot_app.py
```

### Full Setup (dùng OpenAI):

**1. Lấy OpenAI API key:**
- https://platform.openai.com/api/keys
- Copy key

**2. Tạo `.streamlit/secrets.toml`:**
```toml
openai_api_key = "sk-your-key"
```

**3. Restart & test**

---

## 🆘 Nếu không biết info gì

### OpenAI API Key đâu?
```
→ https://platform.openai.com/api/keys
→ Create new secret key
→ Copy sk-... vào secrets.toml
```

### Google Cloud Project ID đâu?
```
→ https://console.cloud.google.com
→ Project selector (top left)
→ Copy project ID
→ Paste vào secrets.toml
```

### Streamlit config đâu?
```
→ .streamlit/config.toml
→ Đã setup sẵn, không cần thay đổi
```

### Chatbot code đâu?
```
→ chatbot_app.py (dòng 1-400)
→ Hoặc chatbot_advanced.py
→ Để nguyên nếu không biết code
```

---

## 📂 Đúng Structure

```
chatbot_/
├── .streamlit/
│   ├── config.toml .................... ✅ (sẵn sàng)
│   └── secrets.toml ................... ← ĐIỀN OPENAI KEY ĐÂY
├── chatbot_app.py .................... ✅ (sẵn sàng)
├── chatbot_advanced.py ............... ✅ (sẵn sàng)
├── requirements.txt .................. ✅ (sẵn sàng)
├── conw.txt .......................... ✅ (knowledge base sẵn sàng)
└── ...
```

**Chỉ cần tạo/edit: `.streamlit/secrets.toml`**

---

## 💡 Ví dụ Đầy Đủ

### Scenario 1: Local (không dùng OpenAI)
```bash
# Không cần tạo secrets.toml
streamlit run chatbot_app.py
# Chatbot sẽ dùng template responses
```

### Scenario 2: Local + OpenAI
```toml
# .streamlit/secrets.toml
openai_api_key = "sk-proj-abc123..."
```
```bash
streamlit run chatbot_app.py
# Chatbot sẽ dùng GPT-3.5
```

### Scenario 3: GCP VM + OpenAI
```toml
# .streamlit/secrets.toml
openai_api_key = "sk-proj-abc123..."
```
```bash
# SSH vào VM, rồi:
streamlit run chatbot_app.py --server.address=0.0.0.0 --server.port=8501
# Access: http://<EXTERNAL_IP>:8501
```

---

## ✅ Verification Checklist

- [ ] `.streamlit/secrets.toml` created (nếu muốn OpenAI)
- [ ] OpenAI API key pasted đúng format
- [ ] File lưu (Ctrl+S)
- [ ] Streamlit restarted
- [ ] Chatbot load Knowledge Base
- [ ] Test query → nhận response ✅

---

## 🎯 TL;DR

**Chỉ cần 1 file để config:**

```
.streamlit/secrets.toml
├── openai_api_key = "sk-xxx" (Optional)
└── gcp_project_id = "my-id" (Optional)
```

**Mà thôi! Hết!**

---

**Cần giúp gì thêm? Hỏi ở đây! 💬**

# 🔑 OpenAI API Integration Guide

Hướng dẫn sử dụng OpenAI API với chatbot để câu trả lời chất lượng cao hơn.

---

## ⚡ Quick Setup (5 phút)

### 1️⃣ Tạo OpenAI API Key

1. Đi tới https://platform.openai.com/api/keys
2. Login hoặc signup tài khoản
3. Bấp "Create new secret key"
4. Copy key (không share key này!)

**Format key:** `sk-xxxxxxxxxxxxxxxxxxxxx`

### 2️⃣ Lưu Key vào Streamlit Secrets

Tạo file `.streamlit/secrets.toml`:

```bash
# Windows: Mở Notepad
# File > Save As > .streamlit\secrets.toml

# Mac/Linux: Terminal
# nano .streamlit/secrets.toml
```

Nội dung:
```toml
openai_api_key = "sk-your-actual-key-here"
```

### 3️⃣ Chạy Chatbot

```bash
streamlit run chatbot_app.py
```

✅ Chatbot sẽ tự động detect API key và dùng OpenAI!

---

## 🎯 Chi tiết từng bước

### Step 1: Tạo OpenAI Account

1. https://openai.com
2. Bấp "Sign up"
3. Email / GitHub / Microsoft account
4. Verify email
5. Add payment method (credit card)

### Step 2: Tạo API Key

```
Dashboard
  ↓
API keys (sidebar)
  ↓
Create new secret key
  ↓
Copy & Save safely
```

### Step 3: Lưu vào Streamlit Secrets

**Option A: File `.streamlit/secrets.toml`**

Vị trí:
```
chatbot_/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml  ← Tạo file này
├── chatbot_app.py
└── ...
```

Content:
```toml
# .streamlit/secrets.toml
openai_api_key = "sk-xxxxxxxxxx"
```

⚠️ **GHI CHÚ QUAN TRỌNG:**
- File này **KHÔNG push lên Git** (thêm vào `.gitignore`)
- Giữ bí mật key này
- Nếu leak, delete key và tạo cái mới

---

## 💰 Pricing & Cost

### OpenAI Models

| Model | Input | Output | Speed | Quality |
|-------|-------|--------|-------|---------|
| GPT-3.5-turbo | $0.50/1M | $1.50/1M | ⚡ Fast | 📊 Good |
| GPT-4 | $30/1M | $60/1M | 🐢 Slow | 🎯 Best |
| GPT-4-turbo | $10/1M | $30/1M | ⚡ Medium | 🎯 Best |

### Ước tính Chi phí

**Chatbot_app.py (GPT-3.5):**

Mỗi query:
```
Input:  ~500 tokens × $0.50/1M = $0.00025
Output: ~300 tokens × $1.50/1M = $0.00045
Total:  ~$0.0007 per query
```

**Nếu:**
- 100 queries/ngày: ~$0.07/ngày = $2.1/tháng
- 1000 queries/ngày: ~$0.7/ngày = $21/tháng

💡 Bạn được free $5 credit mỗi tháng 3 lần.

---

## 🔧 Configuration

### A. Chọn Model

File: `chatbot_app.py` → `generate_with_openai()`

```python
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    json={
        "model": "gpt-3.5-turbo",  # ← Đổi ở đây
        # Tùy chọn: "gpt-4", "gpt-4-turbo-preview"
        ...
    }
)
```

### B. Điều chỉnh Temperature

```python
"temperature": 0.7,  # 0=chính xác, 1=creative
# Nên dùng 0.5-0.7 cho RAG
```

### C. Max Tokens

```python
"max_tokens": 500,  # Độ dài max của response
# Tăng nếu muốn response dài hơn
```

---

## 🧪 Test Configuration

### Bước 1: Verify API Key

```python
# test_openai.py
import requests
import os

api_key = "sk-your-key"

response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Say SUCCESS"}],
        "max_tokens": 10
    }
)

print(response.json())
```

Chạy:
```bash
python test_openai.py
```

Kỳ vọng output:
```json
{
  "choices": [
    {"message": {"content": "SUCCESS"}}
  ]
}
```

### Bước 2: Test Streamlit Integration

1. Tạo `.streamlit/secrets.toml`
2. Chạy chatbot
3. Load knowledge base
4. Gửi query - nếu thấy response từ OpenAI = success!

---

## 🚨 Troubleshooting

### Lỗi: "Unauthorized - check your API key"

**Giải pháp:**
1. Verify key ở https://platform.openai.com/api/keys
2. Kiểm tra key không có space/typo
3. Reload Streamlit: `Ctrl+C` → chạy lại

### Lỗi: "Quota exceeded"

**Giải pháp:**
1. Check usage: https://platform.openai.com/account/usage
2. Upgrade plan hoặc chờ reset hàng tháng
3. Có thể reduce `top_k` để giảm tokens

### Lỗi: "model not found"

**Giải pháp:**
1. Kiểm tra model name chính xác
2. GPT-4 cần be vào whitelist
3. Dùng `gpt-3.5-turbo` thay thế

### Chatbot trả lời chậm

**Giải pháp:**
1. API latency normal (~2-5s)
2. Reduce `max_tokens` → đỡ chậm
3. Reduce `top_k` → ít context → ít token

### Response không chính xác

**Giải pháp:**
1. Improve system prompt
2. Reduce temperature (0.5 thay 0.7)
3. Increase context documents (top_k)

---

## 📊 Monitoring Usage

### Dashboard OpenAI

1. https://platform.openai.com/account/usage
2. Xem:
   - Total cost
   - Cost by model
   - Request count
   - Token usage

### Manual Tracking

Thêm logging vào chatbot:

```python
def log_openai_usage(tokens_in, tokens_out):
    with open("usage_log.csv", "a") as f:
        f.write(f"{datetime.now()},{tokens_in},{tokens_out}\n")

# Gọi sau mỗi OpenAI response
log_openai_usage(input_tokens, output_tokens)
```

---

## 🔐 Security Best Practices

### ✅ DO:

```python
# ✅ Load từ Streamlit secrets
api_key = st.secrets.get("openai_api_key")

# ✅ Environment variables
api_key = os.environ.get("OPENAI_API_KEY")

# ✅ Giữ key bí mật
# ✅ Rotate key định kỳ
# ✅ Monitor usage
```

### ❌ DON'T:

```python
# ❌ Hardcode key
api_key = "sk-xxxxx"  # Never!

# ❌ Commit key lên Git
# git add .streamlit/secrets.toml  # NO!

# ❌ Share key
# "Dùng key này: sk-xxxxx"  # NO!

# ❌ Expose key in logs
print(api_key)  # NO!
```

---

## 💡 Advanced Tips

### A. Rate Limiting

```python
import time

def call_openai_with_rate_limit(prompt, delay=1):
    time.sleep(delay)  # 1 second delay
    return call_openai(prompt)
```

### B. Caching Responses

```python
@st.cache_data
def cached_openai_call(query):
    return call_openai(query)
```

### C. Fallback Strategy

```python
def generate_response(query, context):
    try:
        return generate_with_openai(query, context, api_key)
    except Exception as e:
        st.warning("OpenAI failed, using template instead")
        return generate_with_template(query, context)
```

---

## 🎓 Examples

### Example 1: Tối ưu cost

```python
# Reduce tokens
"max_tokens": 300,  # Thay 500
# Reduce context
top_k = 2  # Thay 3
# Reduce queries
# Cache common questions
```

### Example 2: Tối ưu quality

```python
# Increase context
top_k = 5

# Better prompt
system_prompt = """Expert advisor for Google Cloud.
Provide detailed, accurate answers based on context.
If unsure, ask clarifying questions."""

# Lower temperature
"temperature": 0.5
```

---

## 📚 Resources

- [OpenAI API Docs](https://platform.openai.com/docs/)
- [API Pricing](https://openai.com/pricing)
- [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Model Comparison](https://platform.openai.com/docs/models)

---

## ✅ Checklist

- [ ] Tạo OpenAI account
- [ ] Tạo API key
- [ ] Lưu vào `.streamlit/secrets.toml`
- [ ] Test bằng `test_openai.py`
- [ ] Chạy chatbot
- [ ] Verify API key work
- [ ] Monitor usage regularly
- [ ] Backup key ở chỗ an toàn
- [ ] Set budget alerts
- [ ] Read pricing docs

---

**Ready to use OpenAI? 🚀**

1. Get API key: https://platform.openai.com/api/keys
2. Save to secrets.toml
3. Run chatbot
4. Enjoy! 🎉

# 🚀 Quick Start Guide - Chatbot Setup

## ⚡ Chạy nhanh nhất (3 bước)

### **Windows Users:**
```bash
# Double-click vào file: run_chatbot.bat
```

### **Mac/Linux Users:**
```bash
# Terminal: chmod +x run_chatbot.sh && ./run_chatbot.sh
```

---

## 📋 Chi tiết từng bước

### **Bước 1: Cài đặt Python (nếu chưa có)**

**Windows:**
- Download từ https://www.python.org/downloads/
- Chọn "Add Python to PATH" khi cài đặt

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
```

### **Bước 2: Mở terminal/command prompt**

**Windows:**
- Nhấn `Win + R`
- Gõ `cmd` hoặc `powershell`

**Mac/Linux:**
- Mở Terminal

### **Bước 3: Navigate đến thư mục chatbot_**

```bash
cd đường/dẫn/đến/chatbot_
```

Ví dụ:
```bash
cd d:\USER\test__\chatbot_
```

### **Bước 4: Cài dependencies**

```bash
pip install -r requirements.txt
```

⏳ Chờ khoảng 2-5 phút (lần đầu sẽ download models)

### **Bước 5: Chạy chatbot**

```bash
streamlit run chatbot_app.py
```

✅ Trình duyệt sẽ tự động mở `http://localhost:8501`

---

## 💡 Sử dụng Chatbot

### **Bước 1: Load Knowledge Base**
- Nhấp vào nút **"🔄 Load Knowledge Base"** ở sidebar
- Chờ cho đến khi thấy "✅ Knowledge base ready"

### **Bước 2: Đặt câu hỏi**
- Nhập câu hỏi vào chat input
- Bấm Enter hoặc nhấp nút send

### **Bước 3: Xem kết quả**
- Chatbot sẽ trả lời dựa trên knowledge base
- Mở "📄 Source Documents" để xem tài liệu nguồn

---

## 🎯 Ví dụ sử dụng

### **Câu hỏi 1: Bước đầu**
```
"Tôi cần làm gì trước tiên để setup Google Cloud?"
```

**Trả lời dự kiến:**
> Bạn cần cài đặt Google Cloud CLI, tạo project, enable Vertex AI API...

### **Câu hỏi 2: Chi tiết**
```
"Làm sao để install gcloud CLI?"
```

**Trả lời dự kiến:**
> Bước 1: Download từ google-cloud-cli...
> Bước 2: Giải nén file...

### **Câu hỏi 3: Troubleshoot**
```
"Lỗi gì khi test Gemini?"
```

**Trả lời dự kiến:**
> Kiểm tra PROJECT_ID có đúng không, API có enable không...

---

## ⚙️ Tuỳ chỉnh cơ bản

### Thay đổi số documents retrieved
- Sidebar → "Retrieve docs" → Kéo slider từ 1 đến 5
- 3 là mặc định (đã tốt), 5 nếu muốn chi tiết hơn

### Xóa chat history
- Bấp nút **"🗑️ Clear Chat"** ở sidebar

### Reload knowledge base
- Bấp nút **"🔄 Load Knowledge Base"** lại

---

## 🔧 Troubleshooting

### **Lỗi: "ModuleNotFoundError: No module named 'streamlit'"**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Lỗi: "conw.txt not found"**
- Đảm bảo file `conw.txt` ở cùng thư mục với `chatbot_app.py`

### **Lỗi: "Port 8501 already in use"**
```bash
streamlit run chatbot_app.py --server.port 8502
```

### **Chatbot chạy chậm lần đầu**
- Bình thường! ChromaDB download models, mất 2-5 phút
- Lần sau sẽ nhanh hơn

### **Chatbot không trả lời chính xác**
- Thử reload knowledge base
- Đặt câu hỏi cụ thể hơn
- Tăng "Retrieve docs" trong sidebar

---

## 📚 Dữ liệu & Cấu trúc

**Knowledge Base:** File `conw.txt`
- Chứa hướng dẫn setup Google Cloud + Vertex AI
- Tự động được chia thành chunks
- Chuyển thành vectors bằng Sentence Transformers

**Vector Storage:** Folder `chatbot_data/`
- ChromaDB tự động tạo
- Lưu embeddings của documents
- Xóa folder này để reset knowledge base

---

## 🔐 Nâng cao: Dùng OpenAI API

Nếu bạn có OpenAI API key và muốn kết quả tốt hơn:

1. Tạo folder `.streamlit` (nếu chưa có):
```bash
mkdir .streamlit
```

2. Tạo file `.streamlit/secrets.toml`:
```toml
openai_api_key = "sk-xxxxxxxxxxxxxx"
```

3. Lưu file và reload chatbot

Chatbot sẽ tự động dùng OpenAI khi có API key.

---

## ❓ FAQ

**Q: Có cần internet không?**
A: Lần đầu cần (download models). Sau đó chạy offline được.

**Q: Có cost gì không?**
A: Không (local). Nếu dùng OpenAI API mới có cost.

**Q: Tôi có thể thêm knowledge base khác không?**
A: Hiện tại dùng `conw.txt`. Bạn có thể edit file này hoặc modify code.

**Q: Lưu chat history ở đâu?**
A: Chỉ lưu trong session (khi reload page sẽ mất).

**Q: Có thể dùng GPT-4 không?**
A: Có, edit code và thay `gpt-3.5-turbo` thành `gpt-4`.

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra troubleshooting trên
2. Đảm bảo Python 3.8+
3. Thử reinstall: `pip install -r requirements.txt --upgrade`

---

**Happy Chatting! 🎉**

# 📚 Chatbot Documentation Index

Danh sách các tài liệu và hướng dẫn cho chatbot RAG của bạn.

---

## 🎯 Bắt Đầu Nhanh

### 🎯 BẠN ĐÃ CÓ GCP VM RỒI? ⭐ LÀM CÁI NÀY:
1. **[SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md)** ⭐ STEP-BY-STEP (15 phút)
   - 9 bước setup từ A-Z
   - Upload files → Setup dependencies → Chạy
   - Nơi điền API key chính xác
   - Commands copy-paste

### Cho người mới (chạy local trước):
2. **[QUICKSTART.md](./QUICKSTART.md)** ⭐ START HERE (Local)
   - Hướng dẫn chạy trong 3 bước
   - Windows & Mac/Linux commands
   - Troubleshooting cơ bản
   - Q&A thường gặp

3. **[CONFIGURATION.md](./CONFIGURATION.md)** - NƠI ĐIỀN API KEY
   - Nơi cần điền OpenAI API key
   - Nơi điền Google Cloud ID
   - Quick setup (2 phút)
   - Tất cả configuration locations

### Cho người muốn chi tiết:
4. **[README.md](./README.md)**
   - Tính năng đầy đủ
   - Cài đặt chi tiết
   - Tùy chỉnh nâng cao
   - Cấu trúc dự án

---

## 🎯 Chọn Version

### Version Selection:
5. **[VERSIONS.md](./VERSIONS.md)**
   - So sánh `chatbot_app.py` vs `chatbot_advanced.py`
   - Bảng feature comparison
   - Khi nào dùng cái nào
   - Performance comparison

---

## 🤖 RAG & LLM

### Hiểu RAG & Tối ưu:
6. **[RAG_OPTIMIZATION.md](./RAG_OPTIMIZATION.md)**
   - Cơ bản về RAG pipeline
   - Điều chỉnh `top_k`, chunk size
   - Embedding optimization
   - Query optimization
   - Performance tuning
   - Advanced techniques (reranking, hybrid search)
   - Evaluation metrics

### OpenAI Integration:
7. **[OPENAI_SETUP.md](./OPENAI_SETUP.md)**
   - Tạo OpenAI API key (5 phút)
   - Configuration details
   - Pricing & cost estimates
   - Testing API key
   - Security best practices
   - Troubleshooting API errors

---

## 📂 Cấu Trúc Dự Án

```
chatbot_/
├── 📄 Documents (Đọc các tài liệu)
│   ├── QUICKSTART.md .................. Chạy nhanh local (5 phút)
│   ├── CONFIGURATION.md .............. Nơi điền API key ⭐
│   ├── GCP_QUICKSTART.md ............. Deploy GCP (10 phút) ⭐
│   ├── GCP_DEPLOYMENT.md ............. Chi tiết GCP setup
│   ├── README.md ..................... Tổng quan đầy đủ
│   ├── VERSIONS.md ................... So sánh versions
│   ├── RAG_OPTIMIZATION.md ........... Tối ưu RAG
│   ├── OPENAI_SETUP.md .............. Dùng OpenAI API
│   └── INDEX.md (file này) .......... Navigation guide
│
├── 🐍 Python Code
│   ├── chatbot_app.py ................ Version simple ⭐
│   ├── chatbot_advanced.py ........... Version advanced
│   ├── requirements.txt .............. Dependencies
│   └── .streamlit/
│       ├── config.toml .............. Streamlit config
│       └── secrets.toml ............. ← ĐIỀN API KEY ĐÂY
│
├── 🔧 Configuration & Scripts
│   ├── run_chatbot.bat .............. Windows runner (local)
│   ├── run_chatbot.sh ............... Mac/Linux runner (local)
│   ├── setup_gcp.sh ................. Auto-setup on GCP VM
│   ├── setup_service.sh ............. Systemd service setup
│   ├── .gitignore ................... Git ignore rules
│   └── conw.txt ..................... Knowledge base
│
└── 📦 Generated (auto-created)
    └── chatbot_data/ ................ ChromaDB vectors
```

---

## 📖 Quick Reference

### Commands

**Windows:**
```bash
# Chạy version simple
double-click run_chatbot.bat

# Hoặc Terminal:
pip install -r requirements.txt
streamlit run chatbot_app.py
```

**Mac/Linux:**
```bash
# Chạy version simple
chmod +x run_chatbot.sh && ./run_chatbot.sh

# Hoặc:
pip install -r requirements.txt
streamlit run chatbot_app.py
```

**Chạy version advanced:**
```bash
streamlit run chatbot_advanced.py
```

### Features

| Feature | File | Link |
|---------|------|------|
| **Basic Chat** | chatbot_app.py | [Run](./QUICKSTART.md) |
| **Advanced UI** | chatbot_advanced.py | [Run](./VERSIONS.md) |
| **API Integration** | Both | [Guide](./OPENAI_SETUP.md) |
| **Optimization** | Both | [Guide](./RAG_OPTIMIZATION.md) |
| **Full Docs** | All | [README](./README.md) |

---

## � Learning Path

### Beginner (Local Machine):
```
1. QUICKSTART.md (5 min)
   ↓
2. Run chatbot_app.py
   ↓
3. Load knowledge base
   ↓
4. Ask questions
```

### Intermediate (Google Cloud) ⭐ YOU ARE HERE:
```
1. GCP_QUICKSTART.md (10 min) ⭐
   ↓
2. Create VM: gcloud compute instances create ...
   ↓
3. SSH: bash setup_gcp.sh
   ↓
4. Access: http://<EXTERNAL_IP>:8501
```

### Advanced (Optimize & Customize):
```
1. RAG_OPTIMIZATION.md
   ↓
2. OPENAI_SETUP.md
   ↓
3. GCP_DEPLOYMENT.md (advanced)
   ↓
4. Customize code & deploy
```

---

## 🔍 By Problem

### Lỗi gì đó:

| Problem | Solution |
|---------|----------|
| **"Nơi điền API key?"** | **[CONFIGURATION.md](./CONFIGURATION.md)** ⭐ |
| **"Nơi điền Google Cloud ID?"** | **[CONFIGURATION.md](./CONFIGURATION.md)** |
| "Làm sao chạy?" | [QUICKSTART.md](./QUICKSTART.md#chạy-nhanh-nhất-3-bước) |
| "Không load được KB" | [README.md](./README.md#troubleshooting) |
| "Chạy chậm" | [RAG_OPTIMIZATION.md](./RAG_OPTIMIZATION.md#-6-performance-tuning) |
| "Muốn dùng OpenAI" | [OPENAI_SETUP.md](./OPENAI_SETUP.md#-quick-setup-5-phút) |
| "Chatbot trả lời sai" | [RAG_OPTIMIZATION.md](./RAG_OPTIMIZATION.md#-5-llm-generation-optimization) |
| "Cost quá cao" | [OPENAI_SETUP.md](./OPENAI_SETUP.md#-pricing--cost) |
| **"Muốn deploy lên Cloud?"** | **[GCP_QUICKSTART.md](./GCP_QUICKSTART.md)** ⭐ |
| **"Setup trên GCP VM"** | **[GCP_DEPLOYMENT.md](./GCP_DEPLOYMENT.md)** |
| **"GCP firewall/network"** | **[GCP_DEPLOYMENT.md](./GCP_DEPLOYMENT.md#-7-setup-firewall)** |

---

## ☁️ Google Cloud Deployment

**Deploy on Google Cloud VM (Recommended!):**

1. **[GCP_QUICKSTART.md](./GCP_QUICKSTART.md)** ⭐ FASTEST DEPLOY (10 min)
   - Ultra-quick commands
   - Commands cheat sheet
   - Cost tracking
   - Common issues

2. **[GCP_DEPLOYMENT.md](./GCP_DEPLOYMENT.md)** - DETAILED GUIDE
   - Step-by-step GCP setup
   - Create & configure VM
   - Firewall & networking
   - Cost estimation
   - Monitoring & security

3. **Setup Scripts (Run on GCP VM):**
   - `setup_gcp.sh` - Auto-setup all dependencies
   - `setup_service.sh` - Configure systemd service
   - Both are executable bash scripts

---

## 🔗 External Links

### Tools & Libraries:
- [Streamlit](https://streamlit.io/) - Web framework
- [ChromaDB](https://docs.trychroma.com/) - Vector DB
- [Sentence Transformers](https://www.sbert.net/) - Embeddings
- [OpenAI API](https://platform.openai.com/) - LLM
- [Google Cloud](https://cloud.google.com/) - VM hosting

### Learning:
- [RAG Paper](https://arxiv.org/abs/2005.11401) - Original RAG
- [Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering) - Best practices
- [Vector Search](https://www.sbert.net/docs/usage/semantic_search.html) - How it works

---

## ✅ Checklist

### First Time Setup:
- [ ] Download/clone project
- [ ] Read QUICKSTART.md
- [ ] Install Python 3.8+
- [ ] Run `pip install -r requirements.txt`
- [ ] Run chatbot: `streamlit run chatbot_app.py`
- [ ] Load knowledge base (button ở sidebar)
- [ ] Ask a test question

### Optimization:
- [ ] Read RAG_OPTIMIZATION.md
- [ ] Test different `top_k` values
- [ ] Adjust chunk_size
- [ ] Monitor similarity scores
- [ ] Collect feedback

### Production Ready:
- [ ] Setup OpenAI API (nếu muốn)
- [ ] Test with various queries
- [ ] Set up monitoring
- [ ] Document custom changes
- [ ] Deploy to server

---

## 📞 Support

### Before Asking:
1. Check relevant doc (link ở table "By Problem")
2. Search key terms trong docs
3. Read troubleshooting sections

### Getting Help:
- Python issues: Check Python docs
- Streamlit issues: [Streamlit Forum](https://discuss.streamlit.io/)
- ChromaDB issues: [ChromaDB Docs](https://docs.trychroma.com/)
- OpenAI issues: [OpenAI Support](https://support.openai.com/)

---

## 📝 File Descriptions

### Documentation Files

| File | Purpose | Length | When to Read |
|------|---------|--------|--------------|
| QUICKSTART.md | 3-step setup + Q&A | 5 min | First thing |
| README.md | Full documentation | 20 min | Want details |
| VERSIONS.md | Version comparison | 10 min | Before choosing |
| RAG_OPTIMIZATION.md | Advanced tuning | 30 min | Optimize quality |
| OPENAI_SETUP.md | API integration | 15 min | Use OpenAI |
| INDEX.md (này) | Navigation | 10 min | Lost? Read this |

### Code Files

| File | Purpose | Lines | Complexity |
|------|---------|-------|-----------|
| chatbot_app.py | Simple version | ~200 | ⭐ Low |
| chatbot_advanced.py | Advanced version | ~400 | ⭐⭐ Medium |
| requirements.txt | Dependencies | ~10 | Simple |

### Config Files

| File | Purpose | Edit? |
|------|---------|-------|
| .streamlit/config.toml | Streamlit settings | Maybe |
| .streamlit/secrets.toml | API keys | Yes (create) |
| .gitignore | Git ignore rules | No |

### Data Files

| File | Purpose | Size | Editable |
|------|---------|------|----------|
| conw.txt | Knowledge base | ~5KB | Yes |
| chatbot_data/ | Vector store (auto) | Variable | No |

---

## 🎯 Next Steps

### Pick Your Path:

**"Just want to run it"**
→ QUICKSTART.md → Done!

**"Want to understand how it works"**
→ README.md → RAG_OPTIMIZATION.md

**"Want better results with AI"**
→ OPENAI_SETUP.md → RAG_OPTIMIZATION.md

**"Want to customize code"**
→ VERSIONS.md → README.md → Code

**"Want to deploy to production"**
→ All docs → Setup monitoring → Deploy

---

## 💡 Pro Tips

1. **Start Simple**: Chạy `chatbot_app.py` trước
2. **Test Settings**: Thử `top_k` từ 1-5 để tìm best
3. **Monitor Logs**: Check similarity scores & response time
4. **Iterate**: Adjust settings dựa trên feedback
5. **Backup**: Lưu `.streamlit/secrets.toml` an toàn

---

## 🎉 Ready?

```
1. Pick a doc from above
2. Follow the guide
3. Run the chatbot
4. Ask questions
5. Enjoy! 🚀
```

---

**Last Updated**: May 2026
**Version**: 1.0
**Status**: Ready to use ✅

For updates or issues, check docs first! 📚

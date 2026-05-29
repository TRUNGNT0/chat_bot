# 📱 Chatbot Versions Comparison

Dự án này cung cấp **2 phiên bản chatbot** để bạn lựa chọn theo nhu cầu:

## 🎯 Phiên bản 1: `chatbot_app.py` - Simple & Clean

**👍 Ưu điểm:**
- Giao diện đơn giản, dễ sử dụng
- Chạy nhanh, ít dependencies
- Lý tưởng cho người mới bắt đầu
- Thiết kế tối ưu cho mobile
- Chat interface trực quan

**👎 Nhược điểm:**
- Tính năng hạn chế
- Không thể export chat history
- Không hiển thị similarity scores
- Thiếu stats chi tiết

**🎓 Khi nào dùng:**
- Mới học Streamlit
- Chỉ cần RAG cơ bản
- Muốn interface đơn giản
- Thiết bị yếu (startup nhanh)

**▶️ Chạy:**
```bash
streamlit run chatbot_app.py
```

---

## 🚀 Phiên bản 2: `chatbot_advanced.py` - Feature-Rich

**👍 Ưu điểm:**
- Layout 2 cột (Control + Chat)
- 📊 Statistics & metrics
- 💾 Export chat history (JSON/CSV)
- 📄 Show similarity scores
- 🔔 Detailed source documents
- Cấu hình chi tiết

**👎 Nhược điểm:**
- Giao diện phức tạp hơn
- Chạy chậm hơn (do UI elements)
- Cần giải quyết layout trên mobile
- Code dài hơn, khó tùy chỉnh

**🎓 Khi nào dùng:**
- Dự án production
- Cần lưu chat history
- Muốn analyze performance
- Team development

**▶️ Chạy:**
```bash
streamlit run chatbot_advanced.py
```

---

## 📊 So sánh Chi tiết

| Feature | Simple | Advanced |
|---------|--------|----------|
| Chat Interface | ✅ | ✅ |
| Load KB | ✅ | ✅ |
| RAG Retrieval | ✅ | ✅ |
| OpenAI Integration | ✅ | ✅ |
| Settings | Basic | Full |
| Export History | ❌ | ✅ JSON/CSV |
| Similarity Score | ❌ | ✅ |
| Statistics | ❌ | ✅ |
| Clear Chat | ✅ | ✅ |
| UI Complexity | Low | Medium |
| Performance | Fast | Medium |
| Mobile Friendly | ✅ | Partial |
| Code Length | ~200 lines | ~400 lines |

---

## 🎮 Hướng dẫn Chọn

### Nếu bạn...

**"Muốn chạy nhanh nhất"** → `chatbot_app.py`
- Đơn giản, gọn gàng
- Startup lần đầu cũng nhanh

**"Muốn demo cho team"** → `chatbot_advanced.py`
- Hiển thị statistics
- Export results
- Chuyên nghiệp hơn

**"Mới học Streamlit"** → `chatbot_app.py`
- Code dễ hiểu
- Tập trung vào RAG logic
- Ít distraction

**"Làm project thực tế"** → `chatbot_advanced.py`
- Full-featured
- Export/Analytics
- Professional

---

## 🔄 Chuyển đổi giữa 2 Version

Cả 2 version sử dụng **cùng knowledge base** (`conw.txt`)

Để chuyển sang version khác:

```bash
# Dùng version simple (mặc định)
streamlit run chatbot_app.py

# Hoặc dùng advanced
streamlit run chatbot_advanced.py
```

Chat history không share giữa 2 version (được lưu riêng rẽ).

---

## 🛠️ Tùy chỉnh

### Tùy chỉnh `chatbot_app.py`

Edit file để thay đổi:
- **Màu sắc:** Section CSS
- **Prompt:** `generate_with_template()` function
- **Layout:** Sidebar vs main

### Tùy chỉnh `chatbot_advanced.py`

Edit file để thay đổi:
- **Layout:** `col1, col2 = st.columns([ratio])`
- **Metrics:** `st.metric()` calls
- **Export formats:** Thêm XML, Markdown, etc.

---

## ⚡ Performance Tips

### Nếu `chatbot_app.py` chạy chậm:
```bash
# Giảm top_k (default 3)
streamlit run chatbot_app.py -- --top_k=2
```

### Nếu `chatbot_advanced.py` chạy chậm:
- Giảm `top_k` slider
- Minimize sidebar
- Reload page

---

## 🔧 Troubleshooting

### Lỗi chạy từ version này sang version khác?
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache  # Linux/Mac
rmdir /s %USERPROFILE%\.streamlit\cache  # Windows
```

### Chat history bị mất?
- Mỗi version lưu riêng trong session
- Reload page = session mất
- Dùng export để lưu lâu dài

### OpenAI API không hoạt động?
- Kiểm tra `.streamlit/secrets.toml`
- Verify API key hợp lệ
- Check balance tài khoản

---

## 🚀 Nâng cao

### Tạo version riêng

Bạn có thể copy một trong 2 version và tùy chỉnh:

```bash
cp chatbot_app.py chatbot_custom.py
```

Edit `chatbot_custom.py` theo ý muốn, rồi chạy:
```bash
streamlit run chatbot_custom.py
```

### Kết hợp features từ cả 2

Sao chép tính năng yêu thích từ:
- **Simple → Advanced**: Export, Stats
- **Advanced → Simple**: Clean layout

---

## 📚 Tài liệu Thêm

- [chatbot_app.py Documentation](./README.md)
- [Quick Start Guide](./QUICKSTART.md)
- [Streamlit Docs](https://docs.streamlit.io/)

---

**Chọn version phù hợp và bắt đầu sử dụng! 🎉**

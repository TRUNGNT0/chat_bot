# ✅ Setup Checklist - Làm Theo Thứ Tự

Danh sách bước bước để setup chatbot trên Google Cloud VM.

---

## 🚀 Quick Setup (15 phút)

### ✔️ Step 1: Upload Files to GCP VM
```bash
# Từ local computer
gcloud compute scp --recurse d:\USER\test__\chatbot_/* \
    chatbot-vm:~/chatbot/ \
    --zone=us-central1-a
```

**Status:** Files uploaded ✅

---

### ✔️ Step 2: SSH vào VM
```bash
gcloud compute ssh chatbot-vm --zone=us-central1-a
```

**Status:** Connected to VM ✅

---

### ✔️ Step 3: Chạy Auto-Setup Script
```bash
cd ~/chatbot
bash setup_gcp.sh
```

**Điều này sẽ:**
- ✅ Update system
- ✅ Install Python & dependencies
- ✅ Create virtual environment
- ✅ Install pip packages
- ✅ Setup Streamlit config
- ✅ (Optional) Add OpenAI API key

**Status:** Environment ready ✅

---

### ✔️ Step 4: Điền API Key (Optional)

Nếu muốn dùng OpenAI GPT-3.5:

```bash
# Edit secrets file
nano ~/.streamlit/secrets.toml
```

**Paste nội dung:**
```toml
openai_api_key = "sk-proj-your-actual-key-here"
```

**Cách lấy key:**
1. https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy key
4. Paste vào file

**Save:** `Ctrl+X` → `Y` → `Enter`

**Status:** API key configured ✅

---

### ✔️ Step 5: Setup Auto-Start Service (Optional)

Để chatbot auto-start mỗi khi VM reboot:

```bash
bash ~/chatbot/setup_service.sh
```

**Status:** Service configured ✅

---

### ✔️ Step 6: Start Chatbot

**Option A: Direct**
```bash
cd ~/chatbot
source venv/bin/activate
streamlit run chatbot_app.py --server.address=0.0.0.0 --server.port=8501
```

**Option B: Background (nohup)**
```bash
cd ~/chatbot
source venv/bin/activate
nohup streamlit run chatbot_app.py --server.address=0.0.0.0 --server.port=8501 > streamlit.log 2>&1 &
```

**Option C: Service**
```bash
sudo systemctl start chatbot
sudo systemctl status chatbot  # Check status
```

**Status:** Chatbot running ✅

---

### ✔️ Step 7: Get External IP

```bash
gcloud compute instances describe chatbot-vm \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

Example output:
```
34.125.123.45
```

**Status:** IP address found ✅

---

### ✔️ Step 8: Access Chatbot

Open browser:
```
http://34.125.123.45:8501
```

**Status:** Chatbot accessible ✅

---

### ✔️ Step 9: Test Chatbot

1. Load Knowledge Base (click button)
2. Ask a question: "Làm sao để setup Google Cloud CLI?"
3. Check response

**Status:** Chatbot working ✅

---

## 📋 Full Checklist

### Before Starting:
- [ ] Google Cloud VM created (e2-medium recommended)
- [ ] Firewall rule opened (port 8501)
- [ ] SSH access working

### During Setup:
- [ ] Files uploaded to VM
- [ ] setup_gcp.sh executed
- [ ] Dependencies installed
- [ ] (Optional) OpenAI API key configured
- [ ] (Optional) Systemd service setup
- [ ] Chatbot started

### After Running:
- [ ] External IP obtained
- [ ] Browser access working
- [ ] Knowledge base loaded
- [ ] Test query successful
- [ ] (Optional) Systemd auto-start verified

---

## 🎯 If You Want to Use OpenAI API

### Step A: Get API Key
1. https://platform.openai.com/api/keys
2. "Create new secret key"
3. Copy: `sk-proj-xxx`

### Step B: Add to secrets.toml
```bash
nano ~/.streamlit/secrets.toml
```

Content:
```toml
openai_api_key = "sk-proj-your-key"
```

Save: `Ctrl+X` → `Y` → `Enter`

### Step C: Restart Streamlit
```bash
# If using service:
sudo systemctl restart chatbot

# If using direct:
# Ctrl+C on terminal, then restart
```

### Step D: Test
- Send message in chatbot
- Should get GPT-3.5 response (not template)

---

## 🔧 Common Commands on GCP VM

```bash
# SSH vào VM
gcloud compute ssh chatbot-vm --zone=us-central1-a

# Activate venv
source ~/chatbot/venv/bin/activate

# Run chatbot (direct)
streamlit run ~/chatbot/chatbot_app.py --server.address=0.0.0.0 --server.port=8501

# Run chatbot (background)
nohup streamlit run ... > streamlit.log 2>&1 &

# Check if port is open
curl http://localhost:8501

# View logs (if systemd)
sudo journalctl -u chatbot -f

# Stop service
sudo systemctl stop chatbot

# Restart service
sudo systemctl restart chatbot

# Edit secrets
nano ~/.streamlit/secrets.toml

# Kill process on port 8501
lsof -i :8501
kill -9 <PID>
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "setup_gcp.sh not found" | `chmod +x setup_gcp.sh` then run |
| "ModuleNotFoundError" | Activate venv: `source venv/bin/activate` |
| "Port 8501 already in use" | Kill process: `lsof -i :8501 \| kill -9` |
| "Can't SSH to VM" | Check VM running: `gcloud compute instances list` |
| "ChatBot loads but no response" | Load knowledge base (button ở sidebar) |
| "OpenAI not working" | Check secrets.toml has API key |
| "Connection timeout" | Check firewall rule opened |

---

## 📊 Quick Status Check

After everything setup, run:

```bash
# Check if running
ps aux | grep streamlit

# Check port
netstat -tulpn | grep 8501

# Check logs
tail -f ~/streamlit.log

# Check service (if systemd)
sudo systemctl status chatbot
```

All good = All green lights ✅

---

## 🎉 Success!

If you can see chatbot at `http://<IP>:8501` → **Setup Complete!**

---

## 📞 Need Help?

- **Local setup**: Read [QUICKSTART.md](./QUICKSTART.md)
- **GCP setup**: Read [GCP_DEPLOYMENT.md](./GCP_DEPLOYMENT.md)
- **API key**: Read [CONFIGURATION.md](./CONFIGURATION.md)
- **API cost**: Read [OPENAI_SETUP.md](./OPENAI_SETUP.md)
- **Not sure**: Read [INDEX.md](./INDEX.md) for navigation

---

**Done! Enjoy your chatbot! 🚀**

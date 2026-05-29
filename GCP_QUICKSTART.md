# ☁️ Google Cloud Quick Deploy

**Deploy chatbot lên Google Cloud VM trong 10 phút.**

---

## 🚀 Ultra-Quick Start

### Local Computer:

```bash
# 1. Create VM
gcloud compute instances create chatbot-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=debian-11 \
    --image-project=debian-cloud

# 2. Upload files
gcloud compute scp --recurse ~/chatbot_/* \
    chatbot-vm:~/chatbot/ \
    --zone=us-central1-a

# 3. Open firewall
gcloud compute firewall-rules create allow-streamlit \
    --allow=tcp:8501

# 4. SSH & setup
gcloud compute ssh chatbot-vm --zone=us-central1-a
```

### On Google Cloud VM (SSH):

```bash
# 5. Run setup script
cd ~/chatbot
bash setup_gcp.sh

# 6. Start service (optional)
bash setup_service.sh

# 7. Get IP
gcloud compute instances describe chatbot-vm \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### Browser:

```
http://<EXTERNAL_IP>:8501
```

---

## 📋 Commands Cheat Sheet

### Create & Manage VM

```bash
# Create
gcloud compute instances create chatbot-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=debian-11 --image-project=debian-cloud

# List
gcloud compute instances list

# SSH
gcloud compute ssh chatbot-vm --zone=us-central1-a

# Stop (save cost)
gcloud compute instances stop chatbot-vm --zone=us-central1-a

# Start
gcloud compute instances start chatbot-vm --zone=us-central1-a

# Delete
gcloud compute instances delete chatbot-vm --zone=us-central1-a
```

### Transfer Files

```bash
# Upload file
gcloud compute scp ~/file.txt chatbot-vm:~/

# Upload folder
gcloud compute scp --recurse ~/chatbot_/* chatbot-vm:~/chatbot/

# Download file
gcloud compute scp chatbot-vm:~/file.txt ~/
```

### Network

```bash
# Open port 8501
gcloud compute firewall-rules create allow-streamlit \
    --allow=tcp:8501

# View firewall rules
gcloud compute firewall-rules list

# Delete firewall rule
gcloud compute firewall-rules delete allow-streamlit

# Get external IP
gcloud compute instances describe chatbot-vm \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### On VM (SSH)

```bash
# Activate venv
source ~/chatbot/venv/bin/activate

# Run Streamlit
streamlit run ~/chatbot/chatbot_app.py \
    --server.address=0.0.0.0 --server.port=8501

# Or with nohup (background)
nohup streamlit run ~/chatbot/chatbot_app.py \
    --server.address=0.0.0.0 --server.port=8501 \
    > ~/streamlit.log 2>&1 &

# Or with systemd
sudo systemctl start chatbot
sudo systemctl status chatbot
sudo journalctl -u chatbot -f  # View logs

# Kill process
kill -9 <PID>
lsof -i :8501  # Find PID on port 8501
```

---

## 📊 Zones & Machines

### Popular Zones:

```
us-central1-a  (Iowa)         - US East
us-west1-b     (Oregon)       - US West
europe-west1-b (Belgium)      - Europe
asia-east1-a   (Taiwan)       - Asia
```

### Machine Types:

```
e2-small       $12/month   (0.5 vCPU, 2GB)   - Slow
e2-medium      $25/month   (1 vCPU, 4GB)     - ⭐ Good
e2-standard-2  $50/month   (2 vCPU, 8GB)     - Fast
```

---

## 💰 Cost Tracker

Monthly cost estimate:

```
VM (e2-medium):           $25
Network (10GB):            $1
Storage (30GB):            $1
Other:                     $1
─────────────────────────────
Total:                   ~$28/month
```

**Reduce cost:**
```bash
# Stop VM when not using
gcloud compute instances stop chatbot-vm

# Delete unused resources
gcloud compute instances delete chatbot-vm
```

---

## 🔐 Security Tips

```bash
# Only allow certain IPs
gcloud compute firewall-rules create allow-streamlit \
    --allow=tcp:8501 \
    --source-ranges=YOUR.IP.HERE/32

# Add SSH key
gcloud compute os-login ssh-keys add --key-file=~/.ssh/id_rsa.pub

# View IAM permissions
gcloud projects get-iam-policy PROJECT_ID
```

---

## ✅ Step-by-Step Process

```
1. gcloud compute instances create ... 
        ↓
2. gcloud compute scp (upload files)
        ↓
3. gcloud compute ssh (connect)
        ↓
4. bash setup_gcp.sh (install deps)
        ↓
5. streamlit run ... (start server)
        ↓
6. gcloud compute ... --format (get IP)
        ↓
7. http://<IP>:8501 (access browser)
```

---

## 🆘 Common Issues

| Issue | Fix |
|-------|-----|
| "Connection refused" | Check firewall rule: `gcloud compute firewall-rules list` |
| "Port 8501 not found" | VM might not be running: `gcloud compute instances start chatbot-vm` |
| "Can't SSH" | Enable OS Login or use browser SSH in console |
| "ModuleNotFoundError" | Run: `pip install -r requirements.txt` |
| "Service not starting" | Check: `sudo journalctl -u chatbot -f` |

---

## 📚 Full Docs

For detailed guide: [GCP_DEPLOYMENT.md](./GCP_DEPLOYMENT.md)

---

## 🎯 Next: Advanced Features

After basic setup:

1. **Use OpenAI API** → Edit `~/.streamlit/secrets.toml`
2. **Setup SSL/HTTPS** → Use GCP Load Balancer
3. **Auto-restart on boot** → Run `bash setup_service.sh`
4. **Monitor logs** → `sudo journalctl -u chatbot -f`
5. **Backup data** → `gcloud compute scp --recurse ...`

---

**Ready? 🚀 Follow the "Ultra-Quick Start" above!**

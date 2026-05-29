# 🚀 Deploy Chatbot lên Google Cloud VM

Hướng dẫn chi tiết deploy chatbot RAG lên Google Cloud Compute Engine VM.

---

## ⚡ Quick Deploy (15 phút)

### 1️⃣ Tạo VM trên Google Cloud

```bash
# Trong Cloud Console
gcloud compute instances create chatbot-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --scopes=https://www.googleapis.com/auth/cloud-platform
```

Hoặc dùng UI:
1. GCP Console → Compute Engine → VM Instances
2. Create Instance
   - Name: `chatbot-vm`
   - Machine type: `e2-medium` ($25/tháng)
   - Boot disk: `Debian 11` (30GB)
   - Firewall: ✅ Allow HTTP & HTTPS

### 2️⃣ SSH vào VM

```bash
gcloud compute ssh chatbot-vm --zone=us-central1-a
```

Hoặc dùng UI: Click "SSH" button

### 3️⃣ Setup Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Clone/download chatbot project
cd /home/$(whoami)
git clone <your-repo>  # hoặc upload files
cd chatbot_

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4️⃣ Run Streamlit

```bash
# Chạy trên port 8501
streamlit run chatbot_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501
```

### 5️⃣ Setup Firewall & Access

```bash
# Mở port 8501
gcloud compute firewall-rules create allow-streamlit \
    --allow=tcp:8501 \
    --target-tags=streamlit

# Add tag cho VM
gcloud compute instances add-tags chatbot-vm \
    --tags=streamlit \
    --zone=us-central1-a

# Lấy external IP
gcloud compute instances describe chatbot-vm \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### 6️⃣ Truy cập từ browser

```
http://<EXTERNAL_IP>:8501
```

---

## 📋 Chi tiết từng bước

### Step 1: Tạo Google Cloud Project

```bash
# Set project ID
export PROJECT_ID="my-chatbot-project"

# Create project
gcloud projects create $PROJECT_ID

# Set as active
gcloud config set project $PROJECT_ID

# Enable Compute Engine API
gcloud services enable compute.googleapis.com
```

### Step 2: Tạo VM chi tiết

```bash
gcloud compute instances create chatbot-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium \  # 1 vCPU, 4GB RAM (~$25/tháng)
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --boot-disk-size=30GB \
    --scopes=cloud-platform \
    --metadata=enable-oslogin=TRUE
```

**Machine type options:**
```
e2-small    ($12/tháng, 0.5 vCPU, 2GB) - Slow
e2-medium   ($25/tháng, 1 vCPU, 4GB)   - ⭐ Recommended
e2-standard-2 ($50/tháng, 2 vCPU, 8GB) - Fast
```

### Step 3: Connect SSH

**Option A: gcloud CLI**
```bash
gcloud compute ssh chatbot-vm --zone=us-central1-a
```

**Option B: Browser SSH (GCP Console)**
- Click VM instance
- Click "SSH" button
- Terminal opens in browser

### Step 4: Setup Python Environment

```bash
# SSH vào VM rồi chạy:

# 1. Update packages
sudo apt update
sudo apt upgrade -y

# 2. Install Python
sudo apt install -y python3-pip python3-venv

# 3. Create project directory
mkdir ~/chatbot
cd ~/chatbot

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Upload files (từ local computer)
# gcloud compute scp --recurse ~/chatbot_/* chatbot-vm:~/chatbot/
# Hoặc git clone
```

### Step 5: Install Dependencies

```bash
# Copy requirements.txt đã upload, rồi:
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python3 -c "import streamlit; print('Streamlit OK')"
python3 -c "import chromadb; print('ChromaDB OK')"
```

### Step 6: Configure Streamlit

Tạo file `~/.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501

[browser]
serverAddress = "0.0.0.0"

[logger]
level = "warning"

[client]
showErrorDetails = false
```

Tạo file `~/.streamlit/secrets.toml` (nếu dùng OpenAI):

```toml
openai_api_key = "sk-xxx"
```

### Step 7: Setup Firewall

```bash
# Mở port 8501 cho Streamlit
gcloud compute firewall-rules create allow-streamlit \
    --allow=tcp:8501 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server

# Add tag cho VM
gcloud compute instances add-tags chatbot-vm \
    --tags=http-server \
    --zone=us-central1-a

# Get external IP
gcloud compute instances describe chatbot-vm \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### Step 8: Run Chatbot

```bash
# Activate venv
source ~/chatbot/venv/bin/activate

# Run Streamlit
streamlit run chatbot_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501
```

**Verify:** Output sẽ show:
```
  You can now view your Streamlit app in your browser.

  URL: http://localhost:8501
```

### Step 9: Access từ Browser

```
http://<EXTERNAL_IP>:8501
```

Ví dụ:
```
http://34.125.123.45:8501
```

---

## 🔧 Advanced: Run as Service

### Option A: systemd Service

Tạo file `/etc/systemd/system/chatbot.service`:

```ini
[Unit]
Description=Streamlit Chatbot
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/home/username/chatbot
ExecStart=/home/username/chatbot/venv/bin/streamlit run chatbot_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Chạy service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot
sudo systemctl status chatbot
```

### Option B: nohup (Simple)

```bash
nohup streamlit run chatbot_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 > streamlit.log 2>&1 &
```

### Option C: tmux (Interactive)

```bash
# Install tmux
sudo apt install -y tmux

# Create session
tmux new-session -d -s chatbot -c ~/chatbot

# Run command
tmux send-keys -t chatbot "source venv/bin/activate && streamlit run chatbot_app.py" Enter

# Attach to session
tmux attach -t chatbot

# Detach: Ctrl+B then D
```

---

## 🔐 SSL/TLS (HTTPS)

### Option A: Let's Encrypt + Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure Nginx proxy
# Tạo /etc/nginx/sites-available/chatbot
```

### Option B: GCP Load Balancer

1. GCP Console → Load balancing → Create load balancer
2. Setup SSL certificate
3. Point to VM instance port 8501

---

## 💾 File Upload to VM

### Option 1: gcloud compute scp

```bash
# Copy từ local ke VM
gcloud compute scp ~/chatbot_/requirements.txt \
    chatbot-vm:~/chatbot/

# Copy folder
gcloud compute scp --recurse ~/chatbot_/* \
    chatbot-vm:~/chatbot/
```

### Option 2: Git

```bash
# Trên VM
cd ~/chatbot
git clone https://github.com/yourname/chatbot.git .
```

### Option 3: Cloud Storage

```bash
# Upload ke GCS
gsutil cp -r ~/chatbot_/* gs://my-bucket/chatbot/

# Download trên VM
gsutil cp -r gs://my-bucket/chatbot/* ~/chatbot/
```

---

## 📊 Monitoring & Logs

### Check Status

```bash
# View service status
sudo systemctl status chatbot

# View logs
sudo journalctl -u chatbot -f

# Or check nohup log
tail -f ~/chatbot/streamlit.log
```

### Monitor Resources

```bash
# CPU, RAM, Disk
top

# Disk usage
df -h

# Memory usage
free -h
```

### Streamlit Logs

```bash
# Logs location
cat ~/.streamlit/logs/streamlit.log

# Or tail
tail -f ~/.streamlit/logs/streamlit.log
```

---

## 🛡️ Security Best Practices

### 1. Firewall Rules

```bash
# Restrict IP access (nếu cần)
gcloud compute firewall-rules create allow-streamlit \
    --allow=tcp:8501 \
    --source-ranges=YOUR.IP.HERE/32
```

### 2. VPC Network

```bash
# Tạo VPC private
gcloud compute networks create chatbot-vpc \
    --subnet-mode=custom

# Create VM trong VPC private
# Konfigurasi bastion host cho access
```

### 3. IAM Permissions

```bash
# Create service account
gcloud iam service-accounts create chatbot-sa

# Grant minimal permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=serviceAccount:chatbot-sa@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/viewer
```

### 4. Secrets Management

```bash
# Dùng Secret Manager (bukan plaintext)
gcloud secrets create openai-key \
    --replication-policy="automatic" \
    --data-file=-

# Access in code
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
secret = client.access_secret_version(request=...)
api_key = secret.payload.data.decode('UTF-8')
```

---

## 💰 Cost Estimation

### Monthly Cost

```
e2-medium VM:        $25
Bandwidth (10GB):    $1-2
Storage (30GB):      $1
Total:              ~$27-30/month
```

### Optimize Cost

```bash
# 1. Stop VM khi không dùng
gcloud compute instances stop chatbot-vm

# 2. Dùng e2-small (nếu đủ)
gcloud compute instances create chatbot-vm \
    --machine-type=e2-small

# 3. Schedule auto start/stop
# GCP Console → Compute Engine → Instances → Add schedule
```

---

## 🚀 Deployment Script

Tạo `deploy.sh`:

```bash
#!/bin/bash

set -e

PROJECT_ID="my-chatbot-project"
ZONE="us-central1-a"
VM_NAME="chatbot-vm"

echo "=== Creating VM ==="
gcloud compute instances create $VM_NAME \
    --zone=$ZONE \
    --machine-type=e2-medium \
    --image-family=debian-11 \
    --image-project=debian-cloud

echo "=== Waiting for VM to start ==="
sleep 10

echo "=== Uploading files ==="
gcloud compute scp --recurse . $VM_NAME:~/chatbot/

echo "=== Running setup ==="
gcloud compute ssh $VM_NAME --zone=$ZONE --command='bash ~/chatbot/setup.sh'

echo "=== Getting IP ==="
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME \
    --zone=$ZONE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "✅ Done! Access at: http://$EXTERNAL_IP:8501"
```

Run:
```bash
bash deploy.sh
```

---

## 🔄 Update Code

```bash
# SSH vào VM
gcloud compute ssh chatbot-vm

# Update files
cd ~/chatbot
git pull origin main
# hoặc upload files mới

# Restart service
sudo systemctl restart chatbot
```

---

## 🧹 Cleanup

```bash
# Delete VM
gcloud compute instances delete chatbot-vm --zone=us-central1-a

# Delete firewall rule
gcloud compute firewall-rules delete allow-streamlit

# Delete project (nếu cần)
gcloud projects delete my-chatbot-project
```

---

## 🆘 Troubleshooting

### Lỗi: "Connection refused"
```bash
# Check port
gcloud compute instances describe chatbot-vm \
    --zone=us-central1-a

# Verify firewall
gcloud compute firewall-rules list
```

### Lỗi: "Python module not found"
```bash
# SSH and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Lỗi: "Port already in use"
```bash
# Change port
streamlit run chatbot_app.py --server.port=8502

# Or kill process
lsof -i :8501
kill -9 <PID>
```

### VM connection timeout
```bash
# Check if VM is running
gcloud compute instances list

# Restart VM
gcloud compute instances reset chatbot-vm --zone=us-central1-a
```

---

## 📚 Resources

- [GCP Compute Engine Docs](https://cloud.google.com/compute/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [Streamlit Deployment](https://docs.streamlit.io/library/deploy)
- [GCP Pricing](https://cloud.google.com/pricing/compute)

---

## ✅ Checklist

### Setup:
- [ ] Create GCP project
- [ ] Create VM instance
- [ ] SSH into VM
- [ ] Install Python & dependencies
- [ ] Upload chatbot files
- [ ] Create Streamlit config
- [ ] Configure firewall

### Running:
- [ ] Start Streamlit app
- [ ] Verify access from browser
- [ ] Load knowledge base
- [ ] Test with queries
- [ ] Check logs for errors

### Maintenance:
- [ ] Setup systemd service
- [ ] Monitor resources
- [ ] Update code regularly
- [ ] Backup important data
- [ ] Check security regularly

---

**Ready to deploy on Google Cloud? 🚀**

1. Create GCP project
2. Create VM
3. Run setup script
4. Access your chatbot!

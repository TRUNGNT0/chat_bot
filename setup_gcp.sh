#!/bin/bash

# Google Cloud VM Setup Script for Chatbot
# Run this on Google Cloud VM after SSH

set -e

echo "========================================"
echo "  Chatbot Setup on Google Cloud VM"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# =========================
# 1. UPDATE SYSTEM
# =========================
echo -e "${YELLOW}[1/6] Updating system...${NC}"
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git curl wget

# =========================
# 2. CREATE PROJECT DIRECTORY
# =========================
echo -e "${YELLOW}[2/6] Creating project directory...${NC}"
CHATBOT_DIR="$HOME/chatbot"
mkdir -p $CHATBOT_DIR
cd $CHATBOT_DIR

# =========================
# 3. SETUP PYTHON ENVIRONMENT
# =========================
echo -e "${YELLOW}[3/6] Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# =========================
# 4. DOWNLOAD CHATBOT FILES
# =========================
echo -e "${YELLOW}[4/6] Downloading chatbot files...${NC}"
echo "Option 1: From Git (recommended)"
echo "Option 2: Manual upload"
echo ""
read -p "Do you want to clone from Git? (y/n): " GIT_CHOICE

if [[ $GIT_CHOICE == "y" || $GIT_CHOICE == "Y" ]]; then
    read -p "Enter Git repository URL: " GIT_REPO
    cd /tmp
    git clone $GIT_REPO chatbot_temp
    cp -r chatbot_temp/* $CHATBOT_DIR/
    rm -rf chatbot_temp
    cd $CHATBOT_DIR
    echo -e "${GREEN}✓ Files cloned from Git${NC}"
else
    echo -e "${YELLOW}Please upload files manually using:${NC}"
    echo "gcloud compute scp --recurse ~/chatbot_/* chatbot-vm:~/chatbot/"
    echo ""
    echo "Waiting for files..."
    while [ ! -f "$CHATBOT_DIR/requirements.txt" ]; do
        sleep 5
    done
    echo -e "${GREEN}✓ Files uploaded${NC}"
fi

# =========================
# 5. INSTALL DEPENDENCIES
# =========================
echo -e "${YELLOW}[5/6] Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Verify key packages
python3 -c "import streamlit; print('✓ Streamlit OK')" || echo "WARNING: Streamlit failed"
python3 -c "import chromadb; print('✓ ChromaDB OK')" || echo "WARNING: ChromaDB failed"

# =========================
# 6. SETUP STREAMLIT CONFIG
# =========================
echo -e "${YELLOW}[6/6] Setting up Streamlit configuration...${NC}"

# Create .streamlit directory
mkdir -p ~/.streamlit

# Create config.toml
cat > ~/.streamlit/config.toml << 'EOF'
[server]
headless = true
address = "0.0.0.0"
port = 8501
enableCORS = false

[browser]
serverAddress = "0.0.0.0"

[logger]
level = "warning"

[client]
showErrorDetails = false
toolbarMode = "minimal"
EOF

echo -e "${GREEN}✓ config.toml created${NC}"

# Ask about OpenAI API key
read -p "Do you want to add OpenAI API key? (y/n): " OPENAI_CHOICE
if [[ $OPENAI_CHOICE == "y" || $OPENAI_CHOICE == "Y" ]]; then
    read -sp "Enter OpenAI API key: " OPENAI_KEY
    echo ""
    cat > ~/.streamlit/secrets.toml << EOF
openai_api_key = "$OPENAI_KEY"
EOF
    chmod 600 ~/.streamlit/secrets.toml
    echo -e "${GREEN}✓ secrets.toml created${NC}"
fi

# =========================
# SETUP COMPLETION
# =========================
echo ""
echo "========================================"
echo -e "${GREEN}✅ SETUP COMPLETED${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Streamlit server:"
echo "   cd $CHATBOT_DIR"
echo "   source venv/bin/activate"
echo "   streamlit run chatbot_app.py --server.address=0.0.0.0 --server.port=8501"
echo ""
echo "2. Or setup as systemd service (run setup_service.sh)"
echo ""
echo "3. Get your external IP:"
echo "   gcloud compute instances describe chatbot-vm --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'"
echo ""
echo "4. Access chatbot at: http://<EXTERNAL_IP>:8501"
echo ""
echo "========================================"
echo ""

# Optional: Start Streamlit automatically
read -p "Start Streamlit server now? (y/n): " START_CHOICE
if [[ $START_CHOICE == "y" || $START_CHOICE == "Y" ]]; then
    echo "Starting Streamlit..."
    streamlit run chatbot_app.py --server.address=0.0.0.0 --server.port=8501
fi

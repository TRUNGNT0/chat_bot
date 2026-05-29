#!/bin/bash

# Setup Systemd Service for Chatbot on Google Cloud VM
# Run this to make chatbot auto-start on VM boot

set -e

echo "========================================"
echo "  Setup Chatbot Systemd Service"
echo "========================================"
echo ""

CHATBOT_DIR="$HOME/chatbot"
USERNAME=$(whoami)

# Check if chatbot directory exists
if [ ! -d "$CHATBOT_DIR" ]; then
    echo "❌ Error: Chatbot directory not found at $CHATBOT_DIR"
    echo "Please run setup_gcp.sh first"
    exit 1
fi

# Create systemd service file
echo "Creating systemd service file..."

sudo tee /etc/systemd/system/chatbot.service > /dev/null << EOF
[Unit]
Description=Streamlit Chatbot RAG
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$CHATBOT_DIR
Environment="PATH=$CHATBOT_DIR/venv/bin"
ExecStart=$CHATBOT_DIR/venv/bin/streamlit run chatbot_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --logger.level=warning

Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=chatbot

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Service file created at /etc/systemd/system/chatbot.service"
echo ""

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable service to start on boot
echo "Enabling service to start on boot..."
sudo systemctl enable chatbot

# Ask if user wants to start now
read -p "Start chatbot service now? (y/n): " START_CHOICE
if [[ $START_CHOICE == "y" || $START_CHOICE == "Y" ]]; then
    echo "Starting chatbot service..."
    sudo systemctl start chatbot
    sleep 2
    
    # Show status
    echo ""
    echo "Service status:"
    sudo systemctl status chatbot --no-pager
fi

echo ""
echo "========================================"
echo "✅ Service setup complete!"
echo "========================================"
echo ""
echo "Commands:"
echo "  Start:   sudo systemctl start chatbot"
echo "  Stop:    sudo systemctl stop chatbot"
echo "  Status:  sudo systemctl status chatbot"
echo "  Logs:    sudo journalctl -u chatbot -f"
echo "  Disable: sudo systemctl disable chatbot"
echo ""

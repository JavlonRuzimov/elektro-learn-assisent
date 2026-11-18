#!/bin/bash
# ElektroLearn systemd Service Installer for AWS Ubuntu EC2

echo "[*] ElektroLearn systemd servisi o'rnatilmoqda..."

# 1. Eski fon jarayonlarini to'xtatish
pkill -f telegram_bot.py 2>/dev/null

# 2. Servis faylini yaratish
sudo tee /etc/systemd/system/elektrolearn.service > /dev/null << 'EOF'
[Unit]
Description=ElektroLearn 24/7 Telegram Automation Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ElektroLearn
ExecStart=/home/ubuntu/ElektroLearn/venv/bin/python -u telegram_bot.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/ElektroLearn/bot.log
StandardError=append:/home/ubuntu/ElektroLearn/bot.log

[Install]
WantedBy=multi-user.target
EOF

# 3. Systemd ni qayta yuklash va servisni yoqish
sudo systemctl daemon-reload
sudo systemctl enable elektrolearn
sudo systemctl restart elektrolearn

echo "[+] Servis muvaffaqiyatli ishga tushirildi!"
sudo systemctl status elektrolearn --no-pager

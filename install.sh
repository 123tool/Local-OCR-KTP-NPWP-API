#!/bin/bash

# Warna
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

clear
echo -e "${BLUE}==============================================${NC}"
echo -e "         SPY-E OCR AUTO-INSTALLER 2026        "
echo -e "${BLUE}==============================================${NC}"

# Cek Platform
if [ -d "/data/data/com.termux" ]; then
    echo -e "[*] Mendeteksi Lingkungan: Termux"
    pkg update -y && pkg upgrade -y
    pkg install python clang python-pillow libjpeg-turbo fftw libiconv -y
else
    echo -e "[*] Mendeteksi Lingkungan: Linux/PC"
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
fi

# Instalasi Library Python
echo -e "[*] Menginstall Library (Flask, EasyOCR, Werkzeug)..."
pip install --upgrade pip
pip install flask easyocr werkzeug opencv-python-headless

# Buat Folder
echo -e "[*] Menyiapkan struktur folder..."
mkdir -p templates uploads

echo -e "${GREEN}==============================================${NC}"
echo -e "   INSTALASI SELESAI! SILAKAN JALANKAN:      "
echo -e "   python app.py                             "
echo -e "${GREEN}==============================================${NC}"

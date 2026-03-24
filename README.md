# 🚀 SPY-E IDENTITY OCR

Sistem ekstraksi data NIK KTP dan Nomor NPWP Indonesia berbasis AI (EasyOCR) yang berjalan sepenuhnya secara lokal tanpa memerlukan API Google Cloud.

## 🌟 Fitur Utama
- **Gratis Selamanya**: Tidak ada tagihan bulanan Google Cloud.
- **Offline Mode**: Data diproses di mesin lokal, lebih aman & privat.
- **Modern Dashboard**: UI futuristik berbasis Tailwind CSS.
- **Multi-Platform**: Jalan di Windows, Linux, dan Termux (Android).

## 🛠️ Instalasi

### 1. Via Termux (Android)
```bash
pkg install git -y
git clone [https://github.com/123tool/Local-OCR-KTP-NPWP-API.git]
cd spy-e-ocr
chmod +x install.sh
./install.sh
python app.py

```
### 2. Via Windows (CMD/PowerShell)
​Install Python 3.10+
​Jalankan perintah:
```bash
pip install flask easyocr werkzeug opencv-python-headless
python app.py

```
### 📖 Cara Penggunaan
​Jalankan python app.py.
​Buka browser dan akses http://localhost:5000.
​Pilih tipe dokumen (KTP/NPWP).
​Upload foto dokumen (pastikan cahaya cukup & tulisan terbaca).
​Klik Mulai Ekstraksi.


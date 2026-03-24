import os
import re
import easyocr
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Inisialisasi Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Maksimal 10MB

# Setup Logging agar mudah tracing error
logging.basicConfig(level=logging.INFO)

# Buat folder pendukung jika belum ada
for folder in [app.config['UPLOAD_FOLDER'], 'templates']:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Load Model AI (Indonesia & English) - Proses ini makan RAM sekitar 500MB-1GB
print("--- [SPY-E SYSTEM] Memuat Model AI OCR... Mohon Tunggu ---")
try:
    reader = easyocr.Reader(['id', 'en'], gpu=False) # Set gpu=True jika pakai PC dengan NVIDIA
    print("--- [SPY-E SYSTEM] Model Berhasil Dimuat! ---")
except Exception as e:
    print(f"Gagal memuat model: {e}")

# --- ROUTES ---

@app.route('/')
def index():
    """Menampilkan Dashboard Utama"""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_data():
    """Endpoint API untuk memproses Gambar"""
    if 'file' not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400
    
    file = request.files['file']
    type_photo = request.args.get('type', 'ktp').lower()
    
    if file.filename == '':
        return jsonify({"error": "Nama file tidak valid"}), 400

    # Simpan file secara aman
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    try:
        # Jalankan Proses OCR
        logging.info(f"Memproses {type_photo}: {filename}")
        results = reader.readtext(path, detail=0)
        
        # Inisialisasi Data Output
        extracted_id = "Tidak Terdeteksi"
        raw_text = " ".join(results).upper()

        # Logika Pencarian NIK/NPWP menggunakan REGEX
        if type_photo == 'ktp':
            # Mencari angka 16 digit (NIK KTP Indonesia)
            match = re.search(r'\d{16}', raw_text.replace(" ", ""))
            if match:
                extracted_id = match.group(0)
        else:
            # Mencari format standar NPWP (15-16 digit dengan titik/strip)
            # Contoh: 12.345.678.9-012.345 atau deretan angka panjang
            match = re.search(r'\d{2,3}[\.\s]?\d{3}[\.\s]?\d{3}[\.\s]?\d{1}[\-\.\s]?\d{3}[\.\s]?\d{3}', raw_text)
            if match:
                extracted_id = match.group(0)
            else:
                # Fallback: cari deretan angka minimal 15 digit
                match_fallback = re.search(r'\d{15,16}', raw_text.replace(".", "").replace("-", "").replace(" ", ""))
                if match_fallback:
                    extracted_id = match_fallback.group(0)

        return jsonify({
            "status": "success",
            "branding": "SPY-E OCR Engine",
            "type": type_photo.upper(),
            "detected_id": extracted_id,
            "full_results": results
        })

    except Exception as e:
        logging.error(f"Error saat OCR: {str(e)}")
        return jsonify({"error": "Gagal memproses gambar"}), 500
    finally:
        # Hapus file setelah diproses agar storage tidak penuh
        if os.path.exists(path):
            os.remove(path)

if __name__ == '__main__':
    # Jalankan server (host 0.0.0.0 agar bisa diakses dari HP lain dalam 1 WiFi)
    app.run(host='0.0.0.0', port=5000, debug=False)

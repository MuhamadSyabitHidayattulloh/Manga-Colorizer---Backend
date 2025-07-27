# Manga Colorizer - Backend API

API backend untuk aplikasi Manga Colorizer yang menangani proses pewarnaan gambar menggunakan model AI dari Hugging Face.

## 🚀 Fitur Utama

- **Image Colorization**: Menggunakan model AI untuk mewarnai gambar manga grayscale.
- **Batch Processing**: Mendukung pewarnaan multiple gambar sekaligus.
- **Fallback Mechanism**: Menyediakan fallback jika model AI tidak tersedia.
- **RESTful API**: Menyediakan endpoint API yang mudah digunakan.

## 🛠️ Teknologi yang Digunakan

- **Flask**: Framework web Python.
- **Flask-CORS**: Untuk mengelola Cross-Origin Resource Sharing.
- **Pillow (PIL)**: Library pemrosesan gambar.
- **NumPy**: Untuk operasi numerik.
- **Requests**: Untuk melakukan HTTP requests ke Hugging Face API.
- **python-dotenv**: Untuk mengelola environment variables.

## 📁 Struktur Proyek

```
manga-colorizer-backend/
├── app.py                # Server Flask utama
├── requirements.txt      # Dependencies Python
├── .env.example          # Contoh file environment variables
├── .gitignore            # File yang diabaikan oleh Git
├── uploads/              # Folder untuk file upload sementara
└── results/              # Folder untuk hasil pewarnaan
```

## 🔧 Instalasi dan Setup

### Prerequisites
- Python 3.11+
- pip (Python package installer)

### Setup

1. **Clone repository dan masuk ke direktori proyek**
   ```bash
   git clone https://github.com/MuhamadSyabitHidayattulloh/Manga-Colorizer---Backend.git
   cd Manga-Colorizer---Backend
   ```

2. **Buat virtual environment (opsional, tapi direkomendasikan)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies Python**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment Variables**
   Buat file `.env` di root direktori proyek (`manga-colorizer-backend/`) dan tambahkan baris berikut:
   ```env
   HUGGING_FACE_TOKEN=your_hugging_face_token_here
   MODEL_URL=https://api-inference.huggingface.co/models/Keiser41/Example_Based_Manga_Colorization
   ```
   Ganti `your_hugging_face_token_here` dengan token Hugging Face Anda.

5. **Jalankan server Flask**
   ```bash
   python3 app.py
   ```
   Server akan berjalan di `http://localhost:5000`.

## 🔌 API Endpoints

### Health Check
`GET /health`

Mengecek status kesehatan API.

### Colorize Single Image
`POST /colorize`

Parameters:
- `image`: File gambar yang akan diwarnai (multipart/form-data)
- `reference`: (Optional) File gambar referensi untuk pewarnaan (multipart/form-data)

### Colorize Batch Images
`POST /colorize_batch`

Parameters:
- `images`: Multiple file gambar yang akan diwarnai (multipart/form-data)
- `reference`: (Optional) File gambar referensi untuk pewarnaan (multipart/form-data)

### Download Result
`GET /download/<filename>`

Mengunduh file hasil pewarnaan.

### Get Available Models
`GET /models`

Mendapatkan daftar model AI yang tersedia.

## 🤖 Model AI

API ini menggunakan model **Keiser41/Example_Based_Manga_Colorization** dari Hugging Face.

## 🧪 Testing

Gunakan tools seperti Postman atau `curl` untuk menguji API endpoints:

```bash
# Health check
curl http://localhost:5000/health

# Test colorize endpoint (ganti path/to/your/image.jpg dengan path gambar Anda)
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/colorize
```

## 🐛 Troubleshooting

- **Backend tidak dapat diakses**: Pastikan Flask server berjalan di port 5000, periksa pengaturan firewall, dan pastikan CORS dikonfigurasi dengan benar.
- **Model Hugging Face timeout**: Model mungkin sedang "cold start". Tunggu beberapa menit dan coba lagi. Periksa status API Hugging Face.
- **File upload gagal**: Periksa ukuran file (maksimal yang didukung), pastikan format file didukung, dan periksa permissions folder `uploads`.

## 🤝 Contributing

Kontribusi sangat dihargai! Silakan fork repository, buat branch baru, lakukan perubahan, dan ajukan pull request.

## 📄 License

Distributed under the MIT License. Lihat `LICENSE` untuk informasi lebih lanjut.

## 👥 Authors

- **Developer**: Muhamad Syabit Hidayattulloh

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) untuk platform AI model
- [Flask](https://flask.palletsprojects.com/) untuk backend framework
- Komunitas open source untuk berbagai library yang digunakan



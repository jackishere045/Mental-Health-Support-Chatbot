# Mental Health Support Chatbot

Proyek ini adalah chatbot pendukung kesehatan mental yang dibangun menggunakan [Streamlit](https://streamlit.io/) dan model GPT-3.5-turbo dari [OpenAI](https://platform.openai.com/docs/models/gpt-3-5-turbo). Chatbot ini menyediakan dukungan kesehatan mental lewat antarmuka percakapan, dengan fitur analisis sentimen, pelacakan suasana hati, dan strategi coping yang dipersonalisasi berdasarkan input pengguna.

# Preview
[Demo](https://mental-health-support-chatbot-by-jackdev.streamlit.app/)
![Preview](https://drive.google.com/uc?export=view&id=1y0ArME4ffBShwEYJyIUsMZWYXKlPaRpu)

## Fitur

- **Antarmuka Chat**: Berinteraksi dengan chatbot dalam antarmuka percakapan yang mudah digunakan.
- **Analisis Sentimen**: Menganalisis sentimen pesan pengguna dan mengkategorikannya ke dalam emosi yang berbeda.
- **Pelacakan Suasana Hati**: Melacak suasana hati pengguna dari waktu ke waktu berdasarkan pesan mereka.
- **Strategi Coping**: Memberikan strategi coping yang dipersonalisasi sesuai kondisi emosional pengguna.
- **Ringkasan Sesi**: Menyediakan ringkasan percakapan dan wawasan di akhir setiap sesi.
- **Sumber Bantuan**: Menyediakan tautan ke sumber daya bantuan kesehatan mental yang dapat diakses segera.

## Instalasi

1. **Clone repository:**
    ```bash
    git clone https://github.com/jackdev/Mental-Health-Support-Chatbot.git
    cd Mental-Health-Support-Chatbot
    ```

2. **Buat virtual environment dan aktifkan:**
    ```bash
    python -m venv env
    .\env\Scripts\activate   # Windows
    source env/bin/activate  # Mac/Linux
    ```

3. **Install paket yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Atur API key AI kamu:**
    - Dapatkan API key dari API platform milikmu.
    - Simpan API key di environment variable `"platform"_API_KEY` atau ganti `'your_"platform"_api_key'` di kode dengan API key-mu.

## Cara Menjalankan

1. Jalankan aplikasi Streamlit:
    ```bash
    streamlit run app.py
    ```

2. Buka URL yang muncul (biasanya http://localhost:8501) di browser.

3. Mulai berinteraksi dengan chatbot:
    - Ketik pesanmu di kolom input dan tekan "Send".
    - Chatbot akan merespon, menganalisis sentimen, melacak suasana hati, dan memberikan strategi coping yang sesuai.

## Struktur Proyek

- `app.py` : File utama aplikasi berisi kode Streamlit dan logika chatbot.
- `requirements.txt` : Daftar paket Python yang diperlukan.

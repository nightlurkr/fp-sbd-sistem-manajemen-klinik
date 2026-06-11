# Sistem Manajemen Klinik

Final Project Sistem Basis Data — Institut Teknologi Sepuluh Nopember

## Teknologi
- Python (FastAPI)
- MySQL
- MongoDB

## Cara Menjalankan

### 1. Clone repository
git clone https://github.com/nightlurkr/fp-sbd-sistem-manajemen-klinik.git
cd fp-sbd-sistem-manajemen-klinik

### 2. Install dependencies
pip install fastapi uvicorn sqlalchemy pymysql pymongo python-dotenv

### 3. Setup MySQL
- Buat database di phpMyAdmin atau MySQL
- Jalankan file `database.sql` untuk membuat semua tabel

### 4. Setup MongoDB
- Pastikan MongoDB sudah berjalan di localhost:27017

### 5. Buat file .env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=klinik_db
MONGO_URI=mongodb://localhost:27017
MONGO_DB=klinik_db

### 6. Jalankan server
python -m uvicorn main:app --reload

### 7. Buka Swagger UI
http://localhost:8000/docs

## Struktur Database

### MySQL (Relational)
Menyimpan data terstruktur yang saling berelasi:
- Pasien, Dokter, Poli, Staff
- Jadwal_Praktik, Antrian, Kunjungan
- Obat, Resep, Detail_Resep
- Tagihan, Pembayaran

### MongoDB (Non-Relational)
Menyimpan data fleksibel yang strukturnya berbeda tiap dokumen:
- `rekam_medis` — diagnosis, tindakan, hasil lab per kunjungan
- `info_obat` — deskripsi, efek samping, kontraindikasi obat

## Endpoints
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /pasien/ | Lihat semua pasien |
| POST | /pasien/ | Tambah pasien baru |
| GET | /pasien/{id} | Lihat detail pasien |
| GET | /dokter/ | Lihat semua dokter |
| GET | /antrian/{id_jadwal} | Lihat antrian per jadwal |
| POST | /antrian/ | Tambah antrian |
| PUT | /antrian/{id}/status | Update status antrian |
| GET | /kunjungan/ | Lihat semua kunjungan |
| POST | /kunjungan/ | Tambah kunjungan |
| GET | /rekam-medis/{id_pasien} | Lihat rekam medis pasien |
| POST | /rekam-medis/ | Tambah rekam medis |
| GET | /tagihan/ | Lihat semua tagihan |
| POST | /tagihan/ | Buat tagihan baru |
| PUT | /tagihan/{id}/bayar | Proses pembayaran |
| GET | /obat/ | Lihat semua obat |
| GET | /obat/stok-menipis | Lihat obat stok menipis |
| PUT | /obat/{id}/stok | Update stok obat |

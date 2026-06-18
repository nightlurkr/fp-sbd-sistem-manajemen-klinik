# Sistem Manajemen Klinik

Final Project Sistem Basis Data (SBD) - Kelas A
Institut Teknologi Sepuluh Nopember (ITS) Surabaya, 2026

## Anggota Kelompok

| NRP | Nama |
|-----|------|
| 5027231046 | Ryan Adya Purwanto |
| 5027231067 | Muhammad Yusuf |

## Deskripsi Project

Sistem Manajemen Klinik adalah aplikasi backend berbasis REST API untuk mengelola operasional klinik, meliputi pendaftaran pasien, penjadwalan dokter, antrian, kunjungan, rekam medis, resep obat, tagihan, dan pembayaran. Sistem ini mengintegrasikan MySQL (relational database) dan MongoDB (non-relational database) sesuai kebutuhan penyimpanan data.

## Identifikasi Masalah

Klinik membutuhkan sistem terintegrasi untuk mengelola:
- Data master (poli, dokter, staff, pasien, obat)
- Operasional harian (antrian, kunjungan, resep, tagihan, pembayaran)
- Rekam medis pasien yang bersifat semi-structured (diagnosis, tindakan, hasil lab, foto)
- Informasi obat yang bersifat deskriptif dan bervariasi antar obat

## Tech Stack

- Backend: Python 3.13, FastAPI, Uvicorn
- Relational DB: MySQL via SQLAlchemy + PyMySQL
- Non-Relational DB: MongoDB via PyMongo
- Tools: phpMyAdmin (XAMPP), MongoDB Compass

## Desain Database

### MySQL - Relational Database (12 Tabel)

Data yang disimpan di MySQL adalah data terstruktur dengan relasi antar entitas yang jelas dan memerlukan integritas referensial (foreign key).

Urutan FK (parent ke child):

```
Poli -> Dokter -> Jadwal_Praktik
                -> Kunjungan -> Resep -> Detail_Resep
                             -> Tagihan -> Pembayaran
Pasien -> Antrian, Kunjungan
Staff -> Antrian, Pembayaran
Obat -> Detail_Resep
```

Tabel dan Atribut:

| No | Tabel | Primary Key | Foreign Key | Keterangan |
|----|-------|-------------|-------------|------------|
| 1 | Poli | ID_Poli | - | Data poliklinik |
| 2 | Dokter | ID_Dokter | ID_Poli -> Poli | Data dokter per poli |
| 3 | Staff | ID_Staff | - | Resepsionis, kasir |
| 4 | Pasien | ID_Pasien | - | Data pasien |
| 5 | Jadwal_Praktik | ID_Jadwal | ID_Dokter -> Dokter, ID_Poli -> Poli | Jadwal per hari + kuota |
| 6 | Antrian | ID_Antrian | ID_Pasien -> Pasien, ID_Jadwal -> Jadwal_Praktik, ID_Staff -> Staff | Antrian harian |
| 7 | Kunjungan | ID_Kunjungan | ID_Pasien -> Pasien, ID_Dokter -> Dokter | Catatan kunjungan |
| 8 | Obat | ID_Obat | - | Stok dan harga obat |
| 9 | Resep | ID_Resep | ID_Kunjungan -> Kunjungan, ID_Dokter -> Dokter | Header resep |
| 10 | Detail_Resep | ID_Detail | ID_Resep -> Resep, ID_Obat -> Obat | Detail obat per resep |
| 11 | Tagihan | ID_Tagihan | ID_Kunjungan -> Kunjungan | Tagihan per kunjungan |
| 12 | Pembayaran | ID_Pembayaran | ID_Tagihan -> Tagihan (UNIQUE), ID_Staff -> Staff | One-to-one dengan Tagihan |

### MongoDB - Non-Relational Database (2 Collection)

Data yang disimpan di MongoDB bersifat semi-structured, selalu dibaca bersama dokumen induknya, dan tidak memerlukan JOIN dengan tabel lain.

Alasan penggunaan MongoDB:
- rekam_medis: Diagnosis, tindakan, dan hasil lab bersifat variabel (jumlah dan isi berbeda tiap kunjungan). Hasil lab bisa berupa nested object. Foto disimpan sebagai array URL. Data ini selalu dibaca sebagai satu kesatuan per kunjungan.
- info_obat: Efek samping, kontraindikasi, dan interaksi obat berupa array string yang bervariasi panjangnya tiap obat. Data ini bersifat deskriptif dan selalu diakses bersama.

Keputusan Embedding vs Referencing:
Kedua collection menggunakan embedding karena data selalu dibaca bersama dokumen induknya dan tidak di-query secara independen.

Struktur Collection rekam_medis:
```json
{
  "id_kunjungan": "KNJ001",
  "id_pasien": "PSN001",
  "id_dokter": "DOK001",
  "tanggal": "2026-06-10",
  "keluhan": "Demam tinggi sejak 3 hari",
  "diagnosis": ["Demam dengue", "Dehidrasi ringan"],
  "tindakan": ["Infus NaCl", "Pemberian antipiretik"],
  "catatan_dokter": "Pasien perlu istirahat total 5 hari",
  "hasil_lab": {
    "hemoglobin": "13.5",
    "trombosit": "95000",
    "leukosit": "4500"
  },
  "foto": []
}
```

Struktur Collection info_obat:
```json
{
  "id_obat": "OBT001",
  "nama": "Amoxicillin 500mg",
  "deskripsi": "Antibiotik golongan penisilin",
  "efek_samping": ["Mual", "Diare", "Ruam kulit"],
  "kontraindikasi": ["Alergi penisilin"],
  "interaksi_obat": ["Methotrexate", "Warfarin"],
  "cara_penyimpanan": "Simpan di tempat kering, suhu ruangan"
}
```

## Cara Menjalankan

```bash
# 1. Pastikan MySQL (XAMPP) dan MongoDB sudah running
# 2. Import database MySQL
mysql -u root < database.sql

# 3. Jalankan server
cd klinik-api
pip install fastapi uvicorn sqlalchemy pymysql pymongo python-dotenv
python -m uvicorn main:app --reload

# 4. Akses Swagger UI
# http://localhost:8000/docs
```

## Daftar Endpoint

### Poli
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /poli/ | Semua poli |
| GET | /poli/{id} | Detail poli |
| POST | /poli/ | Tambah poli |
| PUT | /poli/{id} | Update poli |
| DELETE | /poli/{id} | Hapus poli |

### Dokter
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /dokter/ | Semua dokter |
| GET | /dokter/{id} | Detail dokter |
| POST | /dokter/ | Tambah dokter |
| PUT | /dokter/{id} | Update dokter |
| DELETE | /dokter/{id} | Hapus dokter |

### Staff
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /staff/ | Semua staff |
| GET | /staff/{id} | Detail staff |
| POST | /staff/ | Tambah staff |
| PUT | /staff/{id} | Update staff |
| DELETE | /staff/{id} | Hapus staff |

### Jadwal Praktik
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /jadwal/ | Semua jadwal |
| GET | /jadwal/{id} | Detail jadwal |
| POST | /jadwal/ | Tambah jadwal |
| PUT | /jadwal/{id} | Update jadwal |
| DELETE | /jadwal/{id} | Hapus jadwal |

### Pasien
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /pasien/ | Semua pasien |
| GET | /pasien/{id} | Detail pasien |
| POST | /pasien/ | Tambah pasien |
| PUT | /pasien/{id} | Update pasien |
| DELETE | /pasien/{id} | Hapus pasien |

### Antrian
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /antrian/ | Semua antrian |
| GET | /antrian/{id_jadwal} | Antrian per jadwal hari ini |
| POST | /antrian/ | Daftar antrian (validasi kuota + auto nomor) |
| PUT | /antrian/{id}/panggil | Panggil pasien, status dalam_proses |
| PUT | /antrian/{id}/batal | Batalkan antrian |

### Kunjungan
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /kunjungan/ | Semua kunjungan |
| GET | /kunjungan/{id_pasien} | Kunjungan per pasien |
| POST | /kunjungan/dari-antrian/{id_antrian} | Buat kunjungan dari antrian |
| PUT | /kunjungan/{id}/selesai | Selesaikan kunjungan + tagihan otomatis |

### Rekam Medis (MongoDB)
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /rekam-medis/{id_pasien} | Rekam medis per pasien |
| GET | /rekam-medis/kunjungan/{id_kunjungan} | Rekam medis per kunjungan |
| POST | /rekam-medis/ | Simpan rekam medis |
| PUT | /rekam-medis/{id_kunjungan} | Update rekam medis |
| DELETE | /rekam-medis/{id_kunjungan} | Hapus rekam medis |

### Tagihan dan Pembayaran
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /tagihan/ | Semua tagihan |
| GET | /tagihan/{id_kunjungan} | Tagihan per kunjungan |
| POST | /tagihan/ | Buat tagihan manual |
| PUT | /tagihan/{id}/bayar | Proses pembayaran + update status lunas |

### Obat
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /obat/ | Semua obat |
| GET | /obat/stok-menipis | Obat dengan stok <= stok_minimum |
| GET | /obat/{id} | Detail obat |
| POST | /obat/ | Tambah obat |
| PUT | /obat/{id} | Update data obat |
| PUT | /obat/{id}/stok | Update stok obat |
| DELETE | /obat/{id} | Hapus obat |

### Resep
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /resep/{id_kunjungan} | Resep + detail obat per kunjungan |
| POST | /resep/ | Buat resep (cek stok + expired + kurangi stok otomatis) |

### Info Obat (MongoDB)
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /info-obat/ | Semua info obat |
| GET | /info-obat/{id_obat} | Info obat per ID |
| POST | /info-obat/ | Tambah info obat |
| PUT | /info-obat/{id_obat} | Update info obat |
| DELETE | /info-obat/{id_obat} | Hapus info obat |

## Business Logic

1. Validasi kuota antrian - Cek jumlah antrian aktif hari ini >= kuota jadwal maka tolak pendaftaran
2. Auto-generate nomor antrian - Hitung antrian aktif + 1
3. Kunjungan otomatis dari antrian - Ambil ID_Dokter dari Jadwal_Praktik, buat kunjungan, update status antrian ke selesai
4. Tagihan otomatis - Saat kunjungan diselesaikan, tagihan otomatis terbuat
5. Cek stok obat - Sebelum resep dibuat, validasi stok mencukupi
6. Cek expired obat - Obat kadaluarsa tidak bisa diresepkan
7. Auto-pengurangan stok - Stok berkurang otomatis saat resep dibuat
8. Stok menipis - Endpoint filter obat dengan stok <= stok_minimum

## Alur Sistem

GET /pasien/
```
SELECT * FROM Pasien;
```

POST /pasien/
```
INSERT INTO Pasien (ID_Pasien, nama, tanggal_lahir, ...) 
VALUES ('PSN001', 'Budi', '2000-01-01', ...);
```

POST /antrian/ dengan kuota penuh
```
-- Cek dulu berapa antrian di jadwal itu
SELECT COUNT(*) FROM Antrian WHERE ID_Jadwal = 'JDW001';
-- Cek kuota_maks dari jadwal
SELECT kuota_maks FROM Jadwal WHERE ID_Jadwal = 'JDW001';
```

GET /obat/stok-menipis
```
SELECT * FROM Obat WHERE stok <= stok_minimum;
```

POST /resep/ dengan obat expired
```
-- Cek expired_date obat dulu
SELECT expired_date FROM Obat WHERE ID_Obat = 'OBT001';
-- Kalau expired_date < hari ini → return HTTP 400, tidak ada INSERT
```

POST /rekam-medis/
```
js// MongoDB
db.rekam_medis.insert_one({ id_kunjungan: "KNJ001", ... })
```

POST /info-obat/
```
js// MongoDB
db.info_obat.insert_one({ id_obat: "OBT001", ... })
```

PUT /tagihan/{id}/bayar
```
-- Update status tagihan
UPDATE Tagihan SET status_bayar = 'lunas' WHERE ID_Tagihan = 'TAG001';
-- Insert pembayaran baru
INSERT INTO Pembayaran (ID_Pembayaran, ID_Tagihan, tanggal_bayar, metode_bayar)
VALUES ('PAY001', 'TAG001', '2026-06-18', 'tunai');

```

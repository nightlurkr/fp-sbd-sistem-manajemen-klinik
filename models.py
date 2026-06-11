from sqlalchemy import Column, String, Integer, Date, Time, Text, DECIMAL, Enum
from database import Base

class Poli(Base):
    __tablename__ = "Poli"
    ID_Poli    = Column(String(10), primary_key=True)
    nama_poli  = Column(String(50), nullable=False)
    no_ruangan = Column(String(10))
    status     = Column(Enum('aktif', 'tidak_aktif'), default='aktif')

class Dokter(Base):
    __tablename__ = "Dokter"
    ID_Dokter    = Column(String(10), primary_key=True)
    ID_Poli      = Column(String(10), nullable=False)
    nama         = Column(String(100), nullable=False)
    spesialisasi = Column(String(50))
    no_lisensi   = Column(String(20), nullable=False)
    no_telepon   = Column(String(20))

class Pasien(Base):
    __tablename__ = "Pasien"
    ID_Pasien      = Column(String(10), primary_key=True)
    nama           = Column(String(100), nullable=False)
    tanggal_lahir  = Column(Date, nullable=False)
    jenis_kelamin  = Column(Enum('L', 'P'), nullable=False)
    no_telepon     = Column(String(20))
    alamat         = Column(Text)
    golongan_darah = Column(Enum('A', 'B', 'AB', 'O'))

class Staff(Base):
    __tablename__ = "Staff"
    ID_Staff  = Column(String(10), primary_key=True)
    nama      = Column(String(100), nullable=False)
    jabatan   = Column(String(50))
    username  = Column(String(50), nullable=False, unique=True)
    password  = Column(String(255), nullable=False)

class Jadwal_Praktik(Base):
    __tablename__ = "Jadwal_Praktik"
    ID_Jadwal   = Column(String(10), primary_key=True)
    ID_Dokter   = Column(String(10), nullable=False)
    ID_Poli     = Column(String(10), nullable=False)
    hari        = Column(Enum('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu'), nullable=False)
    jam_mulai   = Column(Time, nullable=False)
    jam_selesai = Column(Time, nullable=False)
    kuota       = Column(Integer, default=20)

class Antrian(Base):
    __tablename__ = "Antrian"
    ID_Antrian = Column(String(10), primary_key=True)
    ID_Pasien  = Column(String(10), nullable=False)
    ID_Jadwal  = Column(String(10), nullable=False)
    ID_Staff   = Column(String(10))
    no_antrian = Column(Integer, nullable=False)
    status     = Column(Enum('menunggu','dalam_proses','selesai','batal'), default='menunggu')
    tanggal    = Column(Date, nullable=False)

class Kunjungan(Base):
    __tablename__ = "Kunjungan"
    ID_Kunjungan = Column(String(10), primary_key=True)
    ID_Pasien    = Column(String(10), nullable=False)
    ID_Dokter    = Column(String(10), nullable=False)
    tanggal      = Column(Date, nullable=False)
    keluhan      = Column(Text)
    status       = Column(Enum('berlangsung','selesai'), default='berlangsung')

class Obat(Base):
    __tablename__ = "Obat"
    ID_Obat           = Column(String(10), primary_key=True)
    nama              = Column(String(100), nullable=False)
    satuan            = Column(String(20), nullable=False)
    harga             = Column(DECIMAL(10,2), nullable=False)
    stok              = Column(Integer, default=0)
    stok_minimum      = Column(Integer, default=10)
    manufactured_date = Column(Date)
    expired_date      = Column(Date)

class Resep(Base):
    __tablename__ = "Resep"
    ID_Resep     = Column(String(10), primary_key=True)
    ID_Kunjungan = Column(String(10), nullable=False)
    ID_Dokter    = Column(String(10), nullable=False)
    tanggal      = Column(Date, nullable=False)

class Detail_Resep(Base):
    __tablename__ = "Detail_Resep"
    ID_Detail    = Column(String(10), primary_key=True)
    ID_Resep     = Column(String(10), nullable=False)
    ID_Obat      = Column(String(10), nullable=False)
    jumlah       = Column(Integer, nullable=False)
    dosis        = Column(String(50))
    aturan_pakai = Column(String(100))

class Tagihan(Base):
    __tablename__ = "Tagihan"
    ID_Tagihan   = Column(String(10), primary_key=True)
    ID_Kunjungan = Column(String(10), nullable=False)
    total        = Column(DECIMAL(10,2), nullable=False)
    status_bayar = Column(Enum('belum_bayar','lunas'), default='belum_bayar')
    tanggal      = Column(Date, nullable=False)

class Pembayaran(Base):
    __tablename__ = "Pembayaran"
    ID_Pembayaran = Column(String(10), primary_key=True)
    ID_Tagihan    = Column(String(10), nullable=False, unique=True)
    ID_Staff      = Column(String(10))
    jumlah        = Column(DECIMAL(10,2), nullable=False)
    metode        = Column(Enum('tunai','transfer','BPJS','kartu_debit'), nullable=False)
    tanggal       = Column(Date, nullable=False)
CREATE DATABASE IF NOT EXISTS klinik_db;
USE klinik_db;

CREATE TABLE Poli (
    ID_Poli     VARCHAR(10)  NOT NULL,
    nama_poli   VARCHAR(50)  NOT NULL,
    no_ruangan  VARCHAR(10),
    status      ENUM('aktif', 'tidak_aktif') NOT NULL DEFAULT 'aktif',
    PRIMARY KEY (ID_Poli)
);

CREATE TABLE Dokter (
    ID_Dokter    VARCHAR(10)  NOT NULL,
    ID_Poli      VARCHAR(10)  NOT NULL,
    nama         VARCHAR(100) NOT NULL,
    spesialisasi VARCHAR(50),
    no_lisensi   VARCHAR(20)  NOT NULL,
    no_telepon   VARCHAR(20),
    PRIMARY KEY (ID_Dokter),
    FOREIGN KEY (ID_Poli) REFERENCES Poli(ID_Poli)
);

CREATE TABLE Jadwal_Praktik (
    ID_Jadwal   VARCHAR(10)  NOT NULL,
    ID_Dokter   VARCHAR(10)  NOT NULL,
    ID_Poli     VARCHAR(10)  NOT NULL,
    hari        ENUM('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu') NOT NULL,
    jam_mulai   TIME         NOT NULL,
    jam_selesai TIME         NOT NULL,
    kuota       INT          NOT NULL DEFAULT 20,
    PRIMARY KEY (ID_Jadwal),
    FOREIGN KEY (ID_Dokter) REFERENCES Dokter(ID_Dokter),
    FOREIGN KEY (ID_Poli)   REFERENCES Poli(ID_Poli)
);

CREATE TABLE Pasien (
    ID_Pasien      VARCHAR(10)  NOT NULL,
    nama           VARCHAR(100) NOT NULL,
    tanggal_lahir  DATE         NOT NULL,
    jenis_kelamin  ENUM('L', 'P') NOT NULL,
    no_telepon     VARCHAR(20),
    alamat         TEXT,
    golongan_darah ENUM('A', 'B', 'AB', 'O'),
    PRIMARY KEY (ID_Pasien)
);

CREATE TABLE Staff (
    ID_Staff   VARCHAR(10)  NOT NULL,
    nama       VARCHAR(100) NOT NULL,
    jabatan    VARCHAR(50),
    username   VARCHAR(50)  NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    PRIMARY KEY (ID_Staff)
);

CREATE TABLE Antrian (
    ID_Antrian  VARCHAR(10) NOT NULL,
    ID_Pasien   VARCHAR(10) NOT NULL,
    ID_Jadwal   VARCHAR(10) NOT NULL,
    ID_Staff    VARCHAR(10),
    no_antrian  INT         NOT NULL,
    status      ENUM('menunggu','dalam_proses','selesai','batal') NOT NULL DEFAULT 'menunggu',
    tanggal     DATE        NOT NULL,
    PRIMARY KEY (ID_Antrian),
    FOREIGN KEY (ID_Pasien) REFERENCES Pasien(ID_Pasien),
    FOREIGN KEY (ID_Jadwal) REFERENCES Jadwal_Praktik(ID_Jadwal),
    FOREIGN KEY (ID_Staff)  REFERENCES Staff(ID_Staff)
);

CREATE TABLE Kunjungan (
    ID_Kunjungan VARCHAR(10)  NOT NULL,
    ID_Pasien    VARCHAR(10)  NOT NULL,
    ID_Dokter    VARCHAR(10)  NOT NULL,
    tanggal      DATE         NOT NULL,
    keluhan      TEXT,
    status       ENUM('berlangsung','selesai') NOT NULL DEFAULT 'berlangsung',
    PRIMARY KEY (ID_Kunjungan),
    FOREIGN KEY (ID_Pasien) REFERENCES Pasien(ID_Pasien),
    FOREIGN KEY (ID_Dokter) REFERENCES Dokter(ID_Dokter)
);

CREATE TABLE Obat (
    ID_Obat           VARCHAR(10)   NOT NULL,
    nama              VARCHAR(100)  NOT NULL,
    satuan            VARCHAR(20)   NOT NULL,
    harga             DECIMAL(10,2) NOT NULL,
    stok              INT           NOT NULL DEFAULT 0,
    stok_minimum      INT           NOT NULL DEFAULT 10,
    manufactured_date DATE,
    expired_date      DATE,
    PRIMARY KEY (ID_Obat)
);

CREATE TABLE Resep (
    ID_Resep     VARCHAR(10) NOT NULL,
    ID_Kunjungan VARCHAR(10) NOT NULL,
    ID_Dokter    VARCHAR(10) NOT NULL,
    tanggal      DATE        NOT NULL,
    PRIMARY KEY (ID_Resep),
    FOREIGN KEY (ID_Kunjungan) REFERENCES Kunjungan(ID_Kunjungan),
    FOREIGN KEY (ID_Dokter)    REFERENCES Dokter(ID_Dokter)
);

CREATE TABLE Detail_Resep (
    ID_Detail    VARCHAR(10)  NOT NULL,
    ID_Resep     VARCHAR(10)  NOT NULL,
    ID_Obat      VARCHAR(10)  NOT NULL,
    jumlah       INT          NOT NULL,
    dosis        VARCHAR(50),
    aturan_pakai VARCHAR(100),
    PRIMARY KEY (ID_Detail),
    FOREIGN KEY (ID_Resep) REFERENCES Resep(ID_Resep),
    FOREIGN KEY (ID_Obat)  REFERENCES Obat(ID_Obat)
);

CREATE TABLE Tagihan (
    ID_Tagihan   VARCHAR(10)   NOT NULL,
    ID_Kunjungan VARCHAR(10)   NOT NULL,
    total        DECIMAL(10,2) NOT NULL,
    status_bayar ENUM('belum_bayar','lunas') NOT NULL DEFAULT 'belum_bayar',
    tanggal      DATE          NOT NULL,
    PRIMARY KEY (ID_Tagihan),
    FOREIGN KEY (ID_Kunjungan) REFERENCES Kunjungan(ID_Kunjungan)
);

CREATE TABLE Pembayaran (
    ID_Pembayaran VARCHAR(10)   NOT NULL,
    ID_Tagihan    VARCHAR(10)   NOT NULL UNIQUE,
    ID_Staff      VARCHAR(10),
    jumlah        DECIMAL(10,2) NOT NULL,
    metode        ENUM('tunai','transfer','BPJS','kartu_debit') NOT NULL,
    tanggal       DATE          NOT NULL,
    PRIMARY KEY (ID_Pembayaran),
    FOREIGN KEY (ID_Tagihan) REFERENCES Tagihan(ID_Tagihan),
    FOREIGN KEY (ID_Staff)   REFERENCES Staff(ID_Staff)
);

-- Data dummy
INSERT INTO Poli (ID_Poli, nama_poli, no_ruangan, status) VALUES
('POL001', 'Poli Umum', 'R01', 'aktif'),
('POL002', 'Poli Gigi', 'R02', 'aktif'),
('POL003', 'Poli Anak', 'R03', 'aktif');

INSERT INTO Dokter (ID_Dokter, ID_Poli, nama, spesialisasi, no_lisensi, no_telepon) VALUES
('DOK001', 'POL001', 'Dr. Ahmad Fauzi', 'Umum', 'LIC-001', '081100001111'),
('DOK002', 'POL002', 'Dr. Siti Rahayu', 'Gigi', 'LIC-002', '081100002222'),
('DOK003', 'POL003', 'Dr. Budi Prasetyo', 'Anak', 'LIC-003', '081100003333');

INSERT INTO Staff (ID_Staff, nama, jabatan, username, password) VALUES
('STF001', 'Rina Marlina', 'Resepsionis', 'rina', 'password123'),
('STF002', 'Doni Kusuma', 'Kasir', 'doni', 'password123');

INSERT INTO Jadwal_Praktik (ID_Jadwal, ID_Dokter, ID_Poli, hari, jam_mulai, jam_selesai, kuota) VALUES
('JDW001', 'DOK001', 'POL001', 'Senin', '08:00:00', '12:00:00', 20),
('JDW002', 'DOK002', 'POL002', 'Selasa', '09:00:00', '13:00:00', 15),
('JDW003', 'DOK003', 'POL003', 'Rabu', '10:00:00', '14:00:00', 10);

INSERT INTO Pasien (ID_Pasien, nama, tanggal_lahir, jenis_kelamin, no_telepon, alamat, golongan_darah) VALUES
('PSN001', 'Budi Santoso', '1990-05-15', 'L', '081234567890', 'Jl. Merdeka No. 10 Surabaya', 'A'),
('PSN002', 'Sari Dewi', '1995-08-20', 'P', '082200002222', 'Jl. Sudirman No. 5 Surabaya', 'B'),
('PSN003', 'Andi Pratama', '2010-03-10', 'L', '083300003333', 'Jl. Diponegoro No. 3 Surabaya', 'O');

INSERT INTO Antrian (ID_Antrian, ID_Pasien, ID_Jadwal, ID_Staff, no_antrian, status, tanggal) VALUES
('ANT001', 'PSN001', 'JDW001', 'STF001', 1, 'selesai', '2026-06-10'),
('ANT002', 'PSN002', 'JDW002', 'STF001', 1, 'selesai', '2026-06-10'),
('ANT003', 'PSN003', 'JDW003', 'STF001', 1, 'selesai', '2026-06-10');

INSERT INTO Kunjungan (ID_Kunjungan, ID_Pasien, ID_Dokter, tanggal, keluhan, status) VALUES
('KNJ001', 'PSN001', 'DOK001', '2026-06-10', 'Demam tinggi sejak 3 hari', 'selesai'),
('KNJ002', 'PSN002', 'DOK002', '2026-06-10', 'Sakit gigi berlubang', 'selesai'),
('KNJ003', 'PSN003', 'DOK003', '2026-06-10', 'Batuk pilek', 'selesai');

INSERT INTO Obat (ID_Obat, nama, satuan, harga, stok, stok_minimum, manufactured_date, expired_date) VALUES
('OBT001', 'Amoxicillin 500mg', 'Tablet', 2000, 100, 20, '2025-01-01', '2027-01-01'),
('OBT002', 'Paracetamol 500mg', 'Tablet', 500, 200, 30, '2025-03-01', '2027-03-01'),
('OBT003', 'Vitamin C 1000mg', 'Tablet', 1500, 150, 20, '2025-06-01', '2027-06-01');

INSERT INTO Resep (ID_Resep, ID_Kunjungan, ID_Dokter, tanggal) VALUES
('RES001', 'KNJ001', 'DOK001', '2026-06-10'),
('RES002', 'KNJ002', 'DOK002', '2026-06-10'),
('RES003', 'KNJ003', 'DOK003', '2026-06-10');

INSERT INTO Detail_Resep (ID_Detail, ID_Resep, ID_Obat, jumlah, dosis, aturan_pakai) VALUES
('DTL001', 'RES001', 'OBT001', 10, '500mg', '3x sehari sesudah makan'),
('DTL002', 'RES001', 'OBT002', 10, '500mg', '3x sehari sesudah makan'),
('DTL003', 'RES002', 'OBT002', 6, '500mg', '2x sehari sesudah makan'),
('DTL004', 'RES003', 'OBT002', 6, '500mg', '2x sehari sesudah makan'),
('DTL005', 'RES003', 'OBT003', 10, '1000mg', '1x sehari sesudah makan');

INSERT INTO Tagihan (ID_Tagihan, ID_Kunjungan, total, status_bayar, tanggal) VALUES
('TAG001', 'KNJ001', 75000, 'lunas', '2026-06-10'),
('TAG002', 'KNJ002', 120000, 'lunas', '2026-06-10'),
('TAG003', 'KNJ003', 50000, 'lunas', '2026-06-10');

INSERT INTO Pembayaran (ID_Pembayaran, ID_Tagihan, ID_Staff, jumlah, metode, tanggal) VALUES
('PAY001', 'TAG001', 'STF002', 75000, 'tunai', '2026-06-10'),
('PAY002', 'TAG002', 'STF002', 120000, 'transfer', '2026-06-10'),
('PAY003', 'TAG003', 'STF002', 50000, 'tunai', '2026-06-11');
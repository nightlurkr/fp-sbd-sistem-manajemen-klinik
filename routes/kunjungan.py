from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Kunjungan, Antrian, Jadwal_Praktik, Tagihan
from utils import validate_id
from datetime import date

router = APIRouter()

@router.get("/")
def get_all_kunjungan(db: Session = Depends(get_db)):
    return db.query(Kunjungan).all()

@router.get("/{id_pasien}")
def get_kunjungan_pasien(id_pasien: str, db: Session = Depends(get_db)):
    validate_id(id_pasien, "PSN")
    return db.query(Kunjungan).filter(Kunjungan.ID_Pasien == id_pasien).all()

@router.post("/dari-antrian/{id_antrian}")
def buat_kunjungan_dari_antrian(
    id_antrian: str,
    ID_Kunjungan: str,
    keluhan: str,
    db: Session = Depends(get_db)
):
    validate_id(id_antrian, "ANT")
    validate_id(ID_Kunjungan, "KNJ")

    antrian = db.query(Antrian).filter(Antrian.ID_Antrian == id_antrian).first()
    if not antrian:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan")
    if antrian.status != "dalam_proses":
        raise HTTPException(
            status_code=400,
            detail="Antrian harus dipanggil dulu sebelum membuat kunjungan"
        )

    jadwal = db.query(Jadwal_Praktik).filter(
        Jadwal_Praktik.ID_Jadwal == antrian.ID_Jadwal
    ).first()

    kunjungan_baru = Kunjungan(
        ID_Kunjungan=ID_Kunjungan,
        ID_Pasien=antrian.ID_Pasien,
        ID_Dokter=jadwal.ID_Dokter,
        tanggal=date.today(),
        keluhan=keluhan,
        status="berlangsung"
    )
    db.add(kunjungan_baru)
    antrian.status = "selesai"
    db.commit()
    db.refresh(kunjungan_baru)
    return {"message": "Kunjungan berhasil dibuat", "data": kunjungan_baru}

@router.put("/{id_kunjungan}/selesai")
def selesaikan_kunjungan(
    id_kunjungan: str,
    ID_Tagihan: str,
    total: float,
    db: Session = Depends(get_db)
):
    validate_id(id_kunjungan, "KNJ")
    validate_id(ID_Tagihan, "TAG")

    kunjungan = db.query(Kunjungan).filter(Kunjungan.ID_Kunjungan == id_kunjungan).first()
    if not kunjungan:
        raise HTTPException(status_code=404, detail="Kunjungan tidak ditemukan")
    if kunjungan.status != "berlangsung":
        raise HTTPException(status_code=400, detail="Kunjungan sudah selesai")

    kunjungan.status = "selesai"
    tagihan_baru = Tagihan(
        ID_Tagihan=ID_Tagihan,
        ID_Kunjungan=id_kunjungan,
        total=total,
        status_bayar="belum_bayar",
        tanggal=date.today()
    )
    db.add(tagihan_baru)
    db.commit()
    db.refresh(kunjungan)
    return {
        "message": "Kunjungan selesai, tagihan otomatis dibuat",
        "tagihan": ID_Tagihan,
        "total": total
    }

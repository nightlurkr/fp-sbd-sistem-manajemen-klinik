from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Antrian, Jadwal_Praktik
from datetime import date

router = APIRouter()

@router.get("/")
def get_all_antrian(db: Session = Depends(get_db)):
    return db.query(Antrian).all()

@router.get("/{id_jadwal}")
def get_antrian(id_jadwal: str, db: Session = Depends(get_db)):
    return db.query(Antrian).filter(
        Antrian.ID_Jadwal == id_jadwal,
        Antrian.tanggal == date.today()
    ).all()

@router.post("/")
def daftar_antrian(
    ID_Antrian: str,
    ID_Pasien: str,
    ID_Jadwal: str,
    tanggal: str,
    ID_Staff: str = None,
    db: Session = Depends(get_db)
):
    # Cek jadwal ada atau tidak
    jadwal = db.query(Jadwal_Praktik).filter(
        Jadwal_Praktik.ID_Jadwal == ID_Jadwal
    ).first()

    if not jadwal:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")

    # Hitung antrian yang sudah ada hari ini
    antrian_hari_ini = db.query(Antrian).filter(
        Antrian.ID_Jadwal == ID_Jadwal,
        Antrian.tanggal == tanggal,
        Antrian.status != "batal"
    ).count()

    # Cek kuota
    if antrian_hari_ini >= jadwal.kuota:
        raise HTTPException(
            status_code=400,
            detail=f"Kuota jadwal penuh. Maksimal {jadwal.kuota} pasien per hari"
        )

    # Auto-generate nomor antrian
    nomor_baru = antrian_hari_ini + 1

    antrian_baru = Antrian(
        ID_Antrian=ID_Antrian,
        ID_Pasien=ID_Pasien,
        ID_Jadwal=ID_Jadwal,
        ID_Staff=ID_Staff,
        no_antrian=nomor_baru,
        status="menunggu",
        tanggal=tanggal
    )
    db.add(antrian_baru)
    db.commit()
    db.refresh(antrian_baru)
    return {
        "message": "Antrian berhasil didaftarkan",
        "nomor_antrian": nomor_baru,
        "data": antrian_baru
    }

@router.put("/{id_antrian}/panggil")
def panggil_antrian(
    id_antrian: str,
    db: Session = Depends(get_db)
):
    antrian = db.query(Antrian).filter(
        Antrian.ID_Antrian == id_antrian
    ).first()

    if not antrian:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan")

    if antrian.status != "menunggu":
        raise HTTPException(
            status_code=400,
            detail=f"Antrian tidak bisa dipanggil, status saat ini: {antrian.status}"
        )

    antrian.status = "dalam_proses"
    db.commit()
    db.refresh(antrian)
    return {
        "message": f"Pasien nomor antrian {antrian.no_antrian} dipanggil",
        "data": antrian
    }

@router.put("/{id_antrian}/batal")
def batal_antrian(
    id_antrian: str,
    db: Session = Depends(get_db)
):
    antrian = db.query(Antrian).filter(
        Antrian.ID_Antrian == id_antrian
    ).first()

    if not antrian:
        raise HTTPException(status_code=404, detail="Antrian tidak ditemukan")

    antrian.status = "batal"
    db.commit()
    db.refresh(antrian)
    return {"message": "Antrian dibatalkan", "data": antrian}
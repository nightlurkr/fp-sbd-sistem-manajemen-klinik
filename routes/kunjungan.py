from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Kunjungan

router = APIRouter()

@router.get("/")
def get_all_kunjungan(db: Session = Depends(get_db)):
    return db.query(Kunjungan).all()

@router.get("/{id_pasien}")
def get_kunjungan_pasien(id_pasien: str, db: Session = Depends(get_db)):
    return db.query(Kunjungan).filter(Kunjungan.ID_Pasien == id_pasien).all()

@router.post("/")
def tambah_kunjungan(
    ID_Kunjungan: str, ID_Pasien: str,
    ID_Dokter: str, tanggal: str,
    keluhan: str = None,
    db: Session = Depends(get_db)
):
    kunjungan_baru = Kunjungan(
        ID_Kunjungan=ID_Kunjungan, ID_Pasien=ID_Pasien,
        ID_Dokter=ID_Dokter, tanggal=tanggal,
        keluhan=keluhan
    )
    db.add(kunjungan_baru)
    db.commit()
    db.refresh(kunjungan_baru)
    return kunjungan_baru
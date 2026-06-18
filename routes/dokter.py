from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Dokter
from utils import validate_id

router = APIRouter()

@router.get("/")
def get_all_dokter(db: Session = Depends(get_db)):
    return db.query(Dokter).all()

@router.get("/{id_dokter}")
def get_dokter(id_dokter: str, db: Session = Depends(get_db)):
    validate_id(id_dokter, "DOK")
    dokter = db.query(Dokter).filter(Dokter.ID_Dokter == id_dokter).first()
    if not dokter:
        raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")
    return dokter

@router.post("/")
def tambah_dokter(
    ID_Dokter: str, ID_Poli: str, nama: str,
    no_lisensi: str, spesialisasi: str = None,
    no_telepon: str = None,
    db: Session = Depends(get_db)
):
    validate_id(ID_Dokter, "DOK")
    validate_id(ID_Poli, "POL")
    dokter_baru = Dokter(
        ID_Dokter=ID_Dokter, ID_Poli=ID_Poli,
        nama=nama, spesialisasi=spesialisasi,
        no_lisensi=no_lisensi, no_telepon=no_telepon
    )
    db.add(dokter_baru)
    db.commit()
    db.refresh(dokter_baru)
    return dokter_baru

@router.put("/{id_dokter}")
def update_dokter(
    id_dokter: str, nama: str = None,
    spesialisasi: str = None, no_telepon: str = None,
    db: Session = Depends(get_db)
):
    validate_id(id_dokter, "DOK")
    dokter = db.query(Dokter).filter(Dokter.ID_Dokter == id_dokter).first()
    if not dokter:
        raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")
    if nama: dokter.nama = nama
    if spesialisasi: dokter.spesialisasi = spesialisasi
    if no_telepon: dokter.no_telepon = no_telepon
    db.commit()
    db.refresh(dokter)
    return dokter

@router.delete("/{id_dokter}")
def hapus_dokter(id_dokter: str, db: Session = Depends(get_db)):
    validate_id(id_dokter, "DOK")
    dokter = db.query(Dokter).filter(Dokter.ID_Dokter == id_dokter).first()
    if not dokter:
        raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")
    db.delete(dokter)
    db.commit()
    return {"message": f"Dokter {id_dokter} berhasil dihapus"}

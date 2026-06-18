from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Pasien
from utils import validate_id

router = APIRouter()

@router.get("/")
def get_all_pasien(db: Session = Depends(get_db)):
    return db.query(Pasien).all()

@router.get("/{id_pasien}")
def get_pasien(id_pasien: str, db: Session = Depends(get_db)):
    validate_id(id_pasien, "PSN")
    pasien = db.query(Pasien).filter(Pasien.ID_Pasien == id_pasien).first()
    if not pasien:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")
    return pasien

@router.post("/")
def tambah_pasien(
    ID_Pasien: str, nama: str, tanggal_lahir: str,
    jenis_kelamin: str, no_telepon: str = None,
    alamat: str = None, golongan_darah: str = None,
    db: Session = Depends(get_db)
):
    validate_id(ID_Pasien, "PSN")
    pasien_baru = Pasien(
        ID_Pasien=ID_Pasien, nama=nama,
        tanggal_lahir=tanggal_lahir,
        jenis_kelamin=jenis_kelamin,
        no_telepon=no_telepon,
        alamat=alamat,
        golongan_darah=golongan_darah
    )
    db.add(pasien_baru)
    db.commit()
    db.refresh(pasien_baru)
    return pasien_baru

@router.put("/{id_pasien}")
def update_pasien(
    id_pasien: str, nama: str = None,
    no_telepon: str = None, alamat: str = None,
    db: Session = Depends(get_db)
):
    validate_id(id_pasien, "PSN")
    pasien = db.query(Pasien).filter(Pasien.ID_Pasien == id_pasien).first()
    if not pasien:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")
    if nama: pasien.nama = nama
    if no_telepon: pasien.no_telepon = no_telepon
    if alamat: pasien.alamat = alamat
    db.commit()
    db.refresh(pasien)
    return pasien

@router.delete("/{id_pasien}")
def hapus_pasien(id_pasien: str, db: Session = Depends(get_db)):
    validate_id(id_pasien, "PSN")
    pasien = db.query(Pasien).filter(Pasien.ID_Pasien == id_pasien).first()
    if not pasien:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")
    db.delete(pasien)
    db.commit()
    return {"message": f"Pasien {id_pasien} berhasil dihapus"}

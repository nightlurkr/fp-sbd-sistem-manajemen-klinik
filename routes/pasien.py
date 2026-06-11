from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Pasien

router = APIRouter()

@router.get("/")
def get_all_pasien(db: Session = Depends(get_db)):
    return db.query(Pasien).all()

@router.get("/{id_pasien}")
def get_pasien(id_pasien: str, db: Session = Depends(get_db)):
    return db.query(Pasien).filter(Pasien.ID_Pasien == id_pasien).first()

@router.post("/")
def tambah_pasien(
    ID_Pasien: str, nama: str, tanggal_lahir: str,
    jenis_kelamin: str, no_telepon: str = None,
    alamat: str = None, golongan_darah: str = None,
    db: Session = Depends(get_db)
):
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
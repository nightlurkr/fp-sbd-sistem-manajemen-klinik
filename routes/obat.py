from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Obat

router = APIRouter()

@router.get("/")
def get_all_obat(db: Session = Depends(get_db)):
    return db.query(Obat).all()

@router.get("/stok-menipis")
def get_stok_menipis(db: Session = Depends(get_db)):
    return db.query(Obat).filter(Obat.stok <= Obat.stok_minimum).all()

@router.get("/{id_obat}")
def get_obat(id_obat: str, db: Session = Depends(get_db)):
    return db.query(Obat).filter(Obat.ID_Obat == id_obat).first()

@router.post("/")
def tambah_obat(
    ID_Obat: str, nama: str, satuan: str,
    harga: float, stok: int, stok_minimum: int,
    manufactured_date: str = None,
    expired_date: str = None,
    db: Session = Depends(get_db)
):
    obat_baru = Obat(
        ID_Obat=ID_Obat, nama=nama, satuan=satuan,
        harga=harga, stok=stok, stok_minimum=stok_minimum,
        manufactured_date=manufactured_date,
        expired_date=expired_date
    )
    db.add(obat_baru)
    db.commit()
    db.refresh(obat_baru)
    return obat_baru

@router.put("/{id_obat}/stok")
def update_stok(
    id_obat: str, jumlah: int,
    db: Session = Depends(get_db)
):
    obat = db.query(Obat).filter(Obat.ID_Obat == id_obat).first()
    obat.stok = obat.stok + jumlah
    db.commit()
    db.refresh(obat)
    return { "message": "Stok berhasil diupdate", "stok_sekarang": obat.stok }
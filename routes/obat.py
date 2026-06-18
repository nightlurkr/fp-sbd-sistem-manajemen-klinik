from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Obat
from utils import validate_id

router = APIRouter()

@router.get("/")
def get_all_obat(db: Session = Depends(get_db)):
    return db.query(Obat).all()

@router.get("/stok-menipis")
def get_stok_menipis(db: Session = Depends(get_db)):
    return db.query(Obat).filter(Obat.stok <= Obat.stok_minimum).all()

@router.get("/{id_obat}")
def get_obat(id_obat: str, db: Session = Depends(get_db)):
    validate_id(id_obat, "OBT")
    return db.query(Obat).filter(Obat.ID_Obat == id_obat).first()

@router.post("/")
def tambah_obat(
    ID_Obat: str, nama: str, satuan: str,
    harga: float, stok: int, stok_minimum: int,
    manufactured_date: str = None,
    expired_date: str = None,
    db: Session = Depends(get_db)
):
    validate_id(ID_Obat, "OBT")
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

@router.put("/{id_obat}")
def update_obat(
    id_obat: str, nama: str = None, satuan: str = None,
    harga: float = None, stok_minimum: int = None,
    manufactured_date: str = None, expired_date: str = None,
    db: Session = Depends(get_db)
):
    validate_id(id_obat, "OBT")
    obat = db.query(Obat).filter(Obat.ID_Obat == id_obat).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    if nama: obat.nama = nama
    if satuan: obat.satuan = satuan
    if harga is not None: obat.harga = harga
    if stok_minimum is not None: obat.stok_minimum = stok_minimum
    if manufactured_date: obat.manufactured_date = manufactured_date
    if expired_date: obat.expired_date = expired_date
    db.commit()
    db.refresh(obat)
    return obat

@router.put("/{id_obat}/stok")
def update_stok(id_obat: str, jumlah: int, db: Session = Depends(get_db)):
    validate_id(id_obat, "OBT")
    obat = db.query(Obat).filter(Obat.ID_Obat == id_obat).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    obat.stok = obat.stok + jumlah
    db.commit()
    db.refresh(obat)
    return {"message": "Stok berhasil diupdate", "stok_sekarang": obat.stok}

@router.delete("/{id_obat}")
def hapus_obat(id_obat: str, db: Session = Depends(get_db)):
    validate_id(id_obat, "OBT")
    obat = db.query(Obat).filter(Obat.ID_Obat == id_obat).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    db.delete(obat)
    db.commit()
    return {"message": f"Obat {id_obat} berhasil dihapus"}

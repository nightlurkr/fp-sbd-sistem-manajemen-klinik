from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tagihan, Pembayaran
from utils import validate_id

router = APIRouter()

@router.get("/")
def get_all_tagihan(db: Session = Depends(get_db)):
    return db.query(Tagihan).all()

@router.get("/{id_kunjungan}")
def get_tagihan_kunjungan(id_kunjungan: str, db: Session = Depends(get_db)):
    validate_id(id_kunjungan, "KNJ")
    return db.query(Tagihan).filter(Tagihan.ID_Kunjungan == id_kunjungan).first()

@router.post("/")
def tambah_tagihan(
    ID_Tagihan: str, ID_Kunjungan: str,
    total: float, tanggal: str,
    db: Session = Depends(get_db)
):
    validate_id(ID_Tagihan, "TAG")
    validate_id(ID_Kunjungan, "KNJ")
    tagihan_baru = Tagihan(
        ID_Tagihan=ID_Tagihan,
        ID_Kunjungan=ID_Kunjungan,
        total=total,
        tanggal=tanggal
    )
    db.add(tagihan_baru)
    db.commit()
    db.refresh(tagihan_baru)
    return tagihan_baru

@router.put("/{id_tagihan}/bayar")
def bayar_tagihan(
    id_tagihan: str,
    ID_Pembayaran: str,
    jumlah: float,
    metode: str,
    tanggal: str,
    ID_Staff: str = None,
    db: Session = Depends(get_db)
):
    validate_id(id_tagihan, "TAG")
    validate_id(ID_Pembayaran, "PAY")
    if ID_Staff:
        validate_id(ID_Staff, "STF")

    tagihan = db.query(Tagihan).filter(Tagihan.ID_Tagihan == id_tagihan).first()
    if not tagihan:
        raise HTTPException(status_code=404, detail="Tagihan tidak ditemukan")
    if tagihan.status_bayar == "lunas":
        raise HTTPException(status_code=400, detail="Tagihan sudah lunas")

    tagihan.status_bayar = "lunas"
    pembayaran_baru = Pembayaran(
        ID_Pembayaran=ID_Pembayaran,
        ID_Tagihan=id_tagihan,
        ID_Staff=ID_Staff,
        jumlah=jumlah,
        metode=metode,
        tanggal=tanggal
    )
    db.add(pembayaran_baru)
    db.commit()
    db.refresh(tagihan)
    return {"message": "Pembayaran berhasil", "tagihan": id_tagihan, "status": "lunas"}

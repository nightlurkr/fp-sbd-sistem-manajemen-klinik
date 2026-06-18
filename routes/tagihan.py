from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Tagihan, Pembayaran

router = APIRouter()

@router.get("/")
def get_all_tagihan(db: Session = Depends(get_db)):
    return db.query(Tagihan).all()

@router.get("/{id_kunjungan}")
def get_tagihan_kunjungan(id_kunjungan: str, db: Session = Depends(get_db)):
    return db.query(Tagihan).filter(Tagihan.ID_Kunjungan == id_kunjungan).first()

@router.post("/")
def tambah_tagihan(
    ID_Tagihan: str, ID_Kunjungan: str,
    total: float, tanggal: str,
    db: Session = Depends(get_db)
):
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
    tagihan = db.query(Tagihan).filter(Tagihan.ID_Tagihan == id_tagihan).first()
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
    return { "message": "Pembayaran berhasil", "tagihan": id_tagihan, "status": "lunas" }
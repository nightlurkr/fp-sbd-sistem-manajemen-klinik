from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import Resep, Detail_Resep, Obat, Kunjungan
from datetime import date

router = APIRouter()

class ItemObat(BaseModel):
    id_detail: str
    id_obat: str
    jumlah: int
    dosis: Optional[str] = None
    aturan_pakai: Optional[str] = None

class ResepRequest(BaseModel):
    ID_Resep: str
    ID_Kunjungan: str
    obat_list: List[ItemObat]

@router.get("/{id_kunjungan}")
def get_resep(id_kunjungan: str, db: Session = Depends(get_db)):
    resep = db.query(Resep).filter(
        Resep.ID_Kunjungan == id_kunjungan
    ).first()

    if not resep:
        raise HTTPException(status_code=404, detail="Resep tidak ditemukan")

    detail = db.query(Detail_Resep).filter(
        Detail_Resep.ID_Resep == resep.ID_Resep
    ).all()

    return {
        "ID_Resep": resep.ID_Resep,
        "ID_Kunjungan": resep.ID_Kunjungan,
        "ID_Dokter": resep.ID_Dokter,
        "tanggal": resep.tanggal,
        "detail_obat": [
            {
                "ID_Obat": d.ID_Obat,
                "jumlah": d.jumlah,
                "dosis": d.dosis,
                "aturan_pakai": d.aturan_pakai
            }
            for d in detail
        ]
    }

@router.post("/")
def buat_resep(request: ResepRequest, db: Session = Depends(get_db)):
    kunjungan = db.query(Kunjungan).filter(
        Kunjungan.ID_Kunjungan == request.ID_Kunjungan
    ).first()

    if not kunjungan:
        raise HTTPException(status_code=404, detail="Kunjungan tidak ditemukan")

    # Cek stok dan expired semua obat dulu
    for item in request.obat_list:
        obat = db.query(Obat).filter(Obat.ID_Obat == item.id_obat).first()

        if not obat:
            raise HTTPException(status_code=404, detail=f"Obat {item.id_obat} tidak ditemukan")

        if obat.stok < item.jumlah:
            raise HTTPException(status_code=400, detail=f"Stok {obat.nama} tidak cukup. Stok tersedia: {obat.stok}")

        if obat.expired_date and obat.expired_date < date.today():
            raise HTTPException(status_code=400, detail=f"Obat {obat.nama} sudah kadaluarsa")

    # Buat resep
    resep_baru = Resep(
        ID_Resep=request.ID_Resep,
        ID_Kunjungan=request.ID_Kunjungan,
        ID_Dokter=kunjungan.ID_Dokter,
        tanggal=date.today()
    )
    db.add(resep_baru)
    db.flush()  # ← tambahkan ini

    # Buat detail resep dan kurangi stok
    for item in request.obat_list:
        obat = db.query(Obat).filter(Obat.ID_Obat == item.id_obat).first()

        detail = Detail_Resep(
            ID_Detail=item.id_detail,
            ID_Resep=request.ID_Resep,
            ID_Obat=item.id_obat,
            jumlah=item.jumlah,
            dosis=item.dosis,
            aturan_pakai=item.aturan_pakai
        )
        db.add(detail)
        obat.stok = obat.stok - item.jumlah

    db.commit()
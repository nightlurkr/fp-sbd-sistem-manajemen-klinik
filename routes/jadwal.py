from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Jadwal_Praktik

router = APIRouter()

@router.get("/")
def get_all_jadwal(db: Session = Depends(get_db)):
    return db.query(Jadwal_Praktik).all()

@router.get("/{id_jadwal}")
def get_jadwal(id_jadwal: str, db: Session = Depends(get_db)):
    jadwal = db.query(Jadwal_Praktik).filter(
        Jadwal_Praktik.ID_Jadwal == id_jadwal
    ).first()
    if not jadwal:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")
    return jadwal

@router.post("/")
def tambah_jadwal(
    ID_Jadwal: str, ID_Dokter: str, ID_Poli: str,
    hari: str, jam_mulai: str, jam_selesai: str,
    kuota: int = 20,
    db: Session = Depends(get_db)
):
    jadwal_baru = Jadwal_Praktik(
        ID_Jadwal=ID_Jadwal, ID_Dokter=ID_Dokter,
        ID_Poli=ID_Poli, hari=hari,
        jam_mulai=jam_mulai, jam_selesai=jam_selesai,
        kuota=kuota
    )
    db.add(jadwal_baru)
    db.commit()
    db.refresh(jadwal_baru)
    return jadwal_baru

@router.put("/{id_jadwal}")
def update_jadwal(
    id_jadwal: str, hari: str = None,
    jam_mulai: str = None, jam_selesai: str = None,
    kuota: int = None,
    db: Session = Depends(get_db)
):
    jadwal = db.query(Jadwal_Praktik).filter(
        Jadwal_Praktik.ID_Jadwal == id_jadwal
    ).first()
    if not jadwal:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")
    if hari: jadwal.hari = hari
    if jam_mulai: jadwal.jam_mulai = jam_mulai
    if jam_selesai: jadwal.jam_selesai = jam_selesai
    if kuota is not None: jadwal.kuota = kuota
    db.commit()
    db.refresh(jadwal)
    return jadwal

@router.delete("/{id_jadwal}")
def hapus_jadwal(id_jadwal: str, db: Session = Depends(get_db)):
    jadwal = db.query(Jadwal_Praktik).filter(
        Jadwal_Praktik.ID_Jadwal == id_jadwal
    ).first()
    if not jadwal:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")
    db.delete(jadwal)
    db.commit()
    return {"message": f"Jadwal {id_jadwal} berhasil dihapus"}

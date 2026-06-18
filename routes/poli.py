from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Poli

router = APIRouter()

@router.get("/")
def get_all_poli(db: Session = Depends(get_db)):
    return db.query(Poli).all()

@router.get("/{id_poli}")
def get_poli(id_poli: str, db: Session = Depends(get_db)):
    poli = db.query(Poli).filter(Poli.ID_Poli == id_poli).first()
    if not poli:
        raise HTTPException(status_code=404, detail="Poli tidak ditemukan")
    return poli

@router.post("/")
def tambah_poli(
    ID_Poli: str, nama_poli: str,
    no_ruangan: str = None, status: str = "aktif",
    db: Session = Depends(get_db)
):
    poli_baru = Poli(
        ID_Poli=ID_Poli, nama_poli=nama_poli,
        no_ruangan=no_ruangan, status=status
    )
    db.add(poli_baru)
    db.commit()
    db.refresh(poli_baru)
    return poli_baru

@router.put("/{id_poli}")
def update_poli(
    id_poli: str, nama_poli: str = None,
    no_ruangan: str = None, status: str = None,
    db: Session = Depends(get_db)
):
    poli = db.query(Poli).filter(Poli.ID_Poli == id_poli).first()
    if not poli:
        raise HTTPException(status_code=404, detail="Poli tidak ditemukan")
    if nama_poli: poli.nama_poli = nama_poli
    if no_ruangan: poli.no_ruangan = no_ruangan
    if status: poli.status = status
    db.commit()
    db.refresh(poli)
    return poli

@router.delete("/{id_poli}")
def hapus_poli(id_poli: str, db: Session = Depends(get_db)):
    poli = db.query(Poli).filter(Poli.ID_Poli == id_poli).first()
    if not poli:
        raise HTTPException(status_code=404, detail="Poli tidak ditemukan")
    db.delete(poli)
    db.commit()
    return {"message": f"Poli {id_poli} berhasil dihapus"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Antrian

router = APIRouter()

@router.get("/{id_jadwal}")
def get_antrian(id_jadwal: str, db: Session = Depends(get_db)):
    return db.query(Antrian).filter(Antrian.ID_Jadwal == id_jadwal).all()

@router.post("/")
def tambah_antrian(
    ID_Antrian: str, ID_Pasien: str, ID_Jadwal: str,
    no_antrian: int, tanggal: str,
    ID_Staff: str = None,
    db: Session = Depends(get_db)
):
    antrian_baru = Antrian(
        ID_Antrian=ID_Antrian, ID_Pasien=ID_Pasien,
        ID_Jadwal=ID_Jadwal, no_antrian=no_antrian,
        tanggal=tanggal, ID_Staff=ID_Staff
    )
    db.add(antrian_baru)
    db.commit()
    db.refresh(antrian_baru)
    return antrian_baru

@router.put("/{id_antrian}/status")
def update_status_antrian(
    id_antrian: str, status: str,
    db: Session = Depends(get_db)
):
    antrian = db.query(Antrian).filter(Antrian.ID_Antrian == id_antrian).first()
    antrian.status = status
    db.commit()
    db.refresh(antrian)
    return antrian
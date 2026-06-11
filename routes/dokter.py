from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Dokter

router = APIRouter()

@router.get("/")
def get_all_dokter(db: Session = Depends(get_db)):
    return db.query(Dokter).all()

@router.get("/{id_dokter}")
def get_dokter(id_dokter: str, db: Session = Depends(get_db)):
    return db.query(Dokter).filter(Dokter.ID_Dokter == id_dokter).first()
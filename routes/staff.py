from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Staff
from utils import validate_id

router = APIRouter()

@router.get("/")
def get_all_staff(db: Session = Depends(get_db)):
    return db.query(Staff).all()

@router.get("/{id_staff}")
def get_staff(id_staff: str, db: Session = Depends(get_db)):
    validate_id(id_staff, "STF")
    staff = db.query(Staff).filter(Staff.ID_Staff == id_staff).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff tidak ditemukan")
    return staff

@router.post("/")
def tambah_staff(
    ID_Staff: str, nama: str, username: str, password: str,
    jabatan: str = None,
    db: Session = Depends(get_db)
):
    validate_id(ID_Staff, "STF")
    staff_baru = Staff(
        ID_Staff=ID_Staff, nama=nama,
        jabatan=jabatan, username=username,
        password=password
    )
    db.add(staff_baru)
    db.commit()
    db.refresh(staff_baru)
    return staff_baru

@router.put("/{id_staff}")
def update_staff(
    id_staff: str, nama: str = None,
    jabatan: str = None, username: str = None,
    password: str = None,
    db: Session = Depends(get_db)
):
    validate_id(id_staff, "STF")
    staff = db.query(Staff).filter(Staff.ID_Staff == id_staff).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff tidak ditemukan")
    if nama: staff.nama = nama
    if jabatan: staff.jabatan = jabatan
    if username: staff.username = username
    if password: staff.password = password
    db.commit()
    db.refresh(staff)
    return staff

@router.delete("/{id_staff}")
def hapus_staff(id_staff: str, db: Session = Depends(get_db)):
    validate_id(id_staff, "STF")
    staff = db.query(Staff).filter(Staff.ID_Staff == id_staff).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff tidak ditemukan")
    db.delete(staff)
    db.commit()
    return {"message": f"Staff {id_staff} berhasil dihapus"}

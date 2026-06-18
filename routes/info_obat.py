from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database import get_mongo
from utils import validate_id

router = APIRouter()

class InfoObatRequest(BaseModel):
    id_obat: str
    nama: str
    deskripsi: str
    efek_samping: List[str] = []
    kontraindikasi: List[str] = []
    interaksi_obat: List[str] = []
    cara_penyimpanan: Optional[str] = None

@router.get("/")
def get_all_info_obat():
    mongo = get_mongo()
    return list(mongo.info_obat.find({}, {"_id": 0}))

@router.get("/{id_obat}")
def get_info_obat(id_obat: str):
    validate_id(id_obat, "OBT")
    mongo = get_mongo()
    info = mongo.info_obat.find_one({"id_obat": id_obat}, {"_id": 0})
    if not info:
        raise HTTPException(status_code=404, detail="Info obat tidak ditemukan")
    return info

@router.post("/")
def tambah_info_obat(request: InfoObatRequest):
    validate_id(request.id_obat, "OBT")
    mongo = get_mongo()
    data = request.model_dump()
    mongo.info_obat.insert_one(data)
    return {"message": "Info obat berhasil disimpan"}

@router.put("/{id_obat}")
def update_info_obat(id_obat: str, request: InfoObatRequest):
    validate_id(id_obat, "OBT")
    validate_id(request.id_obat, "OBT")
    mongo = get_mongo()
    result = mongo.info_obat.update_one(
        {"id_obat": id_obat},
        {"$set": request.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Info obat tidak ditemukan")
    return {"message": "Info obat berhasil diupdate"}

@router.delete("/{id_obat}")
def hapus_info_obat(id_obat: str):
    validate_id(id_obat, "OBT")
    mongo = get_mongo()
    result = mongo.info_obat.delete_one({"id_obat": id_obat})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Info obat tidak ditemukan")
    return {"message": f"Info obat {id_obat} berhasil dihapus"}

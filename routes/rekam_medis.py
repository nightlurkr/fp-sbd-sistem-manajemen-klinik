from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from database import get_mongo

router = APIRouter()

class RekamMedisRequest(BaseModel):
    id_kunjungan: str
    id_pasien: str
    id_dokter: str
    tanggal: str
    keluhan: str
    diagnosis: List[str]
    tindakan: List[str]
    catatan_dokter: Optional[str] = None
    hasil_lab: Optional[Dict] = None
    foto: List[str] = []

@router.get("/{id_pasien}")
def get_rekam_medis(id_pasien: str):
    mongo = get_mongo()
    hasil = list(mongo.rekam_medis.find(
        {"id_pasien": id_pasien},
        {"_id": 0}
    ))
    return hasil

@router.get("/kunjungan/{id_kunjungan}")
def get_rekam_medis_by_kunjungan(id_kunjungan: str):
    mongo = get_mongo()
    hasil = mongo.rekam_medis.find_one(
        {"id_kunjungan": id_kunjungan},
        {"_id": 0}
    )
    if not hasil:
        raise HTTPException(status_code=404, detail="Rekam medis tidak ditemukan")
    return hasil

@router.post("/")
def tambah_rekam_medis(request: RekamMedisRequest):
    mongo = get_mongo()
    data = request.model_dump()
    mongo.rekam_medis.insert_one(data)
    return {"message": "Rekam medis berhasil disimpan"}

@router.put("/{id_kunjungan}")
def update_rekam_medis(id_kunjungan: str, request: RekamMedisRequest):
    mongo = get_mongo()
    result = mongo.rekam_medis.update_one(
        {"id_kunjungan": id_kunjungan},
        {"$set": request.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Rekam medis tidak ditemukan")
    return {"message": "Rekam medis berhasil diupdate"}

@router.delete("/{id_kunjungan}")
def hapus_rekam_medis(id_kunjungan: str):
    mongo = get_mongo()
    result = mongo.rekam_medis.delete_one({"id_kunjungan": id_kunjungan})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rekam medis tidak ditemukan")
    return {"message": "Rekam medis berhasil dihapus"}

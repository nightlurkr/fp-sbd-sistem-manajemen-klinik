from fastapi import APIRouter
from database import get_mongo

router = APIRouter()

@router.get("/{id_pasien}")
def get_rekam_medis(id_pasien: str):
    mongo = get_mongo()
    hasil = list(mongo.rekam_medis.find(
        { "id_pasien": id_pasien },
        { "_id": 0 }
    ))
    return hasil

@router.post("/")
def tambah_rekam_medis(
    id_kunjungan: str, id_pasien: str, id_dokter: str,
    tanggal: str, keluhan: str, diagnosis: list,
    tindakan: list, catatan_dokter: str = None,
    hasil_lab: dict = None, foto: list = []
):
    mongo = get_mongo()
    rekam_baru = {
        "id_kunjungan": id_kunjungan,
        "id_pasien": id_pasien,
        "id_dokter": id_dokter,
        "tanggal": tanggal,
        "keluhan": keluhan,
        "diagnosis": diagnosis,
        "tindakan": tindakan,
        "catatan_dokter": catatan_dokter,
        "hasil_lab": hasil_lab,
        "foto": foto
    }
    mongo.rekam_medis.insert_one(rekam_baru)
    return { "message": "Rekam medis berhasil disimpan" }
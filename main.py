from fastapi import FastAPI
from database import engine, Base
from routes import pasien, dokter, antrian, kunjungan, rekam_medis, tagihan, obat

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistem Manajemen Klinik")

app.include_router(pasien.router,      prefix="/pasien",      tags=["Pasien"])
app.include_router(dokter.router,      prefix="/dokter",      tags=["Dokter"])
app.include_router(antrian.router,     prefix="/antrian",     tags=["Antrian"])
app.include_router(kunjungan.router,   prefix="/kunjungan",   tags=["Kunjungan"])
app.include_router(rekam_medis.router, prefix="/rekam-medis", tags=["Rekam Medis"])
app.include_router(tagihan.router,     prefix="/tagihan",     tags=["Tagihan"])
app.include_router(obat.router,        prefix="/obat",        tags=["Obat"])

@app.get("/")
def root():
    return {"message": "Sistem Manajemen Klinik API"}
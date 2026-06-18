import re
from fastapi import HTTPException

ID_PATTERNS = {
    "POL": r"^POL\d{3,}$",
    "DOK": r"^DOK\d{3,}$",
    "STF": r"^STF\d{3,}$",
    "JDW": r"^JDW\d{3,}$",
    "PSN": r"^PSN\d{3,}$",
    "ANT": r"^ANT\d{3,}$",
    "KNJ": r"^KNJ\d{3,}$",
    "OBT": r"^OBT\d{3,}$",
    "RES": r"^RES\d{3,}$",
    "DTL": r"^DTL\d{3,}$",
    "TAG": r"^TAG\d{3,}$",
    "PAY": r"^PAY\d{3,}$",
}

PREFIX_LABELS = {
    "POL": "Poli (contoh: POL001)",
    "DOK": "Dokter (contoh: DOK001)",
    "STF": "Staff (contoh: STF001)",
    "JDW": "Jadwal (contoh: JDW001)",
    "PSN": "Pasien (contoh: PSN001)",
    "ANT": "Antrian (contoh: ANT001)",
    "KNJ": "Kunjungan (contoh: KNJ001)",
    "OBT": "Obat (contoh: OBT001)",
    "RES": "Resep (contoh: RES001)",
    "DTL": "Detail Resep (contoh: DTL001)",
    "TAG": "Tagihan (contoh: TAG001)",
    "PAY": "Pembayaran (contoh: PAY001)",
}

def validate_id(value: str, prefix: str):
    pattern = ID_PATTERNS.get(prefix)
    if not re.match(pattern, value):
        label = PREFIX_LABELS.get(prefix, prefix)
        raise HTTPException(
            status_code=422,
            detail=f"Format ID tidak valid: '{value}'. ID {label} harus diawali '{prefix}' diikuti angka, contoh: {prefix}001"
        )

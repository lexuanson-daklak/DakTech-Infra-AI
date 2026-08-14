from pathlib import Path
import qrcode
OUT=Path(__file__).resolve().parents[1]/"generated"/"qr_codes"
def create_qr(value,filename):
    OUT.mkdir(parents=True,exist_ok=True); p=OUT/filename; qrcode.make(value).save(p); return p

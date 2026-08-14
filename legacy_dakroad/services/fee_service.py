from pathlib import Path
import pandas as pd
F=Path(__file__).resolve().parents[1]/"data"/"fee_rates.csv"
def calculate_fee(zone,purpose,area,start,end):
    df=pd.read_csv(F); m=df[(df.area_zone==zone)&(df.purpose_code==purpose)]
    days=(end-start).days+1
    price=0 if m.empty else int(m.iloc[0].unit_price_vnd_m2_day)
    return {"days":days,"unit_price":price,"total_amount":float(area)*days*price,
            "note":"Kết quả mô phỏng, không phải nghĩa vụ tài chính chính thức."}

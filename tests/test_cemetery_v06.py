from pathlib import Path
import pandas as pd

BASE=Path(__file__).resolve().parent.parent
DATA=BASE/'data'

p=pd.read_csv(DATA/'cemetery_v06_progress.csv')
assert int(p.loc[p.chi_tieu=='Bản ghi ứng viên từ báo cáo','gia_tri'].iloc[0]) == 303
assert int(p.loc[p.chi_tieu=='Nhóm kỹ thuật tên + địa bàn','gia_tri'].iloc[0]) == 267
assert int(p.loc[p.chi_tieu=='Nhóm cùng tên + cùng địa bàn có nhiều dòng','gia_tri'].iloc[0]) == 20
assert int(p.loc[p.chi_tieu=='Bản ghi trong nhóm cùng tên + cùng địa bàn','gia_tri'].iloc[0]) == 56
assert int(p.loc[p.chi_tieu=='Đã xác minh chính thức','gia_tri'].iloc[0]) == 0
pri=pd.read_csv(DATA/'cemetery_v06_review_priority.csv')
assert pri.so_ban_ghi.sum() == 303
print('PASS cemetery v0.6 public aggregate checks')

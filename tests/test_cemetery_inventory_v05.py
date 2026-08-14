from pathlib import Path
import pandas as pd

BASE=Path(__file__).resolve().parent.parent
summary=pd.read_csv(BASE/'data'/'cemetery_candidate_summary_v0.5.csv')
status=pd.read_csv(BASE/'data'/'cemetery_candidate_status_v0.5.csv')
types=pd.read_csv(BASE/'data'/'cemetery_candidate_type_v0.5.csv')

vals=dict(zip(summary['chi_tieu'],summary['gia_tri']))
assert int(vals['Bản ghi ứng viên chưa xác minh']) == 303
assert int(vals['Khóa định danh ứng viên khác nhau']) == 267
assert int(vals['Nhóm có khả năng trùng cần rà soát']) == 20
assert int(vals['Bản ghi nằm trong nhóm có khả năng trùng']) == 56
assert int(vals['Bản ghi đã xác minh']) == 0
assert int(status['so_ban_ghi'].sum()) == 303
assert int(types['so_ban_ghi'].sum()) == 303
print('test_cemetery_inventory_v05: PASS')

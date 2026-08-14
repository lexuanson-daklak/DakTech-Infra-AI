ALLOWED={"TRONG_GIU_XE","KINH_DOANH_DICH_VU","TAP_KET_VAT_LIEU","SU_KIEN","KHAC"}
def evaluate_application(data,asset):
    out=[]
    def add(r,s,m): out.append({"rule_id":r,"status":s,"message":m})
    if not data.get("asset_code"): add("R01","FAIL","Chưa xác định vị trí.")
    if float(data.get("requested_area_m2",0))<=0: add("R02","FAIL","Diện tích phải lớn hơn 0.")
    if float(data.get("requested_area_m2",0))>float(asset.get("usable_area_m2",0)): add("R03","REVIEW","Vượt diện tích khả dụng.")
    if data["end_date"]<data["start_date"]: add("R04","FAIL","Ngày kết thúc trước ngày bắt đầu.")
    if not data.get("has_image"): add("R05","REVIEW","Thiếu ảnh hiện trạng.")
    if data.get("purpose_code") not in ALLOWED: add("R06","REVIEW","Mục đích chưa chuẩn hóa.")
    if asset.get("status")!="ACTIVE": add("R07","FAIL","Vị trí chưa được kích hoạt.")
    if (data["end_date"]-data["start_date"]).days+1>30: add("R08","REVIEW","Thời hạn vượt 30 ngày.")
    if data.get("purpose_code") in {"TAP_KET_VAT_LIEU","SU_KIEN"}: add("R09","REVIEW","Cần kiểm tra an toàn giao thông.")
    if not data.get("applicant_name") or not data.get("phone_number"): add("R10","FAIL","Thiếu thông tin người đề nghị.")
    allowed=set(filter(None,asset.get("allowed_purposes","").split("|")))
    if allowed and data.get("purpose_code") not in allowed: add("R11","REVIEW","Mục đích chưa phù hợp vị trí.")
    fail=any(x["status"]=="FAIL" for x in out); review=any(x["status"]=="REVIEW" for x in out)
    overall="KHONG_TIEP_NHAN" if fail else ("CAN_BO_XEM_XET" if review else "DE_XUAT_TIEP_NHAN")
    return {"overall_status":overall,"rule_results":out,
            "recommended_action":"Khắc phục lỗi bắt buộc." if fail else ("Cán bộ xem xét cảnh báo." if review else "Có thể tiếp nhận."),
            "disclaimer":"Kết quả chỉ hỗ trợ tham khảo."}

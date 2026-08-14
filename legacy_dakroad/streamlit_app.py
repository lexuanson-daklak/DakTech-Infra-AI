from pathlib import Path
from datetime import date
import json
import pandas as pd
import pydeck as pdk
import streamlit as st
from database.init_database import init_db
from database.repository import connect
from services.auth_service import authenticate
from services.rule_engine import evaluate_application
from services.fee_service import calculate_fee
from services.application_service import create_application,list_applications,update_status
from services.qr_service import create_qr
from services.ai_service import assess_application
from services.official_fee_service import load_rates, calculate_nq24, calculate_nq35

BASE=Path(__file__).resolve().parent
if not (BASE/"database"/"dakroad.db").exists(): init_db()
st.set_page_config(page_title="DakRoad AI",page_icon="🛣️",layout="wide")
DISCLAIMER="SẢN PHẨM DEMO PHỤC VỤ CUỘC THI – DỮ LIỆU VÀ KẾT QUẢ KHÔNG CÓ GIÁ TRỊ PHÁP LÝ."
PURPOSES={"TRONG_GIU_XE":"Trông giữ xe","KINH_DOANH_DICH_VU":"Kinh doanh dịch vụ","TAP_KET_VAT_LIEU":"Tập kết vật liệu","SU_KIEN":"Tổ chức sự kiện","KHAC":"Mục đích khác"}

def assets():
    with connect() as c: return pd.read_sql_query("SELECT * FROM assets ORDER BY id",c)

def login():
    st.title("🛣️ DakRoad AI")
    st.subheader("Nền tảng quản trị tài sản đường bộ và hỗ trợ xử lý sử dụng tạm thời lòng đường, hè phố")
    st.info("Phiên bản 0.6.3 sử dụng Rule Engine có thể giải thích; kết quả nộp hồ sơ được lưu ổn định sau khi giao diện tải lại.")
    st.error(DISCLAIMER)
    with st.form("login"):
        u=st.text_input("Tên đăng nhập",value="nguoidan_demo")
        p=st.text_input("Mật khẩu",value="DakRoad@2026",type="password")
        ok=st.form_submit_button("Đăng nhập")
    if ok:
        user=authenticate(u,p)
        if user: st.session_state.update(authenticated=True,user=user); st.rerun()
        st.error("Sai tài khoản hoặc mật khẩu.")

def map_page():
    st.header("Bản đồ tài sản mô phỏng"); df=assets()
    a,b=st.columns([2,1])
    with a:
        layer=pdk.Layer("ScatterplotLayer",data=df,get_position="[longitude,latitude]",get_radius=55,pickable=True)
        view=pdk.ViewState(latitude=df.latitude.mean(),longitude=df.longitude.mean(),zoom=12)
        st.pydeck_chart(pdk.Deck(layers=[layer],initial_view_state=view,tooltip={"html":"<b>{asset_code}</b><br/>{asset_name}<br/>{status}"}))
    with b:
        code=st.selectbox("Chọn vị trí",df.asset_code); r=df[df.asset_code==code].iloc[0]
        st.write(f"**{r.asset_name}**"); st.write(r.road_name); st.write(f"Diện tích khả dụng: {r.usable_area_m2} m²"); st.write(f"Trạng thái: {r.status}")

def create_page():
    st.header("Tạo hồ sơ")
    st.error(DISCLAIMER)

    df = assets()
    shown = df[df.status.isin(["ACTIVE", "RESTRICTED"])]
    labels = {
        f"{r.asset_code} – {r.asset_name}": r.asset_code
        for _, r in shown.iterrows()
    }

    # Không dùng st.form tại trang này để tránh kết quả bị mất khi giao diện tự rerun.
    label = st.selectbox("Vị trí", list(labels), key="create_asset")
    name = st.text_input(
        "Người đề nghị",
        value="Người đề nghị Demo",
        key="create_name",
    )
    phone = st.text_input(
        "Số điện thoại mô phỏng",
        value="0900000000",
        key="create_phone",
    )
    p_label = st.selectbox(
        "Mục đích",
        list(PURPOSES.values()),
        key="create_purpose",
    )
    area = st.number_input(
        "Diện tích (m²)",
        min_value=0.0,
        value=20.0,
        key="create_area",
    )

    c1, c2 = st.columns(2)
    start_date = c1.date_input(
        "Từ ngày",
        date.today(),
        key="create_start",
    )
    end_date = c2.date_input(
        "Đến ngày",
        date.today(),
        key="create_end",
    )

    desc = st.text_area(
        "Mô tả",
        value="Tình huống mô phỏng.",
        key="create_desc",
    )
    image = st.file_uploader(
        "Ảnh hiện trạng",
        type=["jpg", "jpeg", "png"],
        key="create_image",
    )

    submitted = st.button(
        "Kiểm tra và nộp",
        type="primary",
        key="create_submit",
    )

    if submitted:
        try:
            asset_code = labels[label]
            asset = shown[shown.asset_code == asset_code].iloc[0].to_dict()
            purpose = next(
                code for code, value in PURPOSES.items()
                if value == p_label
            )
            payload = {
                "asset_code": asset_code,
                "asset_id": int(asset["id"]),
                "applicant_name": name.strip(),
                "phone_number": phone.strip(),
                "purpose_code": purpose,
                "requested_area_m2": area,
                "start_date": start_date,
                "end_date": end_date,
                "description": desc.strip(),
                "has_image": image is not None,
            }

            rule_result = evaluate_application(payload, asset)
            result = assess_application(rule_result, payload)
            fee = calculate_fee(
                asset["area_zone"],
                purpose,
                area,
                start_date,
                end_date,
            )

            submission = {
                "result": result,
                "fee": fee,
                "rule_status": rule_result["overall_status"],
                "application_code": None,
                "error": None,
            }

            if rule_result["overall_status"] != "KHONG_TIEP_NHAN":
                submission["application_code"] = create_application(
                    st.session_state.user["id"],
                    payload,
                    result,
                    fee,
                )

            st.session_state["last_submission"] = submission

        except Exception as exc:
            st.session_state["last_submission"] = {
                "result": None,
                "fee": None,
                "rule_status": None,
                "application_code": None,
                "error": f"{type(exc).__name__}: {exc}",
            }

    # Kết quả được giữ trong session_state nên không biến mất sau rerun.
    submission = st.session_state.get("last_submission")
    if submission:
        st.divider()
        st.subheader("Kết quả hỗ trợ kiểm tra")

        if submission.get("error"):
            st.error(
                "Hệ thống chưa thể lưu hồ sơ. "
                f"Chi tiết kỹ thuật: {submission['error']}"
            )
        else:
            st.json(submission["result"])
            st.write(
                "Khoản thu mô phỏng: "
                f"**{submission['fee']['total_amount']:,.0f} đồng**"
            )

            if submission["rule_status"] == "KHONG_TIEP_NHAN":
                st.error("Hồ sơ có lỗi bắt buộc.")
            elif submission.get("application_code"):
                st.success(
                    "Đã tạo hồ sơ "
                    f"**{submission['application_code']}**"
                )

def review_page():
    if st.session_state.user["role"] not in {"OFFICER","MANAGER"}: st.error("Không có quyền."); return
    st.header("Kiểm tra và xử lý hồ sơ"); rows=list_applications()
    if not rows: st.info("Chưa có hồ sơ."); return
    opts={f"{r['application_code']} – {r['status']}":r for r in rows}; r=opts[st.selectbox("Hồ sơ",list(opts))]
    c1,c2=st.columns(2)
    with c1:
        st.write(f"**{r['application_code']}**"); st.write(f"Vị trí: {r['asset_code']}"); st.write(f"Diện tích: {r['requested_area_m2']} m²")
        st.write(f"Khoản thu mô phỏng: {r['fee_amount']:,.0f} đồng")
    with c2:
        st.json(json.loads(r["ai_result_json"]) if r["ai_result_json"] else {})
    note=st.text_area("Ý kiến cán bộ",value="Đã xem xét trên dữ liệu mô phỏng.")
    status=st.radio("Xử lý",["YEU_CAU_BO_SUNG","TU_CHOI","DA_CHAP_THUAN"],horizontal=True)
    if st.button("Lưu xử lý"):
        permit=update_status(r["application_code"],status,note); st.success(f"Đã cập nhật. {permit or ''}"); st.rerun()

def permit_page():
    st.header("Giấy phép QR mô phỏng"); rows=[r for r in list_applications() if r.get("permit_code")]
    if not rows: st.info("Chưa có giấy phép."); return
    opts={f"{r['permit_code']} – {r['application_code']}":r for r in rows}; r=opts[st.selectbox("Chọn",list(opts))]
    p=create_qr(f"DAKROAD-DEMO|{r['permit_code']}|{r['application_code']}",f"{r['permit_code']}.png")
    st.error("SẢN PHẨM DEMO – KHÔNG CÓ GIÁ TRỊ PHÁP LÝ")
    st.write(f"**{r['permit_code']}**"); st.write(f"{r['asset_code']} – {r['asset_name']}"); st.write(f"{r['start_date']} đến {r['end_date']}")
    st.image(str(p),width=220)

def dashboard():
    if st.session_state.user["role"]!="MANAGER": st.error("Chỉ tài khoản lãnh đạo."); return
    st.header("Dashboard"); a=assets(); rows=list_applications(); df=pd.DataFrame(rows)
    c1,c2,c3=st.columns(3); c1.metric("Tài sản mẫu",len(a)); c2.metric("Hồ sơ",len(df)); c3.metric("Tiền mô phỏng","0 đồng" if df.empty else f"{df.fee_amount.sum():,.0f} đồng")
    if not df.empty: st.bar_chart(df.status.value_counts()); st.dataframe(df[["application_code","asset_code","requested_area_m2","status","fee_amount"]],use_container_width=True)


def legal_data_page():
    st.header("Kho dữ liệu pháp lý và đề xuất địa phương")
    st.warning("Hệ thống tách riêng văn bản chính thức, hồ sơ đề xuất và dữ liệu thực tiễn. Không dùng đề án cấp xã như mức thu đã có hiệu lực.")
    sources = pd.read_csv(BASE / "data" / "legal_sources.csv")
    proposals = pd.read_csv(BASE / "data" / "local_proposals_2026.csv")
    flags = pd.read_csv(BASE / "data" / "legal_review_flags.csv")
    detail = pd.read_csv(BASE / "data" / "proposal_rate_details_2026.csv")
    quality = pd.read_csv(BASE / "data" / "data_quality_issues.csv")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nguồn hồ sơ", len(sources))
    c2.metric("Địa phương/đề xuất", len(proposals))
    c3.metric("Dòng mức thu đề xuất", len(detail))
    c4.metric("Vấn đề chất lượng dữ liệu", len(quality))
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Nguồn văn bản", "Đề xuất địa phương 2026", "Chi tiết mức đề xuất", "Chất lượng dữ liệu", "Điểm cần thẩm định"])
    with tab1:
        st.dataframe(sources[["source_id","document_no","date","issuer","document_type","territory","status","summary"]], use_container_width=True)
    with tab2:
        st.dataframe(proposals[["locality","proposal_type","fee_summary","revenue_mechanism","status","estimated_revenue_vnd","legal_review"]], use_container_width=True)
    with tab3:
        st.dataframe(detail, use_container_width=True)
    with tab4:
        st.dataframe(quality, use_container_width=True)
    with tab5:
        st.dataframe(flags, use_container_width=True)
    st.caption("Legal Version Control Layer: văn bản gốc -> phiên bản/chế độ áp dụng -> địa bàn -> quy tắc -> hồ sơ liên quan.")

def official_fee_lookup_page():
    st.header("Tra cứu và tính thử mức thu từ nguồn chính thức")
    st.error("Kết quả phục vụ kiểm chứng dữ liệu. Việc áp dụng thực tế phải xác định đúng địa bàn, thời điểm, hiệu lực và văn bản chuyển tiếp.")
    policy = st.selectbox("Nguồn dữ liệu", ["NQ24/2024 - Đắk Lắk trước sắp xếp", "NQ35/2022 - Phú Yên trước sắp xếp"])
    rates = load_rates()
    if policy.startswith("NQ24"):
        labels = {
            "Bãi trông, giữ xe đạp, xe máy":"BIKE_MOTORBIKE_PARKING",
            "Đỗ xe ô tô theo lượt":"CAR_PARKING_TRIP",
            "Đỗ xe ô tô theo tháng":"CAR_PARKING_MONTH",
            "Tập kết vật liệu từ 15 ngày trở lên":"MATERIAL_15PLUS",
            "Tập kết vật liệu dưới 15 ngày":"MATERIAL_UNDER15",
        }
        label = st.selectbox("Nội dung", list(labels))
        code = labels[label]
        condition = ""; locality = ""; quantity=1.0; periods=1.0
        if code == "BIKE_MOTORBIKE_PARKING":
            bands = {
                "Giá đất từ 25 triệu đồng/m2 trở lên":"LAND_GE_25M",
                "Từ 20 đến dưới 25 triệu đồng/m2":"LAND_20_25M",
                "Từ 15 đến dưới 20 triệu đồng/m2":"LAND_15_20M",
                "Từ 10 đến dưới 15 triệu đồng/m2":"LAND_10_15M",
                "Từ 5 đến dưới 10 triệu đồng/m2":"LAND_5_10M",
                "Dưới 5 triệu đồng/m2":"LAND_LT_5M",
            }
            condition = bands[st.selectbox("Nhóm giá đất", list(bands))]
            quantity = st.number_input("Diện tích (m2)", min_value=0.0, value=20.0)
            periods = st.number_input("Số tháng", min_value=0.0, value=1.0)
        elif code == "CAR_PARKING_TRIP":
            quantity = st.number_input("Số xe", min_value=0.0, value=1.0)
            periods = st.number_input("Số lượt/xe", min_value=0.0, value=1.0)
        elif code == "CAR_PARKING_MONTH":
            quantity = st.number_input("Số xe", min_value=0.0, value=1.0)
            periods = st.number_input("Số tháng", min_value=0.0, value=1.0)
        elif code == "MATERIAL_15PLUS":
            locality = st.selectbox("Nhóm địa bàn", ["BUON_MA_THUOT","DISTRICT_TOWN"])
            quantity = st.number_input("Diện tích (m2)", min_value=0.0, value=20.0)
            periods = st.number_input("Số tháng", min_value=0.0, value=1.0)
        else:
            locality = st.selectbox("Nhóm địa bàn", ["BUON_MA_THUOT","DISTRICT_TOWN"])
            quantity = st.number_input("Diện tích (m2)", min_value=0.0, value=20.0)
            periods = st.number_input("Số đợt sử dụng dưới 15 ngày", min_value=0.0, value=1.0)
        result = calculate_nq24(code, quantity, periods, condition, locality)
    else:
        df = rates[rates.policy_code == "NQ35_2022_PHUYEN_FORMER"]
        locality = st.selectbox("Địa phương", sorted(df.locality.unique()))
        positions = sorted(df[df.locality == locality].position.unique())
        position = st.selectbox("Vị trí", positions)
        purposes = df[(df.locality == locality) & (df.position == position)][["purpose_code","purpose_name"]].drop_duplicates()
        pmap = dict(zip(purposes.purpose_name, purposes.purpose_code))
        purpose_label = st.selectbox("Nội dung sử dụng", list(pmap))
        area = st.number_input("Diện tích (m2)", min_value=0.0, value=20.0)
        months = st.number_input("Số tháng", min_value=0.0, value=1.0)
        result = calculate_nq35(locality, position, pmap[purpose_label], area, months)
    if result.get("ok"):
        st.metric("Kết quả tính theo dữ liệu nguồn", f"{result['total']:,.0f} đồng")
        st.write(f"Mức thu: **{result['rate']:,.0f}** - Đơn vị: `{result['unit']}`")
        st.write(f"Nguồn: `{result['source_id']}`")
        if result.get("notes"): st.caption(result['notes'])
    else:
        st.warning(result.get("message"))


def main():
    if not st.session_state.get("authenticated"): login(); return
    u=st.session_state.user; st.sidebar.success(f"{u['full_name']} ({u['role']})")
    pages=["Bản đồ","Tạo hồ sơ","Tra cứu mức thu","Kho dữ liệu pháp lý"]
    if u["role"] in {"OFFICER","MANAGER"}: pages.append("Xử lý")
    pages.append("Giấy phép QR")
    if u["role"]=="MANAGER": pages.append("Dashboard")
    page=st.sidebar.radio("Chức năng",pages)
    if st.sidebar.button("Đăng xuất"): st.session_state.clear(); st.rerun()
    st.sidebar.caption(DISCLAIMER)
    st.sidebar.markdown("---")
    st.sidebar.caption("Phiên bản: MVP v0.6.2 - sửa lỗi trùng mã hồ sơ")
    st.sidebar.caption("Trạng thái: Rule Engine + hỗ trợ tự động có cấu trúc")
    {"Bản đồ":map_page,"Tạo hồ sơ":create_page,"Tra cứu mức thu":official_fee_lookup_page,"Kho dữ liệu pháp lý":legal_data_page,"Xử lý":review_page,"Giấy phép QR":permit_page,"Dashboard":dashboard}[page]()
if __name__=="__main__": main()

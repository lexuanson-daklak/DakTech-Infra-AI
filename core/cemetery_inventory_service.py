from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import DATA_DIR

SOURCE_TYPE_LABELS = {
    "LOCAL_INVENTORY_REPORT": "Báo cáo kiểm kê/hiện trạng địa phương",
    "LOCAL_IMPLEMENTATION_DIRECTIVE": "Văn bản triển khai của địa phương",
    "CANCELLED_LOCAL_REPORT": "Báo cáo địa phương đã hủy/xin lấy lại",
    "LOCAL_PLANNING_CONTEXT": "Hồ sơ quy hoạch/mở rộng của địa phương",
    "LOCAL_CLOSURE_DECISION": "Quyết định đóng cửa/chuyển trạng thái",
    "OPERATOR_REPORT": "Báo cáo đơn vị vận hành",
    "KKT_RELOCATION_CONTEXT": "Hồ sơ bối cảnh khu kinh tế/di dời",
}
DATA_USE_LABELS = {
    "PROVISIONAL_EXTRACTED": "Dữ liệu tách sơ bộ",
    "CONTEXT_ONLY": "Chỉ dùng làm bối cảnh/nguồn tham khảo",
    "SUMMARY_ONLY_NEEDS_DETAIL": "Mới có số liệu tổng hợp, cần chi tiết",
    "EXCLUDED_CANCELLED": "Loại khỏi lớp dữ liệu sử dụng do nguồn đã hủy",
    "CONTEXT_EXTRACTED": "Đã tách một phần thông tin bối cảnh",
}
VERIFY_LABELS = {
    "NOT_VERIFIED_BY_SXD": "Chưa được Sở Xây dựng xác minh",
    "NOT_VERIFIED": "Chưa xác minh",
    "VERIFIED": "Đã xác minh",
}
STATUS_LABELS = {
    "ACTIVE": "Đang sử dụng/hoạt động theo dữ liệu nguồn",
    "REVIEW": "Cần rà soát",
    "CLOSED": "Đã đóng cửa/chuyển trạng thái theo nguồn",
    "PLANNED": "Dự kiến/quy hoạch",
    "UNKNOWN": "Chưa rõ",
}
TYPE_LABELS = {
    "NGHIA_TRANG": "Tên nguồn có cụm 'nghĩa trang'",
    "NGHIA_DIA": "Tên nguồn có cụm 'nghĩa địa'",
    "KHU_MAI_TANG": "Tên nguồn có cụm 'khu mai táng'",
    "CHUA_RO_LOAI_HINH": "Tên nguồn chưa đủ rõ để phân loại",
}


def _read(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def load_candidate_summary() -> pd.DataFrame:
    return _read("cemetery_candidate_summary_v0.5.csv")


def load_candidate_status() -> pd.DataFrame:
    return _read("cemetery_candidate_status_v0.5.csv")


def load_candidate_type() -> pd.DataFrame:
    return _read("cemetery_candidate_type_v0.5.csv")


def load_collection_status() -> pd.DataFrame:
    df = _read("cemetery_collection_status_v0.4.csv")
    if df.empty:
        return df
    out = df.copy()
    if "source_type" in out:
        out["source_type"] = out["source_type"].map(SOURCE_TYPE_LABELS).fillna(out["source_type"])
    if "data_use_status" in out:
        out["data_use_status"] = out["data_use_status"].map(DATA_USE_LABELS).fillna(out["data_use_status"])
    if "verification_status" in out:
        out["verification_status"] = out["verification_status"].map(VERIFY_LABELS).fillna(out["verification_status"])
    return out


def metric_from_summary(label: str, default=0):
    df = load_candidate_summary()
    if df.empty:
        return default
    hit = df[df["chi_tieu"] == label]
    if hit.empty:
        return default
    return hit.iloc[0]["gia_tri"]

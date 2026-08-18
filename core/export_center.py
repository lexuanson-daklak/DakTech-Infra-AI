from __future__ import annotations

from datetime import datetime
from io import BytesIO
import json
import zipfile

import pandas as pd
import streamlit as st


STATUS_VI = {
    "ACTIVE": "Đang hoạt động",
    "REVIEW": "Cần rà soát",
    "RESTRICTED": "Hạn chế",
    "LIMITED": "Giới hạn",
    "CLOSED": "Đã đóng",
    "PLANNED": "Quy hoạch/dự kiến",
    "INACTIVE": "Không hoạt động",
}


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _json_default(value):
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def json_bytes(df: pd.DataFrame) -> bytes:
    records = df.where(pd.notna(df), None).to_dict(orient="records")
    return json.dumps(records, ensure_ascii=False, indent=2, default=_json_default).encode("utf-8")


def excel_bytes(
    datasets: dict[str, pd.DataFrame],
    metadata: dict | None = None,
    data_dictionary: pd.DataFrame | None = None,
) -> bytes:
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        used = set()
        for name, df in datasets.items():
            sheet = str(name)[:31] or "Data"
            base = sheet
            i = 2
            while sheet in used:
                suffix = f"_{i}"
                sheet = (base[:31-len(suffix)] + suffix)
                i += 1
            used.add(sheet)
            df.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.book[sheet]
            ws.freeze_panes = "A2"
            for col in ws.columns:
                max_len = max((len(str(cell.value)) if cell.value is not None else 0) for cell in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(max_len + 2, 12), 42)

        if metadata:
            meta_df = pd.DataFrame(
                [{"Trường": k, "Giá trị": v} for k, v in metadata.items()]
            )
            meta_df.to_excel(writer, sheet_name="Thong_tin_xuat", index=False)

        if data_dictionary is not None and not data_dictionary.empty:
            data_dictionary.to_excel(writer, sheet_name="Tu_dien_du_lieu", index=False)

    return bio.getvalue()


def geojson_bytes(
    df: pd.DataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
) -> bytes | None:
    if lat_col not in df.columns or lon_col not in df.columns:
        return None

    work = df.copy()
    work[lat_col] = pd.to_numeric(work[lat_col], errors="coerce")
    work[lon_col] = pd.to_numeric(work[lon_col], errors="coerce")
    work = work.dropna(subset=[lat_col, lon_col])
    if work.empty:
        return None

    features = []
    for _, row in work.iterrows():
        props = {}
        for key, value in row.items():
            if key in (lat_col, lon_col):
                continue
            if pd.isna(value):
                props[key] = None
            else:
                props[key] = _json_default(value)
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row[lon_col]), float(row[lat_col])],
            },
            "properties": props,
        })

    obj = {"type": "FeatureCollection", "features": features}
    return json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")


def zip_bundle(
    module_slug: str,
    datasets: dict[str, pd.DataFrame],
    metadata: dict,
    data_dictionary: pd.DataFrame | None = None,
) -> bytes:
    bio = BytesIO()
    ts = _timestamp()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as z:
        for name, df in datasets.items():
            stem = f"{module_slug}_{name}_{ts}"
            z.writestr(f"data/{stem}.csv", csv_bytes(df))
            z.writestr(f"data/{stem}.json", json_bytes(df))
            gj = geojson_bytes(df)
            if gj:
                z.writestr(f"data/{stem}.geojson", gj)

        xlsx = excel_bytes(datasets, metadata=metadata, data_dictionary=data_dictionary)
        z.writestr(f"{module_slug}_FULL_DATA_{ts}.xlsx", xlsx)

        manifest = {
            "module": module_slug,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "datasets": {k: int(len(v)) for k, v in datasets.items()},
            "metadata": metadata,
        }
        z.writestr(
            "manifest.json",
            json.dumps(manifest, ensure_ascii=False, indent=2, default=_json_default).encode("utf-8"),
        )

        if data_dictionary is not None and not data_dictionary.empty:
            z.writestr("data_dictionary.csv", csv_bytes(data_dictionary))

        readme = f"""TRUNG TÂM XUẤT DỮ LIỆU – {module_slug}

Gói này được tạo trực tiếp từ Streamlit.
Người dùng không cần vào GitHub để lấy dữ liệu.

Nguyên tắc:
- Dữ liệu xuất ra tuân theo bộ lọc và quyền truy cập hiện hành.
- Bản Public chỉ được xuất dữ liệu mẫu/tổng hợp an toàn.
- Dữ liệu nội bộ/chính thức chỉ được xuất trong môi trường nội bộ có phân quyền.
- Trạng thái xác minh và nguồn dữ liệu phải được giữ kèm nếu có.

Thời điểm tạo: {datetime.now().isoformat(timespec="seconds")}
"""
        z.writestr("README.txt", readme.encode("utf-8"))
    return bio.getvalue()


def render_export_center(
    *,
    module_name: str,
    module_slug: str,
    description: str,
    datasets: dict[str, pd.DataFrame],
    metadata: dict,
    data_dictionary: pd.DataFrame | None = None,
    public_demo: bool = True,
):
    st.title(f"📤 Trung tâm xuất dữ liệu – {module_name}")
    st.caption(description)

    if public_demo:
        st.warning(
            "Đây là bản Public/Demo. Chỉ dữ liệu mẫu hoặc dữ liệu tổng hợp an toàn được phép tải xuống. "
            "Dữ liệu nội bộ phải dùng môi trường có phân quyền."
        )

    names = list(datasets.keys())
    selected = st.selectbox("Chọn bảng dữ liệu", names)
    df = datasets[selected]

    st.subheader("Xem trước dữ liệu sẽ xuất")
    st.caption(f"{len(df):,} dòng · {len(df.columns)} cột")
    st.dataframe(df.head(200), width="stretch", hide_index=True)

    ts = _timestamp()
    base = f"{module_slug}_{selected}_{ts}"

    c1, c2, c3, c4 = st.columns(4)
    c1.download_button(
        "⬇️ CSV",
        data=csv_bytes(df),
        file_name=f"{base}.csv",
        mime="text/csv",
        width="stretch",
    )
    c2.download_button(
        "⬇️ Excel",
        data=excel_bytes({selected: df}, metadata=metadata, data_dictionary=data_dictionary),
        file_name=f"{base}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch",
    )
    c3.download_button(
        "⬇️ JSON",
        data=json_bytes(df),
        file_name=f"{base}.json",
        mime="application/json",
        width="stretch",
    )

    gj = geojson_bytes(df)
    if gj:
        c4.download_button(
            "⬇️ GeoJSON",
            data=gj,
            file_name=f"{base}.geojson",
            mime="application/geo+json",
            width="stretch",
        )
    else:
        c4.button("GeoJSON: chưa có tọa độ", disabled=True, width="stretch")

    st.divider()
    st.subheader("Tải trọn bộ dữ liệu")
    st.write(
        "Gói đầy đủ gồm: CSV + JSON + GeoJSON (nếu có tọa độ) + Excel nhiều sheet "
        "+ từ điển dữ liệu + manifest + README."
    )
    bundle = zip_bundle(
        module_slug=module_slug,
        datasets=datasets,
        metadata=metadata,
        data_dictionary=data_dictionary,
    )
    st.download_button(
        "📦 Tải FULL DATA PACKAGE (.zip)",
        data=bundle,
        file_name=f"{module_slug}_FULL_DATA_{ts}.zip",
        mime="application/zip",
        type="primary",
        width="stretch",
    )

    with st.expander("Thông tin kèm theo dữ liệu xuất"):
        st.json(metadata)
        if data_dictionary is not None and not data_dictionary.empty:
            st.dataframe(data_dictionary, width="stretch", hide_index=True)

from __future__ import annotations

import pandas as pd
import pydeck as pdk
import streamlit as st


def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        col.metric(label, value, help=help_text)


def point_map(df: pd.DataFrame, tooltip_fields: list[str] | None = None, zoom: float = 7.0):
    if df.empty or not {"latitude", "longitude"}.issubset(df.columns):
        st.info("Chưa có dữ liệu tọa độ để hiển thị bản đồ.")
        return
    map_df = df.dropna(subset=["latitude", "longitude"]).copy()
    if map_df.empty:
        st.info("Chưa có tọa độ hợp lệ để hiển thị bản đồ.")
        return
    tooltip_fields = tooltip_fields or [c for c in ["asset_code", "asset_name", "status"] if c in map_df.columns]
    html = "<br/>".join([f"<b>{c}</b>: {{{c}}}" for c in tooltip_fields])
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[longitude, latitude]",
        get_radius=180,
        pickable=True,
        auto_highlight=True,
    )
    view = pdk.ViewState(
        latitude=float(map_df["latitude"].mean()),
        longitude=float(map_df["longitude"].mean()),
        zoom=zoom,
    )
    st.pydeck_chart(
        pdk.Deck(layers=[layer], initial_view_state=view, tooltip={"html": html}),
        use_container_width=True,
    )


def status_table(df: pd.DataFrame, columns: list[str]):
    cols = [c for c in columns if c in df.columns]
    st.dataframe(df[cols], use_container_width=True, hide_index=True)


def show_key_value(record: pd.Series, fields: list[tuple[str, str]]):
    rows = []
    for field, label in fields:
        value = record.get(field, "")
        if pd.isna(value):
            value = ""
        rows.append({"Nội dung": label, "Thông tin": value})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

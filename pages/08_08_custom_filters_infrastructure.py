import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="Custom Filters for Infrastructure", layout="wide")

st.title("Custom Filters for Infrastructure")

st.markdown(
    """
### 📌 概要

このページでは、OpenStreetMapのタグを活用して、道路やインフラ以外の要素（例えばトンネル・橋・サービスエリアなど）を**カスタムクエリ**で抽出・可視化する方法を学びます。

---

### 🛠 使用する主な関数の解説

- `ox.features_from_place(place, tags)`：指定した地名とタグ条件に基づいて、OSMから特定の施設をGeoDataFrameとして取得します。
- `ox.geocode_to_gdf(place)`：対象都市のポリゴン（境界形状）を取得します。

---

### ⚙️ 実行
"""
)

with st.form("infra_form"):
    place = st.text_input(
        "都市名またはエリア（例: Shibuya, Tokyo, Japan）", value="Shibuya, Tokyo, Japan"
    )
    submitted = st.form_submit_button("施設データを取得")

if submitted:
    with st.spinner("データを取得中..."):
        polygon = ox.geocode_to_gdf(place)

        # インフラ施設の抽出例
        tags = {"man_made": True, "power": True, "waterway": True}
        gdf = ox.features_from_place(place, tags=tags)

        st.success("インフラ関連の要素を取得しました。")

        fig, ax = plt.subplots(figsize=(8, 8))
        polygon.plot(ax=ax, facecolor="white", edgecolor="black", linewidth=1, zorder=1)
        gdf.plot(ax=ax, markersize=5, color="red", zorder=2)
        st.pyplot(fig)

        st.dataframe(
            gdf[["name", "man_made", "power", "waterway"]].dropna(how="all", axis=1)
        )

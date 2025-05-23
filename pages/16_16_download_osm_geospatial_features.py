import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="Download OSM Geospatial Features", layout="wide")

st.title("Download OSM Geospatial Features")

st.markdown(
    """
### 📌 概要

このページでは、OpenStreetMapの指定したタグに基づく**地物データ（建物、道路、施設など）**を取得・可視化します。

---

### 🛠 使用する主な関数の解説

- `ox.features_from_place(place, tags)`：地名とタグを指定して、対応するOSMの地物をGeoDataFrameとして取得します。
- `ox.geocode_to_gdf(place)`：エリアの境界ポリゴンを取得し、背景として重ねて表示します。

---

### ⚙️ 実行
"""
)

with st.form("features_form"):
    place = st.text_input(
        "対象地域名（例: Shibuya, Tokyo, Japan）", value="Shibuya, Tokyo, Japan"
    )
    key = st.selectbox(
        "OSMキー（例: building, highway, amenity など）",
        ["building", "highway", "amenity", "shop", "landuse"],
        index=0,
    )
    submitted = st.form_submit_button("データを取得")

if submitted:
    with st.spinner("地物データ取得中..."):
        tags = {key: True}
        gdf = ox.features_from_place(place, tags=tags)
        boundary = ox.geocode_to_gdf(place)

        st.success(f"取得完了：{len(gdf)} 件の「{key}」地物")

        st.subheader(f"{key} 地物の分布")
        fig, ax = plt.subplots(figsize=(8, 8))
        boundary.plot(ax=ax, facecolor="white", edgecolor="black", linewidth=1)
        gdf.plot(ax=ax, color="blue", markersize=2)
        ax.set_title(f"OSM features: {key}")
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("属性テーブル（抜粋）")
        st.dataframe(gdf.head(20))

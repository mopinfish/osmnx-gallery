import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="Building Footprints", layout="wide")

st.title("Building Footprints Viewer")

st.markdown(
    """
### 📌 概要

このページでは、指定した都市または地域に存在する**建物のフットプリント（建物輪郭）**をOpenStreetMapから取得し、可視化します。

---

### 🛠 使用する主な関数の解説

- `ox.features_from_place(place, tags={"building": True})`：対象地域内の建物ポリゴンを取得します。
- `ox.geocode_to_gdf(place)`：地域の境界ポリゴンを取得します。
- `matplotlib` を使って建物密度や配置を地図上に表示します。

---

### ⚙️ 実行
"""
)

with st.form("building_form"):
    place = st.text_input(
        "都市名またはエリア（例: Shibuya, Tokyo, Japan）", value="Shibuya, Tokyo, Japan"
    )
    submitted = st.form_submit_button("建物データを取得・表示")

if submitted:
    with st.spinner("データ取得中..."):
        boundary = ox.geocode_to_gdf(place)
        buildings = ox.features_from_place(place, tags={"building": True})

        st.success("建物データを取得しました。")

        st.subheader("建物フットプリントの可視化")
        fig, ax = plt.subplots(figsize=(8, 8))
        boundary.plot(
            ax=ax, facecolor="white", edgecolor="black", linewidth=1, zorder=1
        )
        buildings.plot(ax=ax, facecolor="skyblue", edgecolor="none", zorder=2)
        ax.set_title(f"Buildings in {place}")
        ax.axis("off")
        st.pyplot(fig)

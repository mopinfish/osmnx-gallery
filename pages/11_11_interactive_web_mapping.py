import streamlit as st
import osmnx as ox
import leafmap.foliumap as leafmap

st.set_page_config(page_title="Interactive Web Mapping", layout="wide")

st.title("Interactive Web Mapping with OSMnx")

st.markdown(
    """
### 📌 概要

このページでは、OSMnxで取得したGeoDataFrameを使い、**Leafletベースのインタラクティブ地図（folium）**上で可視化します。

---

### 🛠 使用する主なライブラリと関数の解説

- `ox.features_from_place(place, tags={"building": True})`：建物ポリゴンを取得します。
- `ox.geocode_to_gdf(place)`：地域の境界ポリゴンを取得します。
- `leafmap.Map()`：foliumをベースとしたインタラクティブマップの作成が可能なMapオブジェクトを生成します。
- `add_gdf(gdf, layer_name)`：GeoDataFrameを地図レイヤーとして追加します。

---

### ⚙️ 実行
"""
)

with st.form("webmap_form"):
    place = st.text_input(
        "都市名またはエリア（例: Shibuya, Tokyo, Japan）", value="Shibuya, Tokyo, Japan"
    )
    submitted = st.form_submit_button("地図を生成")

if submitted:
    with st.spinner("データを取得中..."):
        gdf_boundary = ox.geocode_to_gdf(place)
        gdf_buildings = ox.features_from_place(place, tags={"building": True})

        m = leafmap.Map(
            center=(
                gdf_boundary.geometry.centroid.y.values[0],
                gdf_boundary.geometry.centroid.x.values[0],
            ),
            zoom=15,
        )
        m.add_gdf(gdf_boundary, layer_name="Boundary")
        m.add_gdf(gdf_buildings, layer_name="Buildings")

        st.success("インタラクティブマップが生成されました。")
        m.to_streamlit(height=700)

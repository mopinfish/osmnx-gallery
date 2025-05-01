# osmnx_overview.py

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(layout="wide")
st.title("OSMnx Overview Demo")
st.write("都市境界の取得、保存、OSM IDによる検索などをデモします。")

# --- セクション1: 単一都市の境界を取得 ---
st.header("① 単一都市の境界取得と表示")
city_name = st.text_input("都市名", "Manhattan, New York, USA")

if st.button("都市境界を取得"):
    city = ox.geocode_to_gdf(city_name)
    city_proj = ox.projection.project_gdf(city)

    fig, ax = plt.subplots(figsize=(8, 8))
    city_proj.plot(ax=ax, fc="gray", ec="none")
    ax.set_axis_off()
    st.pyplot(fig)
    st.dataframe(city)

# --- セクション2: 複数都市の境界を取得しGeoPackage保存 ---
st.header("② 複数都市の境界取得・保存・表示")
place_input = st.text_area(
    "都市リスト（1行ずつ入力）",
    value="\n".join(
        [
            "Berkeley, California, USA",
            "Oakland, California, USA",
            "Piedmont, California, USA",
            "Emeryville, California, USA",
            "Alameda, Alameda County, CA, USA",
        ]
    ),
)
places = [line.strip() for line in place_input.strip().splitlines() if line.strip()]

if st.button("複数都市を取得して表示"):
    gdf = ox.geocode_to_gdf(list(places))
    gdf_proj = ox.projection.project_gdf(gdf)

    # 保存（GeoPackage）
    Path("data").mkdir(exist_ok=True)
    gpkg_path = Path("data/east_bay.gpkg")
    gdf.to_file(gpkg_path, driver="GPKG")

    fig, ax = plt.subplots(figsize=(8, 8))
    gdf_proj.plot(ax=ax, fc="gray", ec="none")
    ax.set_axis_off()
    st.pyplot(fig)

    st.success(f"保存完了: {gpkg_path}")
    st.dataframe(gdf)

# --- セクション3: OSM ID から地物を取得 ---
st.header("③ OSM IDから地物を取得")
osm_ids = st.text_input("OSM IDs（カンマ区切り）", "R357794, N8170768521, W427818536")

if st.button("OSM IDから取得"):
    try:
        ids = [x.strip() for x in osm_ids.split(",")]
        gdf = ox.geocode_to_gdf([{"osmid": id} for id in ids], by_osmid=True)
        st.map(gdf)
        st.dataframe(gdf)
    except Exception as e:
        st.error(f"取得に失敗しました: {e}")

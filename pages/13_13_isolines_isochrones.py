import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

st.set_page_config(page_title="Isolines and Isochrones", layout="wide")

st.title("Isolines and Isochrones")

st.markdown(
    """
### 📌 概要

このページでは、OSMnxとNetworkXを使って、**等時間線（isochrones）**を計算・表示します。
中心地点から指定の時間内で到達できる範囲をポリゴンとして可視化できます。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_point()`：緯度経度と距離をもとにネットワークを取得します。
- `ox.project_graph()`：ネットワークを投影座標系に変換（BallTree不要化）。
- `nx.single_source_dijkstra_path_length()`：重み付き最短距離（例：travel_time）を計算します。

---

### ⚙️ 実行
"""
)

with st.form("isochrone_form"):
    lat = st.number_input("中心点の緯度", value=35.7101, format="%.6f")
    lng = st.number_input("中心点の経度", value=139.8107, format="%.6f")
    dist = st.slider("探索距離（メートル）", 500, 5000, 2000, step=500)
    times = st.multiselect("等時間線の時間（分）", [5, 10, 15, 20], default=[5, 10, 15])
    submitted = st.form_submit_button("等時間線を描画")

if submitted:
    with st.spinner("ネットワークと等時間線の計算中..."):
        center = (lat, lng)
        G = ox.graph_from_point(center, dist=dist, network_type="walk")
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        G_proj = ox.project_graph(G)

        node_center = ox.distance.nearest_nodes(G_proj, lng, lat)
        travel_times = nx.single_source_dijkstra_path_length(
            G_proj, node_center, weight="travel_time"
        )

        nodes = ox.graph_to_gdfs(G_proj, edges=False)
        nodes["travel_time"] = nodes.index.map(travel_times)
        polygons = []

        for minutes in sorted(times):
            threshold = minutes * 60
            sub_nodes = nodes[nodes["travel_time"] <= threshold]
            if sub_nodes.empty:
                continue
            buffer = sub_nodes.geometry.unary_union.convex_hull.buffer(100)
            polygons.append({"geometry": buffer, "minutes": minutes})

        gdf_poly = gpd.GeoDataFrame(polygons, crs=nodes.crs)

        fig, ax = plt.subplots(figsize=(8, 8))
        gdf_poly.plot(
            ax=ax, column="minutes", cmap="plasma", edgecolor="k", legend=True
        )
        nodes.plot(ax=ax, color="black", markersize=2)
        ax.set_title("Isochrones from center")
        ax.axis("off")
        st.pyplot(fig)

import streamlit as st
import networkx as nx
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

# アプリ設定
st.set_page_config(page_title="等時圏分析ツール", layout="wide")
ox.settings.log_console = True
ox.settings.use_cache = True

# サイドバー設定
with st.sidebar:
    st.header("分析パラメータ")
    place = st.text_input("分析地域", "東京都新宿区")
    network_type = st.selectbox(
        "移動手段",
        ["walk", "bike", "drive"],
        index=0
    )
    trip_times = st.multiselect(
        "時間範囲（分）",
        [5, 10, 15, 20, 25, 30],
        default=[5, 10, 15]
    )
    travel_speed = st.slider("移動速度 (km/h)", 1.0, 10.0, 4.5)
    buffer_method = st.radio(
        "等時線生成方法",
        ["Convex Hull", "Buffer"]
    )

# メインコンテンツ
st.title("Isolines and Isochrones｜OSMnx 等時圏分析ツール")

st.markdown("""
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
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("可視化領域")
    map_placeholder = st.empty()

with col2:
    st.subheader("分析設定概要")
    st.json({
        "地域": place,
        "移動手段": network_type,
        "時間範囲": trip_times,
        "移動速度": f"{travel_speed} km/h"
    })

if st.button("等時圏生成"):
    with st.spinner("地理データ処理中..."):
        try:
            # 道路ネットワーク取得
            G = ox.graph_from_place(place, network_type=network_type)
            G_proj = ox.project_graph(G)

            # 中心点計算
            gdf_nodes = ox.convert.graph_to_gdfs(G, edges=False)
            x, y = gdf_nodes["geometry"].union_all().centroid.xy
            center_node = ox.distance.nearest_nodes(G_proj, x[0], y[0])

            # エッジの移動時間属性追加
            meters_per_minute = travel_speed * 1000 / 60
            for u, v, k, data in G_proj.edges(data=True, keys=True):
                data["time"] = data["length"] / meters_per_minute

            # 等時圏生成
            isochrone_polys = []
            for time in sorted(trip_times, reverse=True):
                subgraph = nx.ego_graph(
                    G_proj, center_node, radius=time, distance="time")

                if buffer_method == "Convex Hull":
                    poly = gpd.GeoSeries([
                        Point(data["x"], data["y"])
                        for node, data in subgraph.nodes(data=True)
                    ]).unary_union.convex_hull
                else:
                    # Bufferメソッド用の処理
                    edge_lines = []
                    for u, v in subgraph.edges():
                        edge_data = G_proj.get_edge_data(u, v)[0]
                        if "geometry" in edge_data:
                            edge_lines.append(edge_data["geometry"])

                    nodes_gdf = gpd.GeoDataFrame(
                        geometry=[Point(data["x"], data["y"])
                                  for node, data in subgraph.nodes(data=True)]
                    )
                    n = nodes_gdf.buffer(50)
                    e = gpd.GeoSeries(edge_lines).buffer(20)
                    poly = n.union(e).unary_union

                isochrone_polys.append(poly)

            # 可視化
            fig, ax = plt.subplots(figsize=(10, 10))
            ox.plot_graph(G_proj, ax=ax, node_size=0,
                          edge_color="gray", edge_linewidth=0.5)

            colors = ox.plot.get_colors(
                len(trip_times), cmap="plasma", start=0)
            for poly, color in zip(isochrone_polys, colors):
                gpd.GeoSeries([poly]).plot(
                    ax=ax, color=color, alpha=0.4, ec="none")

            map_placeholder.pyplot(fig)
            st.session_state.isochrones = gpd.GeoDataFrame(
                geometry=isochrone_polys)

        except Exception as e:
            st.error(f"エラー発生: {str(e)}")

# データエクスポート
if "isochrones" in st.session_state:
    with st.expander("生成データのエクスポート"):
        geojson = st.session_state.isochrones.to_json()
        st.download_button(
            label="GeoJSON形式でダウンロード",
            data=geojson,
            file_name="isochrones.geojson",
            mime="application/json"
        )

        st.dataframe(
            st.session_state.isochrones.assign(
                到達時間=lambda df: sorted(trip_times, reverse=True)
            ),
            column_config={
                "geometry": "地理情報",
                "到達時間": st.column_config.NumberColumn("到達時間（分）")
            }
        )

# 実行方法
with st.sidebar.expander("実行ガイド"):
    st.markdown("""
    ```
    pip install streamlit osmnx geopandas matplotlib
    streamlit run isochrone_app.py
    ```
    """)

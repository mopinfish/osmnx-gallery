import multiprocessing as mp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import osmnx as ox
import streamlit as st

st.set_page_config(page_title="OSMnxルーティング・速度・時間分析", layout="wide")
ox.settings.use_cache = True
np.random.seed(0)

# --- 解説と主要関数ソース ---
st.markdown("""
# OSMnx ルーティング・速度・時間分析

このアプリはOSMnxを用いた道路ネットワークの
- 最近傍ノード・エッジ探索
- 距離・時間最短経路探索
- 速度補完と所要時間推定
- 並列処理による大量ルート計算

をインタラクティブに体験できます。

---

## 主な関数とソースコード

### 最近傍ノード探索
```
nodes, dists = ox.distance.nearest_nodes(G, X, Y, return_dist=True)
node = ox.distance.nearest_nodes(G, x, y)
```

### 最近傍エッジ探索
```
edges, dists = ox.distance.nearest_edges(G, X, Y, return_dist=True)
edge = ox.distance.nearest_edges(G, x, y)
```

### 最短経路探索
```
route = ox.routing.shortest_path(G, orig, dest, weight="length")
```

### k本の最短経路
```
routes = ox.routing.k_shortest_paths(G, orig, dest, k=30, weight="length")
```

### 速度・所要時間補完
```
G = ox.routing.add_edge_speeds(G, hwy_speeds={"residential": 35, ...})
G = ox.routing.add_edge_travel_times(G)
```

### 並列最短経路計算
```
routes = ox.routing.shortest_path(G, origs, dests, weight="travel_time", cpus=4)
```
""")

# --- サイドバー ---
with st.sidebar:
    st.header("分析パラメータ")
    place = st.text_input("地域名", "Piedmont, California, USA")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike"], index=0)
    st.markdown("#### 速度補完 (km/h)")
    hwy_speeds = {
        "residential": st.slider("residential", 10, 60, 35),
        "secondary": st.slider("secondary", 20, 90, 50),
        "tertiary": st.slider("tertiary", 20, 100, 60)
    }

# --- データ取得 ---


@st.cache_resource
def get_graph(place, network_type):
    G = ox.graph.graph_from_place(place, network_type=network_type)
    Gp = ox.projection.project_graph(G)
    return Gp


G = get_graph(place, network_type)

# --- タブ ---
tab1, tab2, tab3, tab4 = st.tabs([
    "最近傍ノード・エッジ探索", "最短経路・k本経路", "速度・時間補完", "並列ルーティング"
])

with tab1:
    st.subheader("最近傍ノード・エッジ探索")
    n_points = st.slider("サンプル点数", 1, 200, 100)
    points = ox.utils_geo.sample_points(
        ox.convert.to_undirected(G), n=n_points)
    X = points.x.values
    Y = points.y.values
    X0 = X.mean()
    Y0 = Y.mean()
    nodes, dists = ox.distance.nearest_nodes(G, X, Y, return_dist=True)
    node = ox.distance.nearest_nodes(G, X0, Y0)
    edges, edists = ox.distance.nearest_edges(G, X, Y, return_dist=True)
    edge = ox.distance.nearest_edges(G, X0, Y0)
    st.write(f"最近傍ノードID（中心点）: {node}")
    st.write(f"最近傍エッジ（中心点）: {edge}")

with tab2:
    st.subheader("最短経路・k本経路")
    orig = st.number_input("起点ノードID", value=int(list(G.nodes)[0]))
    dest = st.number_input("終点ノードID", value=int(
        list(G.nodes)[min(120, len(G.nodes)-1)]))
    if st.button("距離最短経路を描画"):
        route = ox.routing.shortest_path(G, orig, dest, weight="length")
        fig, ax = ox.plot.plot_graph_route(
            G, route, route_color="y", route_linewidth=6, node_size=0, show=False, close=False)
        st.pyplot(fig)
    if st.button("k本の最短経路を描画"):
        routes = ox.routing.k_shortest_paths(
            G, orig, dest, k=5, weight="length")
        fig, ax = ox.plot.plot_graph_routes(G, list(
            routes), route_colors="y", route_linewidth=4, node_size=0, show=False, close=False)
        st.pyplot(fig)

with tab3:
    st.subheader("速度・所要時間補完と比較")
    G2 = ox.routing.add_edge_speeds(G, hwy_speeds=hwy_speeds)
    G2 = ox.routing.add_edge_travel_times(G2)
    edges_gdf = ox.convert.graph_to_gdfs(G2, nodes=False)
    st.write("道路種別ごとの平均速度・距離・所要時間（秒）")
    edges_gdf["highway"] = edges_gdf["highway"].astype(str)
    st.dataframe(edges_gdf.groupby("highway")[
                 ["length", "speed_kph", "travel_time"]].mean().round(1))
    orig2 = list(G2.nodes)[1]
    dest2 = list(G2.nodes)[min(120, len(G2.nodes)-1)]
    route1 = ox.routing.shortest_path(G2, orig2, dest2, weight="length")
    route2 = ox.routing.shortest_path(G2, orig2, dest2, weight="travel_time")
    fig, ax = ox.plot.plot_graph_routes(G2, [route1, route2], route_colors=[
                                        "r", "y"], route_linewidth=6, node_size=0, show=False, close=False)
    st.pyplot(fig)
    # 距離・時間比較
    r1_gdf = ox.routing.route_to_gdf(G2, route1, weight="length")
    r2_gdf = ox.routing.route_to_gdf(G2, route2, weight="travel_time")
    route1_length = int(r1_gdf["length"].sum())
    route2_length = int(r2_gdf["length"].sum())
    route1_time = int(r1_gdf["travel_time"].sum())
    route2_time = int(r2_gdf["travel_time"].sum())
    st.write(f"距離最短経路: {route1_length}m, {route1_time}s")
    st.write(f"時間最短経路: {route2_length}m, {route2_time}s")

with tab4:
    st.subheader("並列ルーティング")
    n_routes = st.number_input("経路本数", 10, 10000, 100)
    cpus = st.slider("CPUコア数", 1, mp.cpu_count(), 2)
    origs = np.random.choice(list(G.nodes), size=n_routes)
    dests = np.random.choice(list(G.nodes), size=n_routes)
    if st.button("並列経路計算（travel_time最小）"):
        with st.spinner("計算中..."):
            routes = ox.routing.shortest_path(
                G, origs, dests, weight="travel_time", cpus=cpus)
            valid_routes = [r for r in routes if r]
            st.write(
                f"計算成功率: {len(valid_routes)}/{len(routes)} ({len(valid_routes)/len(routes):.1%})")

# --- データダウンロード ---
with st.sidebar.expander("GeoJSON出力"):
    edges_gdf = ox.convert.graph_to_gdfs(G, nodes=False)
    st.download_button(
        label="ネットワーク(GeoJSON)",
        data=edges_gdf.to_json(),
        file_name="network.geojson",
        mime="application/json"
    )

# --- ソースコードダウンロード ---
with st.expander("📜 このページのソースコード"):
    with open(__file__, "r") as f:
        st.code(f.read(), language="python")

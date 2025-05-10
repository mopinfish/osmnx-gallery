import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Routing by Speed or Travel Time", layout="wide")

st.title("OSMnx Routing: Speed vs. Travel Time")

st.markdown("""
### 📌 概要

このページでは、OSMnxとNetworkXを使って経路探索を行い、距離または時間ベースでの最短経路を比較します。

---

### 🛠 使用する主な関数の解説

- `ox.add_edge_speeds(G)`：各エッジに推定速度（km/h）を追加します。
- `ox.add_edge_travel_times(G)`：速度から各エッジの移動時間（秒）を追加します。
- `nx.shortest_path(G, source, target, weight)`：指定された重み（距離 or 時間）で最短経路を探索します。
- `ox.plot_graph_route(G, route)`：指定したルートをグラフ上に描画します。

---

### ⚙️ 実行
""")

with st.form("routing_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk"], index=0)
    routing_mode = st.radio("経路タイプを選択", ["最短距離", "最短時間"])
    submitted = st.form_submit_button("ルート探索")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)

        orig, dest = list(G.nodes())[0], list(G.nodes())[-1]
        weight = "length" if routing_mode == "最短距離" else "travel_time"

        route = nx.shortest_path(G, orig, dest, weight=weight)

        st.success(f"{routing_mode}に基づいたルートを表示します")

        fig, ax = ox.plot_graph_route(G, route, node_size=0, bgcolor="w", edge_color="#cccccc",
                                      route_color="red", route_linewidth=3, show=False, close=False)
        st.pyplot(fig)

        st.markdown(f"**出発ノード:** {orig}  **到着ノード:** {dest}")
        st.markdown(f"**ルートのノード数:** {len(route)}")

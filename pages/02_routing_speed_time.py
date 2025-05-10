import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Routing by Speed or Travel Time", layout="wide")

st.title("OSMnx Routing: Speed vs. Travel Time")

st.markdown("""
このページでは、OSMnxとNetworkXを使って経路探索を行い、
**距離ベース**または**時間ベース**での最短経路を比較します。

- `graph_from_place()` で道路ネットワークを取得
- `add_edge_speeds()` や `add_edge_travel_times()` により速度・所要時間の属性を追加
- `shortest_path()` によって最短経路を算出
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

        # 出発点と到着点をランダムに設定
        orig, dest = list(G.nodes())[0], list(G.nodes())[-1]
        weight = "length" if routing_mode == "最短距離" else "travel_time"

        route = nx.shortest_path(G, orig, dest, weight=weight)

        st.success(f"{routing_mode}に基づいたルートを表示します")

        fig, ax = ox.plot_graph_route(G, route, node_size=0, bgcolor="w", edge_color="#cccccc",
                                      route_color="red", route_linewidth=3, show=False, close=False)
        st.pyplot(fig)

        st.markdown(f"**出発ノード:** {orig}  **到着ノード:** {dest}")
        st.markdown(f"**ルートのノード数:** {len(route)}")

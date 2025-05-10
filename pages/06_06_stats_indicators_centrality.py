import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Network Stats & Centrality", layout="wide")

st.title("Network Statistics and Centrality Measures")

st.markdown("""
### 📌 概要

このページでは、OSMnxで取得した道路ネットワークから統計情報や中心性指標を算出します。

---

### 🛠 使用する主な関数の解説

- `ox.basic_stats(G)`：ノード数、エッジ数、平均ストリート長などのネットワーク統計を返します。
- `nx.betweenness_centrality_subset()`：指定ノード間の媒介中心性を計算します（部分集合を使って効率化）。
- `ox.plot_graph()`：中心性の大小に応じてノードサイズを変更して可視化します。

---

### ⚙️ 実行
""")

with st.form("centrality_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0)
    k = st.slider("中心性計算のノード数上限（サンプリング）", min_value=50, max_value=300, value=150, step=10)
    submitted = st.form_submit_button("計算実行")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        stats = ox.basic_stats(G)

        st.subheader("基本統計情報")
        for k_, v_ in stats.items():
            st.write(f"**{k_}**: {v_}")

        st.subheader("Betweenness Centrality（媒介中心性）")
        with st.spinner("中心性を計算中..."):
            nodes = list(G.nodes())
            sample_nodes = nodes[:k]
            centrality = nx.betweenness_centrality_subset(G, sources=sample_nodes, targets=sample_nodes, weight="length", normalized=True)

            top_node = max(centrality, key=centrality.get)

            fig, ax = ox.plot_graph(G, node_size=[centrality.get(n, 0)*5000 for n in G.nodes()],
                                    node_color="r", edge_color="#999999", show=False, close=False)
            st.pyplot(fig)
            st.write(f"**最大中心性のノード:** {top_node}")

import streamlit as st
import osmnx as ox
import igraph as ig
import networkx as nx

st.set_page_config(page_title="OSMnx to iGraph Conversion", layout="wide")

st.title("Convert OSMnx Network to iGraph")

st.markdown(
    """
### 📌 概要

このページでは、OSMnxで取得したネットワークを `igraph` 形式に変換し、ネットワークの基本的なプロパティを表示します。

---

### 🛠 使用する主な関数・処理の解説

- `ox.graph_from_place(place)`：指定都市のネットワークを取得します。
- `nx.Graph(G)`：NetworkXグラフを無向化します。
- `igraph.Graph.TupleList()`：無向ネットワークのエッジリストからiGraphに変換します。

---

### ⚙️ 実行
"""
)

with st.form("igraph_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike"], index=0
    )
    submitted = st.form_submit_button("変換実行")

if submitted:
    with st.spinner("OSMnxネットワークを取得してiGraphに変換中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        G_undir = nx.Graph(G)  # 無向化（NetworkX）

        edges = list(G_undir.edges())
        g = ig.Graph.TupleList(edges, directed=False)

        st.success("iGraphへの変換が完了しました。")

        st.subheader("iGraph オブジェクト情報")
        st.write(f"ノード数: {g.vcount()}")
        st.write(f"エッジ数: {g.ecount()}")
        st.write(f"密度: {g.density():.4f}")
        st.write("次数分布（上位10件）:")
        degrees = g.degree()
        degree_counts = sorted(
            [(i, d) for i, d in enumerate(degrees)], key=lambda x: -x[1]
        )[:10]
        for node, deg in degree_counts:
            st.write(f"ノード {node}: 次数 {deg}")

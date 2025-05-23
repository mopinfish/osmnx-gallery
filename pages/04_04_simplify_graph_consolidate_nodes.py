import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simplify Graph & Consolidate Nodes", layout="wide")

st.title("Simplify Graph & Consolidate Nodes")

st.markdown(
    """
### 📌 概要

このページでは、OSMnxで取得した道路ネットワークを**簡素化（simplify）**したり、
交差点のノードを**統合（consolidate）**して、より抽象化されたネットワークを作成します。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_place(place, simplify=True)`：都市名からネットワークを取得し、簡素化します。
- `ox.consolidate_intersections(G, tolerance, rebuild_graph=True)`：指定距離以内の交差点ノードを1つに統合します。
- `ox.graph_to_gdfs(G)`：ネットワークをGeoDataFrame（ノード・エッジ）に変換します。

---

### ⚙️ 実行
"""
)

with st.form("simplify_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0
    )
    tolerance = st.slider("ノード統合の許容距離（メートル）", 1, 100, 15)
    submitted = st.form_submit_button("取得・簡素化・統合実行")

if submitted:
    with st.spinner("ネットワーク取得と処理中..."):
        G = ox.graph_from_place(place, network_type=network_type, simplify=True)
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

        G_proj = ox.consolidate_intersections(
            G, tolerance=tolerance, rebuild_graph=True
        )
        gdf_nodes_proj, gdf_edges_proj = ox.graph_to_gdfs(G_proj)

        st.success("ネットワークの取得と統合が完了しました。")

        st.subheader("オリジナルのノードとエッジ")
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        gdf_edges.plot(ax=ax1, linewidth=0.5, edgecolor="gray")
        gdf_nodes.plot(ax=ax1, color="red", markersize=5)
        st.pyplot(fig1)

        st.subheader("統合後のノードとエッジ")
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        gdf_edges_proj.plot(ax=ax2, linewidth=0.5, edgecolor="gray")
        gdf_nodes_proj.plot(ax=ax2, color="blue", markersize=5)
        st.pyplot(fig2)

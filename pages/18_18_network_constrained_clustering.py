import streamlit as st
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

st.set_page_config(page_title="Network-Constrained Clustering", layout="wide")

st.title("Network-Constrained Clustering")

st.markdown(
    """
### 📌 概要

このページでは、道路ネットワーク上のノード位置を使って、**ネットワーク制約付きクラスタリング**を行います。
KMeansを使い、ネットワーク上のノードを位置情報でクラスタリングし、視覚化します。

---

### 🛠 使用する主な手法の解説

- `ox.graph_from_place()`：ネットワーク取得
- `ox.graph_to_gdfs()`：ノード座標を取得
- `sklearn.cluster.KMeans()`：クラスタリング手法（ここでは幾何学座標に基づく）

---

### ⚙️ 実行
"""
)

with st.form("clustering_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["walk", "drive", "bike"], index=0
    )
    n_clusters = st.slider("クラスタ数", min_value=2, max_value=10, value=4)
    submitted = st.form_submit_button("クラスタリング実行")

if submitted:
    with st.spinner("ネットワーク取得とクラスタリング中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

        coords = np.array([(point.y, point.x) for point in gdf_nodes.geometry])
        model = KMeans(n_clusters=n_clusters, random_state=42).fit(coords)
        gdf_nodes["cluster"] = model.labels_

        st.success("クラスタリングが完了しました。")

        fig, ax = plt.subplots(figsize=(8, 8))
        gdf_edges.plot(ax=ax, linewidth=0.5, edgecolor="gray", zorder=1)
        gdf_nodes.plot(ax=ax, column="cluster", cmap="tab10", markersize=8, zorder=2)
        ax.set_title(f"Network-Constrained Clustering (k={n_clusters})")
        ax.axis("off")
        st.pyplot(fig)

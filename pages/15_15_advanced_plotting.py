import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, colors

st.set_page_config(page_title="Advanced Plotting", layout="wide")

st.title("Advanced Plotting with OSMnx")

st.markdown("""
### 📌 概要

このページでは、OSMnxによるネットワーク可視化の高度なカスタマイズ方法を紹介します。ノードサイズや色、エッジ長に応じた色付けなど、視覚的に意味のある表現を行います。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_place()`：ネットワークの取得
- `ox.plot_graph()`：OSMnx v2では数値ではなくカラーコードを `edge_color` に渡す必要があります。
- `matplotlib.cm` を用いて値をカラーコードに変換し、凡例を表示します。

---

### ⚙️ 実行
""")

with st.form("plot_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0)
    submitted = st.form_submit_button("グラフ描画")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        edge_lengths = [data.get("length", 0)
                        for _, _, data in G.edges(data=True)]

        # 長さをカラーマップに変換（hex）
        norm = colors.Normalize(vmin=min(edge_lengths), vmax=max(edge_lengths))
        cmap = cm.get_cmap("plasma")
        edge_rgba = [colors.to_hex(cmap(norm(val))) for val in edge_lengths]

        fig, ax = plt.subplots(figsize=(8, 8))
        ox.plot_graph(
            G,
            ax=ax,
            edge_color=edge_rgba,
            edge_linewidth=1,
            node_size=5,
            node_color="black",
            bgcolor="white",
            show=False,
            close=False
        )

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm._A = []
        plt.colorbar(sm, ax=ax, shrink=0.5, label="Edge Length (m)")
        st.pyplot(fig)

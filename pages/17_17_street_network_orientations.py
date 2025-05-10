import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Street Network Orientations", layout="wide")

st.title("Street Network Orientations")

st.markdown("""
### 📌 概要

このページでは、道路ネットワークの**方位角分布（方向性）**を分析・可視化します。  
都市の街路パターンがどの方向に整列しているかを理解するのに有効です。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_place()`：道路ネットワークの取得
- `ox.bearing.add_edge_bearings()`：各エッジに「bearing（方位角）」属性を追加
- `matplotlib.pyplot` を使って極座標ヒストグラムを描画

---

### ⚙️ 実行
""")

with st.form("bearing_form"):
    place = st.text_input("都市名（例: Manhattan, New York, USA）",
                          value="Manhattan, New York, USA")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike"], index=0)
    submitted = st.form_submit_button("描画実行")

if submitted:
    with st.spinner("ネットワークと方位データを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        G = ox.bearing.add_edge_bearings(G)
        bearings = [data["bearing"]
                    for _, _, data in G.edges(data=True) if "bearing" in data]

        fig, ax = plt.subplots(
            subplot_kw={'projection': 'polar'}, figsize=(6, 6))
        ax.hist(
            np.deg2rad(bearings),
            bins=36,
            density=True,
            color="dodgerblue",
            edgecolor="k",
            alpha=0.7
        )
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Street Orientation Histogram", y=1.05)

        st.pyplot(fig)

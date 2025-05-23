import streamlit as st
import osmnx as ox

st.set_page_config(page_title="Graph Place Queries", layout="wide")

st.title("Graph Place Queries with OSMnx")

st.markdown(
    """
### 📌 概要

このページでは、OSMnxの `graph_from_place` や `graph_from_address` などの関数を使って、
地名・住所・緯度経度から道路ネットワークを取得する方法を解説・体験できます。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_place(place)`：都市名を指定して道路ネットワークを取得
- `ox.graph_from_address(address, dist)`：住所と距離を指定して周辺の道路ネットワークを取得
- `ox.graph_from_point((lat, lng), dist)`：緯度経度からバッファ距離でネットワークを取得

---

### ⚙️ 実行
"""
)

mode = st.radio("入力モードの選択", ["都市名", "住所", "緯度経度"])
network_type = st.selectbox(
    "ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0
)

if mode == "都市名":
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    trigger = st.button("ネットワーク取得（都市名）")
    if trigger:
        with st.spinner("ネットワークを取得中..."):
            G = ox.graph_from_place(place, network_type=network_type)
            fig, ax = ox.plot_graph(
                G,
                bgcolor="w",
                node_size=5,
                edge_color="#999999",
                show=False,
                close=False,
            )
            st.pyplot(fig)

elif mode == "住所":
    address = st.text_input(
        "住所（例: 1 Chome-1-2 Oshiage, Sumida, Tokyo）",
        value="1 Chome-1-2 Oshiage, Sumida, Tokyo",
    )
    dist = st.slider("取得半径（メートル）", 100, 3000, 800, 100)
    trigger = st.button("ネットワーク取得（住所）")
    if trigger:
        with st.spinner("ネットワークを取得中..."):
            G = ox.graph_from_address(address, dist=dist, network_type=network_type)
            fig, ax = ox.plot_graph(
                G,
                bgcolor="w",
                node_size=5,
                edge_color="#999999",
                show=False,
                close=False,
            )
            st.pyplot(fig)

elif mode == "緯度経度":
    lat = st.number_input("緯度", value=35.7101, format="%.6f")
    lng = st.number_input("経度", value=139.8107, format="%.6f")
    dist = st.slider("取得半径（メートル）", 100, 3000, 800, 100)
    trigger = st.button("ネットワーク取得（緯度経度）")
    if trigger:
        with st.spinner("ネットワークを取得中..."):
            G = ox.graph_from_point((lat, lng), dist=dist, network_type=network_type)
            fig, ax = ox.plot_graph(
                G,
                bgcolor="w",
                node_size=5,
                edge_color="#999999",
                show=False,
                close=False,
            )
            st.pyplot(fig)

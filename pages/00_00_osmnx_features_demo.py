import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="OSMnx Features Demo", layout="wide")

st.title("OSMnx Features Demo")

st.markdown("""
### 📌 概要

このデモでは、OSMnxを使って指定した都市の道路ネットワークを取得し、可視化します。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_place(place, network_type)`:
    指定された都市の道路ネットワークを取得します。
- `ox.plot_graph(G)`:
    ネットワークを可視化する関数で、Matplotlibの描画機能を内部で使っています。
- `ox.basic_stats(G)`:
    ネットワークの基本統計指標（ノード数、平均ノード間距離など）を取得します。

---

### ⚙️ 実行
""")

with st.form("osmnx_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", options=["drive", "walk", "bike", "all"], index=0)
    submitted = st.form_submit_button("ネットワークを取得して描画")

if submitted:
    with st.spinner("ネットワークデータを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)

        st.success("ネットワークの取得が完了しました。")

        st.subheader("ネットワークの可視化")
        fig, ax = ox.plot_graph(
            G, bgcolor="w", node_size=5, edge_color="#999999", show=False, close=False)
        st.pyplot(fig)

        st.subheader("基本統計情報")
        stats = ox.basic_stats(G)
        for key, value in stats.items():
            st.write(f"**{key}**: {value}")

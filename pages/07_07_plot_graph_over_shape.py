import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plot Graph Over Shape", layout="wide")

st.title("Plot Graph Over Shapefile")

st.markdown("""
### 📌 概要

このページでは、取得した道路ネットワークを都市境界（行政区域）と重ねて描画します。
ネットワークデータとポリゴンデータを同時に取得・表示することで、都市構造の可視化が可能になります。

---

### 🛠 使用する主な関数の解説

- `ox.graph_from_place(place, network_type)`:  
  指定した地名（place）から、OpenStreetMapに基づいて道路ネットワークを取得します。`network_type`で「車道」「歩道」などの種類を選べます。

- `ox.geocode_to_gdf(place)`:  
  地名からジオメトリ情報（ポリゴン）を取得し、GeoDataFrameとして返します。

- `ox.plot_graph(G, ax=..., ...)`:  
  ネットワークグラフを既存のMatplotlibの軸上に描画します。都市の輪郭と重ねて表示するために使用します。

---

### ⚙️ 実行
""")

with st.form("plot_shape_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0)
    submitted = st.form_submit_button("取得して重ねて描画")

if submitted:
    with st.spinner("ネットワークとポリゴンを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)
        gdf = ox.geocode_to_gdf(place)

        st.success("データの取得が完了しました。")

        fig, ax = plt.subplots(figsize=(8, 8))
        gdf.plot(ax=ax, facecolor="white",
                 edgecolor="black", linewidth=2, zorder=1)
        ox.plot_graph(G, ax=ax, node_size=5, edge_color="gray",
                      show=False, close=False, bgcolor="white")
        st.pyplot(fig)

# streamlit_app.py

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import contextily as ctx  # type: ignore

st.set_page_config(layout="wide")
st.title("OSMnx × Contextily デモアプリ")
st.write("都市の道路ネットワークを取得し、OpenStreetMapの背景地図付きで可視化します。")

# ユーザー入力
place_name = st.text_input(
    "都市名を入力してください（例: Piedmont, California, USA）",
    "Piedmont, California, USA",
)
network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])

if st.button("ネットワークを取得して表示"):
    with st.spinner("ネットワークを取得中..."):
        # ネットワークを取得
        G = ox.graph_from_place(place_name, network_type=network_type)
        nodes, edges = ox.graph_to_gdfs(G)

        # 背景地図用にWeb Mercatorに変換（EPSG:3857）
        edges_web = edges.to_crs(epsg=3857)

        # プロット
        fig, ax = plt.subplots(figsize=(10, 10))
        edges_web.plot(ax=ax, linewidth=1, edgecolor="blue")
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_axis_off()
        st.pyplot(fig)

        # 表示
        st.subheader("ノードGeoDataFrame（上位5件）")
        st.dataframe(nodes.head())

        st.subheader("エッジGeoDataFrame（上位5件）")
        st.dataframe(edges.head())

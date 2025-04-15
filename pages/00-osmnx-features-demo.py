# streamlit_app.py

import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

st.title("OSMnx デモアプリ")
st.write("都市の道路ネットワークを取得・可視化し、GeoDataFrameとしても出力します。")

# 入力フィールド
place_name = st.text_input(
    "都市名を入力してください（例: Piedmont, California, USA）", "Piedmont, California, USA")
network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])

if st.button("ネットワークを取得して表示"):
    with st.spinner("ネットワークを取得中..."):
        # ネットワーク取得
        G = ox.graph_from_place(place_name, network_type=network_type)
        fig, ax = ox.plot_graph(G, show=False, close=False)
        st.pyplot(fig)

        # GeoDataFrameに変換
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

        # 表示
        st.subheader("ノードGeoDataFrame（上位5件）")
        st.dataframe(gdf_nodes.head())

        st.subheader("エッジGeoDataFrame（上位5件）")
        st.dataframe(gdf_edges.head())

        # オプション: shapefileとしてダウンロード
        st.download_button(
            label="ノードをGeoJSONでダウンロード",
            data=gdf_nodes.to_json(),
            file_name="nodes.geojson",
            mime="application/geo+json"
        )

        st.download_button(
            label="エッジをGeoJSONでダウンロード",
            data=gdf_edges.to_json(),
            file_name="edges.geojson",
            mime="application/geo+json"
        )

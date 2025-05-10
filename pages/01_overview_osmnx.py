import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="OSMnx Overview", layout="wide")

st.title("OSMnx Overview")

st.markdown("""
このページでは、OSMnxを用いた地理データの取得と描画の基本的な流れを解説します。
対象とする地名に応じて、OSM（OpenStreetMap）から建物・道路・施設などの情報を取得し、可視化することができます。

- `geocode_to_gdf` を使って地名をGeoDataFrameに変換
- `graph_from_place` で道路ネットワークを取得
- `plot_graph` でネットワークを描画
""")

with st.form("overview_form"):
    place = st.text_input(
        "都市名を入力（例: Shibuya, Tokyo, Japan）", value="Shibuya, Tokyo, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0)
    submitted = st.form_submit_button("ネットワーク取得")

if submitted:
    with st.spinner("都市のGeoDataFrameとネットワークを取得中..."):
        # PlaceをGeoDataFrameとして取得
        gdf = ox.geocode_to_gdf(place)
        G = ox.graph_from_place(place, network_type=network_type)

        st.success("データの取得が完了しました。")

        st.subheader("エリアの形状（境界）")
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        gdf.plot(ax=ax1, facecolor="lightgray", edgecolor="black")
        st.pyplot(fig1)

        st.subheader("道路ネットワーク")
        fig2, ax2 = ox.plot_graph(
            G, bgcolor="w", node_size=5, edge_color="#444444", show=False, close=False)
        st.pyplot(fig2)

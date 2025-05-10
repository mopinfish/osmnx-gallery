import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="OSMnx Features Demo", layout="wide")

st.title("OSMnx Features Demo")

st.markdown("""
このデモでは、OSMnxを使って指定した都市の道路ネットワークを取得し、可視化します。
以下のステップで進行します：

1. 入力された都市名に基づき、道路ネットワークを取得
2. ネットワークのノードおよびエッジを描画
3. 基本的な統計情報を表示
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

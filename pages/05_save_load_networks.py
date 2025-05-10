import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import tempfile
import os

st.set_page_config(page_title="Save and Load Networks", layout="wide")

st.title("Save and Load Networks")

st.markdown("""
このページでは、OSMnxを使って取得した道路ネットワークをローカルに保存・再読込する方法を紹介します。

- `graph_from_place()` でネットワークを取得
- `.graphml` ファイルとして保存 (`save_graphml`)
- 再度 `.graphml` ファイルから読み込み (`load_graphml`)
""")

with st.form("save_load_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox(
        "ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0)
    submitted = st.form_submit_button("取得・保存・再読込")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)

        # 一時ファイルに保存
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "network.graphml")
            ox.save_graphml(G, filepath)

            # 再読込
            G_loaded = ox.load_graphml(filepath)

            st.success("ネットワークを保存して再読込しました。")

            st.subheader("読み込んだネットワークの可視化")
            fig, ax = ox.plot_graph(
                G_loaded, bgcolor="w", node_size=5, edge_color="#444444", show=False, close=False)
            st.pyplot(fig)

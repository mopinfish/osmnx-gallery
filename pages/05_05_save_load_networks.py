import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import tempfile
import os

st.set_page_config(page_title="Save and Load Networks", layout="wide")

st.title("Save and Load Networks")

st.markdown("""
### 📌 概要

このページでは、OSMnxで取得したネットワークを `.graphml` ファイルとして保存し、再読込する方法を体験できます。

---

### 🛠 使用する主な関数の解説

- `ox.save_graphml(G, filepath)`：OSMnxのネットワークデータをGraphML形式で保存します。
- `ox.load_graphml(filepath)`：GraphMLファイルからネットワークを再構築します。
- `ox.graph_from_place()`：対象都市から道路ネットワークを取得します。

---

### ⚙️ 実行
""")

with st.form("save_load_form"):
    place = st.text_input("都市名（例: Kamakura, Japan）", value="Kamakura, Japan")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"], index=0)
    submitted = st.form_submit_button("取得・保存・再読込")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        G = ox.graph_from_place(place, network_type=network_type)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "network.graphml")
            ox.save_graphml(G, filepath)

            G_loaded = ox.load_graphml(filepath)

            st.success("ネットワークを保存して再読込しました。")

            st.subheader("読み込んだネットワークの可視化")
            fig, ax = ox.plot_graph(G_loaded, bgcolor="w", node_size=5, edge_color="#444444", show=False, close=False)
            st.pyplot(fig)

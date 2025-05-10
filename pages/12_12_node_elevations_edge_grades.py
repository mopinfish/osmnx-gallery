import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Node Elevations & Edge Grades", layout="wide")

st.title("Node Elevations and Edge Grades")

st.markdown("""
### 📌 概要

このページでは、OSMnxを使って取得したネットワークに対し、ノードの標高（elevation）とエッジの勾配（grade）を付加し、
それらを視覚的に確認します。

---

### 🛠 使用する主な関数の解説

- `ox.add_node_elevations_raster(G, filepath)`：ラスターデータをもとにノード標高を付加します。
- `ox.add_edge_grades(G)`：ノード間の標高差からエッジの勾配（％）を算出します。
- `ox.plot_graph()`：エッジの勾配に応じた色でネットワークを可視化します。

> ⚠️ 本デモはSRTMなどの標高ラスターデータ（GeoTIFF）をローカルに配置しておく必要があります。

---

### ⚙️ 実行
""")

with st.form("elevation_form"):
    place = st.text_input("都市名（例: 600 Montgomery St, San Francisco, California, USA）",
                          value="600 Montgomery St, San Francisco, California, USA")
    network_type = st.selectbox(
        "ネットワークタイプ", ["walk", "drive", "bike"], index=2)
    tiff_path = st.text_input(
        "標高GeoTIFFのファイルパス（例: data/srtm.tif）", value="input_data/elevation1.tif")
    submitted = st.form_submit_button("標高と勾配を計算")

if submitted:
    if not tiff_path:
        st.error("標高データのGeoTIFFファイルパスを指定してください。")
    else:
        with st.spinner("ネットワークと標高データ処理中..."):
            G = ox.graph.graph_from_address(
                place, dist=500, dist_type="bbox", network_type=network_type)
            G = ox.elevation.add_node_elevations_raster(G, tiff_path)
            G = ox.add_edge_grades(G)

            st.success("標高と勾配の付加が完了しました。")

            edge_colors = [
                data["grade"] if ("grade" in data and data["grade"]
                                  is not None and not np.isnan(data["grade"])) else 0.0
                for _, _, data in G.edges(data=True)
            ]

            fig, ax = plt.subplots(figsize=(8, 8))
            nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
            ox.plot.plot_graph(
                G, ax=ax, node_color=nc, node_size=5, edge_color="#333333", bgcolor="k")

            sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(
                vmin=min(edge_colors), vmax=max(edge_colors)))
            sm._A = []
            plt.colorbar(sm, ax=ax, shrink=0.5, label="Edge Grade")

            st.pyplot(fig)

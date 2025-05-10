import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🏙️ OSMnx Figure-Ground Diagram Demo")

st.markdown("""
このページでは、OSMnx を使って都市の建物と道路ネットワークの図（figure-ground diagram）を描画します。
建物（figure）と道路（ground）を重ねて表示することで、都市の密度・構造・空間的バランスを視覚的に確認できます。
""")

st.markdown("""
---
## 📘 実行している処理の解説

### 建物ポリゴンと道路ネットワークの取得
```python
buildings = ox.geometries_from_place(place, tags={"building": True})
G = ox.graph.graph_from_place(place, network_type="drive")
```

### 重ね合わせて描画
```python
buildings.plot(...); ox.plot.plot_graph(..., ax=ax)
```
建物は黒、道路は白としてコントラストを強調し、都市構造をわかりやすく表現しています。
---
""")

with st.form("figure_ground_form"):
    place = st.text_input("都市名または地名", "Manhattan, New York, USA")
    submitted = st.form_submit_button("建物と道路を描画")

if submitted:
    try:
        st.info(f"{place} の建物ポリゴンと道路ネットワークを取得しています...")

        tags = {"building": True}
        buildings = ox.features_from_place(place, tags=tags)
        G = ox.graph.graph_from_place(place, network_type="drive")
        G_proj = ox.projection.project_graph(G)
        buildings_proj = buildings.to_crs(G_proj.graph["crs"])

        # 描画
        fig, ax = plt.subplots(figsize=(10, 10))
        buildings_proj.plot(ax=ax, facecolor="black", edgecolor="none")
        ox.plot.plot_graph(G_proj, ax=ax, show=False, close=False,
                           edge_color="white", edge_linewidth=0.3, node_size=0)
        ax.set_title(f"{place} - Figure-Ground Diagram", fontsize=14)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

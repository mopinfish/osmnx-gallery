import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import japanize_matplotlib  # type: ignore

print(japanize_matplotlib.__name__)

st.set_page_config(layout="wide")
st.title("🗺️ OSMnx Plot Graph Over Shape Demo")

st.markdown("""
このページでは、都市や地名のポリゴン（行政境界など）の上に、OSM道路ネットワークを重ねて描画する方法を紹介します。
背景には都市の輪郭（Polygon）を表示し、上に道路ネットワークを重ねることで、都市構造の理解に役立ちます。
""")

st.markdown("""
---
## 📘 実行している処理の解説

### 境界ポリゴンの取得
```python
gdf = ox.geocoder.geocode_to_gdf(place)
```

### ネットワークの取得と描画
```python
G = ox.graph.graph_from_place(place, network_type="drive")
ox.plot.plot_graph(G, ...)
```

### 背景としてGeoDataFrameを描画
```python
gdf.plot(ax=ax, facecolor="white", edgecolor="black")
```
---
""")

with st.form("shape_form"):
    place = st.text_input("都市名または地名", "Berkeley, California, USA")
    submitted = st.form_submit_button("ネットワークとポリゴンを重ねて表示")

if submitted:
    try:
        # 境界取得とネットワーク取得
        gdf = ox.geocoder.geocode_to_gdf(place)
        G = ox.graph.graph_from_place(place, network_type="drive")
        G_proj = ox.projection.project_graph(G)
        gdf_proj = gdf.to_crs(G_proj.graph["crs"])

        # 描画
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf_proj.plot(ax=ax, facecolor="white", edgecolor="black", linewidth=1)
        ox.plot.plot_graph(G_proj, ax=ax, show=False,
                           close=False, edge_color="#333333", node_size=0)
        ax.set_title(f"{place} の道路ネットワークと行政ポリゴン", fontsize=14)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

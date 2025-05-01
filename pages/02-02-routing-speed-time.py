import streamlit as st
import osmnx as ox

st.set_page_config(layout="wide")
st.title("📍 OSMnx Routing & Nearest Node Demo (v2.0対応)")

st.markdown(
    """
このページでは、指定した都市の道路ネットワークを取得し、
そのネットワーク上にランダムな点を生成し、各点に最も近いノード・エッジを検索する処理を行います。
OSMnxの `nearest_nodes` や `nearest_edges` 関数の利用例を体験できます。
"""
)

st.markdown(
    """
---
## 📘 実行している処理の解説

1. 指定した地名に基づいて道路ネットワークを取得します：
```python
G = ox.graph.graph_from_place(place, network_type="drive")
```

2. 投影変換を行って、距離計算が可能な平面直交座標系に変換します：
```python
Gp = ox.projection.project_graph(G)
```

3. ネットワークを無向グラフに変換し、ランダムな点を生成します：
```python
G_un = Gp.to_undirected()
points = ox.utils_geo.sample_points(G_un, n=n)
```

4. 各点から最近傍ノード・エッジを検索します：
```python
ox.distance.nearest_nodes(Gp, X, Y, return_dist=True)
ox.distance.nearest_edges(Gp, X, Y, return_dist=True)
```
---
"""
)

# --- フォームで入力を受け取る ---
with st.form("routing_form"):
    place = st.text_input(
        "対象都市名（例: Piedmont, California, USA）", "Piedmont, California, USA"
    )
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    n = st.slider("ランダム点の数", 10, 300, 100)
    submitted = st.form_submit_button("ネットワーク取得と検索実行")

if submitted:
    try:
        st.info(
            f"{place} の道路ネットワークを取得しています...（タイプ: {network_type}）"
        )
        G = ox.graph.graph_from_place(place, network_type=network_type)
        Gp = ox.projection.project_graph(G)
        G_un = Gp.to_undirected()

        points = ox.utils_geo.sample_points(G_un, n=n)
        X, Y = points.x.values, points.y.values
        X0, Y0 = X.mean(), Y.mean()

        nodes, node_dists = ox.distance.nearest_nodes(Gp, X, Y, return_dist=True)
        edges, edge_dists = ox.distance.nearest_edges(Gp, X, Y, return_dist=True)

        fig, ax = ox.plot.plot_graph(Gp, show=False, close=False)
        ax.scatter(X, Y, c="red", s=10, label="Sample Points")
        ax.scatter(X0, Y0, c="blue", s=30, label="Centroid")
        ax.legend()
        st.pyplot(fig)

        st.success("検索完了 ✅")
        st.write("最近傍ノード（先頭5件）:", nodes[:5])
        st.write("最近傍エッジ（先頭5件）:", edges[:5])

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

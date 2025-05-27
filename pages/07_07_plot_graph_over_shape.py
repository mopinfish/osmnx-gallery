# 📄 ファイル名: pages/07-plot-graph-over-shape.py

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="07 - Plot Graph Over Shape", layout="wide")
st.title("🗺️ Plot Street Network Over a Shape")

st.markdown("### 📍 地名を指定して、ポリゴンとネットワークを重ねて描画")

with st.form("graph_over_shape_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    use_projection = st.checkbox("投影（地図座標系）を統一する", value=True)
    submitted = st.form_submit_button("描画実行")

if submitted:
    with st.spinner("ネットワークとポリゴンを取得中..."):
        try:
            # ポリゴン取得
            gdf = ox.geocode_to_gdf(place)
            polygon = gdf.loc[0, "geometry"]

            # ネットワーク取得
            G = ox.graph_from_polygon(polygon, network_type=network_type)

            # 投影（必要に応じて）
            if use_projection:
                G = ox.project_graph(G)
                gdf = gdf.to_crs(G.graph["crs"])  # ✅ project_gdfの代替

            # 描画
            fig, ax = plt.subplots(figsize=(8, 8))
            ox.plot_graph(
                G,
                ax=ax,
                bgcolor="white",
                show=False,
                close=False,
                edge_color="black",
                node_size=0,
                edge_linewidth=0.8,
            )
            gdf.plot(ax=ax, facecolor="none", edgecolor="red", linewidth=2)
            ax.set_title(f"{place} - {network_type} network with boundary", fontsize=12)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🗺️ Plot Street Network Over a Shape の解説

このノートブックでは、OSMnx を使って取得した道路ネットワークを、地理的なポリゴン（たとえば市区町村の境界）と重ね合わせて描画する方法を紹介します。背景に地形や都市境界を表示することで、ネットワークの空間的な広がりや分布を視覚的に理解しやすくなります。

---

## 🏙️ 1. 都市のポリゴン形状を取得

```python
import osmnx as ox

gdf = ox.geocode_to_gdf("Piedmont, California, USA")
polygon = gdf.loc[0, "geometry"]
```

- `geocode_to_gdf` を使うと、都市名からポリゴン（行政境界）を取得できる
- `polygon` は Shapely の `Polygon` もしくは `MultiPolygon` 形式

---

## 🌐 2. ポリゴンに基づいてネットワークを取得

```python
G = ox.graph_from_polygon(polygon, network_type="drive")
```

- ポリゴンの範囲内でOSMから道路ネットワークを抽出

---

## 🖼️ 3. ポリゴンとネットワークを重ねて描画

```python
fig, ax = ox.plot_graph(G, show=False, close=False)
gdf.plot(ax=ax, facecolor="none", edgecolor="k", linewidth=3)
```

- `ox.plot_graph()` の返す `ax` に対して、`GeoDataFrame.plot()` を重ねるだけで背景表示が可能
- `facecolor="none"` にすることでポリゴンは透明、`edgecolor` によって境界が強調される

---

## 🧭 4. プロジェクションの整合

```python
gdf_proj = ox.project_gdf(gdf)
G_proj = ox.project_graph(G)
```

- `GeoDataFrame`（ポリゴン）と `Graph` を同一の投影座標系に合わせる必要がある
- 投影後のオブジェクトに対して同様に `plot()` を適用可能

---

## ✅ まとめ

| 処理 | 使用関数 | 説明 |
|------|-----------|------|
| ポリゴン取得 | `geocode_to_gdf` | 都市名から行政境界を取得 |
| ネットワーク取得 | `graph_from_polygon` | ポリゴン内のOSMネットワークを取得 |
| 投影整合 | `project_gdf`, `project_graph` | 地図投影の統一 |
| 可視化 | `plot_graph` + `gdf.plot(ax=...)` | ポリゴンとグラフを重ねて描画 |

---

この手法は、都市構造の可視化、計画範囲の明示、地図ベースのプレゼン資料作成などに活用できます。行政境界と道路網を直感的に比較することで、空間的な把握がより深まります。
"""
)

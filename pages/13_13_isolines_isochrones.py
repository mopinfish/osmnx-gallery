# 📄 ファイル名: pages/13-isolines-isochrones.py

import streamlit as st
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

st.set_page_config(page_title="13 - Isochrones", layout="wide")
st.title("🕒 Isochrones by Travel Time")

st.markdown(
    "指定地点から、歩行ネットワークに基づくアイソクロン（等時間圏）を描画します。"
)

with st.form("isochrone_form"):
    lat = st.number_input("緯度 (Y)", value=35.6895)
    lon = st.number_input("経度 (X)", value=139.6917)
    distance = st.slider("ネットワーク取得範囲（メートル）", 500, 5000, 2000, step=500)
    travel_speed = st.slider("歩行速度（km/h）", 1.0, 10.0, 4.5, step=0.5)
    trip_times = st.multiselect(
        "到達時間（分）", [5, 10, 15, 20, 25], default=[5, 10, 15]
    )
    submitted = st.form_submit_button("実行")

if submitted:
    with st.spinner("ネットワークとアイソクロンを計算中..."):
        try:
            # ネットワーク取得
            G = ox.graph_from_point((lat, lon), dist=distance, network_type="walk")
            gdf_nodes = ox.convert.graph_to_gdfs(G, edges=False)
            x, y = gdf_nodes["geometry"].union_all().centroid.xy
            # 中心ノード
            center_node = ox.distance.nearest_nodes(G, x[0], y[0])
            G = ox.project_graph(G)

            # 時間属性を追加（分単位）
            meters_per_minute = travel_speed * 1000 / 60
            for _, _, _, data in G.edges(keys=True, data=True):
                data["time"] = data["length"] / meters_per_minute

            # カラー設定
            trip_times_sorted = sorted(trip_times, reverse=True)
            iso_colors = ox.plot.get_colors(
                n=len(trip_times_sorted), cmap="plasma", start=0.3
            )

            # ポリゴン生成
            isochrone_polys = []
            for trip_time in trip_times_sorted:
                subgraph = nx.ego_graph(
                    G, center_node, radius=trip_time, distance="time"
                )
                node_points = [
                    Point((data["x"], data["y"]))
                    for node, data in subgraph.nodes(data=True)
                ]
                if node_points:
                    poly = gpd.GeoSeries(node_points).unary_union.convex_hull
                    isochrone_polys.append(poly)

            # 可視化
            fig, ax = plt.subplots(figsize=(8, 8))

            for i, poly in enumerate(isochrone_polys):
                gpd.GeoSeries(poly).plot(
                    ax=ax,
                    color=iso_colors[i],
                    alpha=0.6,
                    edgecolor="none",
                    label=f"{trip_times_sorted[i]}分",
                )
            ox.plot_graph(
                G, ax=ax, node_size=0, edge_color="gray", show=False, close=False
            )
            ax.set_title("Isochrones from center")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🕒 Isochrones from a Center Point の解説

このアプリは、指定した地点から歩行可能な範囲を時間に応じて可視化する「アイソクロンマップ（等時間圏）」を生成する Streamlit アプリです。  
地図上で、徒歩で何分圏内に到達可能かを色分けポリゴンとして表示し、出発地点も赤い点で強調されます。

---

## 🔹 ユーザー入力

- **緯度 / 経度**：中心となる出発地点を指定
- **取得範囲（メートル）**：ネットワーク取得範囲（例：2000m 半径）
- **歩行速度（km/h）**：徒歩移動速度を指定（デフォルト 4.5km/h）
- **到達時間（分）**：複数の時間圏（5分、10分など）を選択可能

---

## 🔹 処理の流れ

### 1. ネットワークの取得

```python
G = ox.graph_from_point((lat, lon), dist=distance, network_type="walk")
G = ox.project_graph(G)
```

- 指定した地点から一定距離の歩行ネットワークをOSMから取得
- 投影を行い、面積や距離計算に対応

---

### 2. 中心ノードの特定

```python
center_node = ox.distance.nearest_nodes(G, lon, lat)
```

- 出発点（緯度経度）から最寄りのグラフノードを特定

---

### 3. エッジに移動時間属性を追加

```python
for _, _, _, data in G.edges(keys=True, data=True):
    data["time"] = data["length"] / meters_per_minute
```

- 指定速度（km/h）をもとに各道路の通過時間（分）を計算し、`"time"` 属性として追加

---

### 4. アイソクロンポリゴンを作成

```python
nx.ego_graph(G, center_node, radius=trip_time, distance="time")
```

- `ego_graph()` を使い、指定時間内に到達可能なノードを抽出
- 各ノードを囲む凸包（Convex Hull）でポリゴンを作成

---

## 🔹 可視化

### 5. ポリゴンと道路の描画

```python
gpd.GeoSeries(poly).plot(...)
ox.plot_graph(G, ...)
```

- 到達時間ごとに異なる色でポリゴンを塗り分け
- 背景に道路ネットワーク（グレー）を描画
- 時間の短い順に表示し、ポリゴンが重ならないように工夫

---

### 6. 中心ノードの赤点表示

```python
ax.scatter(center_x, center_y, c="red", s=50, label="中心地点", zorder=5)
```

- 出発地点を明示的に赤い点でプロット（凡例にも表示）

---

### 7. 地図の表示範囲調整

```python
ax.set_xlim(center_x - 1000, center_x + 1000)
ax.set_ylim(center_y - 1000, center_y + 1000)
```

- 地図の表示範囲を中心点を基準に適度にズームイン

---

## ✅ 出力結果

- 色分けされた複数のアイソクロン（時間圏）
- 背景に道路ネットワーク
- 出発点を赤い点で明示
- 凡例付きのシンプルでわかりやすいアクセス圏マップ

---

## 📌 応用アイデア

- 通勤圏や商圏の視覚化
- 医療・教育施設のアクセス性評価
- アイソライン（等距離圏）への応用
- folium を使ったWeb地図形式への拡張

---
"""
)

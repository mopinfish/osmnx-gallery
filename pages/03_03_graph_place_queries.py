# 📄 ファイル名の例: pages/03-graph-place-queries.py

import streamlit as st
import osmnx as ox

st.set_page_config(page_title="03 - Graph Place Queries", layout="wide")
st.title("🧭 Graph from Place Queries")

st.markdown("### 📍 道路ネットワークの取得方法を選択してください")

query_method = st.selectbox(
    "取得方法",
    [
        "地名から取得",
        "複数の地名",
        "緯度経度 + 距離",
        "バウンディングボックス",
        "ポリゴン",
    ],
)

G = None

with st.form("graph_form"):
    if query_method == "地名から取得":
        place = st.text_input("地名（例: 東京都千代田区）", "東京都千代田区")
        network_type = st.selectbox(
            "ネットワークタイプ", ["drive", "walk", "bike", "all"]
        )
    elif query_method == "複数の地名":
        places = st.text_area("複数の地名（改行区切り）", "東京都千代田区\n東京都港区")
        network_type = st.selectbox(
            "ネットワークタイプ", ["drive", "walk", "bike", "all"]
        )
    elif query_method == "緯度経度 + 距離":
        lat = st.number_input("緯度", value=35.681236)
        lon = st.number_input("経度", value=139.767125)
        dist = st.number_input("距離（メートル）", value=1000)
        network_type = st.selectbox(
            "ネットワークタイプ", ["drive", "walk", "bike", "all"]
        )
    elif query_method == "バウンディングボックス":
        north = st.number_input("北緯", value=35.69)
        south = st.number_input("南緯", value=35.67)
        east = st.number_input("東経", value=139.77)
        west = st.number_input("西経", value=139.75)
        network_type = st.selectbox(
            "ネットワークタイプ", ["drive", "walk", "bike", "all"]
        )
    elif query_method == "ポリゴン":
        place_poly = st.text_input("地名（ポリゴン取得）", "東京都千代田区")
        network_type = st.selectbox(
            "ネットワークタイプ", ["drive", "walk", "bike", "all"]
        )
    submitted = st.form_submit_button("ネットワークを取得・表示")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        try:
            if query_method == "地名から取得":
                G = ox.graph_from_place(place, network_type=network_type)
            elif query_method == "複数の地名":
                place_list = [p.strip() for p in places.splitlines() if p.strip()]
                G = ox.graph_from_place(place_list, network_type=network_type)
            elif query_method == "緯度経度 + 距離":
                point = (lat, lon)
                G = ox.graph_from_point(point, dist=dist, network_type=network_type)
            elif query_method == "バウンディングボックス":
                G = ox.graph_from_bbox(
                    north, south, east, west, network_type=network_type
                )
            elif query_method == "ポリゴン":
                gdf = ox.geocode_to_gdf(place_poly)
                polygon = gdf.loc[0, "geometry"]
                G = ox.graph_from_polygon(polygon, network_type=network_type)

            fig, ax = ox.plot_graph(G, bgcolor="white", show=False, close=False)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"ネットワーク取得に失敗しました: {e}")
# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---

# 🧭 Graph from Place Queries の解説

このノートブックでは、OSMnx を用いて様々な方法で都市や地理的エリアの道路ネットワークグラフを取得する方法を紹介します。OpenStreetMapから地名・バウンディングボックス・ポイント距離・ポリゴンなど、さまざまな「場所の指定方法」に対応しています。

---

## 📍 1. 地名からのグラフ取得

### 関数: `graph_from_place`

```python
G = ox.graph_from_place("Berkeley, California, USA", network_type="drive")
```

- 単一の地名文字列から道路ネットワークを取得

---

## 📍 2. リストによる複数地名の指定

```python
places = ["Berkeley, California, USA", "Piedmont, California, USA"]
G = ox.graph_from_place(places, network_type="drive")
```

- 複数の市区町村をまとめてネットワーク化可能

---

## 📐 3. 緯度経度と半径による取得

### 関数: `graph_from_point`

```python
point = (37.87, -122.27)  # 緯度, 経度
G = ox.graph_from_point(point, dist=1000, network_type="drive")
```

- 指定した地点を中心に、指定距離内のネットワークを取得
- `dist`（メートル）によって範囲を調整可能

---

## ⬛ 4. バウンディングボックスからの取得

### 関数: `graph_from_bbox`

```python
north, south, east, west = 37.89, 37.85, -122.25, -122.30
G = ox.graph_from_bbox(north, south, east, west, network_type="drive")
```

- 指定した四隅座標で囲まれたエリアのネットワークを取得

---

## 🔷 5. 多角形（ポリゴン）からの取得

### 関数: `graph_from_polygon`

```python
gdf = ox.geocode_to_gdf("Piedmont, California, USA")
polygon = gdf.loc[0, "geometry"]
G = ox.graph_from_polygon(polygon, network_type="drive")
```

- `geocode_to_gdf()` によって得られたポリゴンを使ってネットワークを取得

---

## 🖼️ 6. ネットワークの可視化

```python
ox.plot_graph(G)
```

- 上記どの方法で取得したグラフも、共通の描画関数で表示可能

---

## ✅ まとめ

| 方法 | 関数 | 説明 |
|------|------|------|
| 地名 | `graph_from_place` | 単一または複数の地名から取得 |
| 緯度経度＋半径 | `graph_from_point` | 中心点と距離から取得 |
| バウンディングボックス | `graph_from_bbox` | 範囲座標を指定 |
| ポリゴン | `graph_from_polygon` | ポリゴン形状で指定 |
| ジオコーディング補助 | `geocode_to_gdf` | ポリゴン取得に活用可能 |

---

OSMnx を使えば、都市や任意エリアの道路ネットワークを柔軟な指定方法で取得できます。解析や可視化の目的に応じて、適切な指定方法を選びましょう。
"""
)

# 📄 ファイル名: pages/11-interactive-web-mapping.py

import streamlit as st
import osmnx as ox
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="11 - Interactive Web Mapping", layout="wide")
st.title("🗺️ Interactive Web Mapping with OSMnx + Folium")

st.markdown("### 📍 場所を指定して、道路ネットワークと建物をインタラクティブマップに表示")

with st.form("web_map_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    include_buildings = st.checkbox("建物ポリゴンも表示する", value=True)
    network_type = st.selectbox("ネットワークの種類", ["drive", "walk", "bike", "all"])
    submitted = st.form_submit_button("マップを生成")

if submitted:
    with st.spinner("データを取得中..."):
        try:
            # ネットワーク取得
            G = ox.graph_from_place(place, network_type=network_type)
            nodes, edges = ox.graph_to_gdfs(G)

            # データ量制限（最大2000本）
            if len(edges) > 2000:
                edges = edges[edges["highway"].notna()].iloc[:2000]

            # 中心座標を取得
            center_lat = nodes.geometry.y.mean()
            center_lon = nodes.geometry.x.mean()

            # foliumマップ作成
            m = folium.Map(location=[center_lat, center_lon],
                           zoom_start=14, control_scale=True)

            # 道路エッジを追加（属性を表示せず軽量化）
            folium.GeoJson(edges, name="Network").add_to(m)

            # 建物の取得と追加（任意）
            if include_buildings:
                tags = {"building": True}
                buildings = ox.features_from_place(place, tags=tags)
                if not buildings.empty:
                    buildings = buildings.iloc[:1000]  # 最大1000件に制限
                    folium.GeoJson(buildings, name="Buildings").add_to(m)

            folium.LayerControl().add_to(m)

            # 表示
            st.markdown("#### 🌍 インタラクティブマップ")
            st_data = st_folium(m, width=800, height=600)

        except Exception as e:
            st.error(f"マップ生成に失敗しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown("""
---
# 🗺️ Interactive Web Mapping with OSMnx and Folium の解説

このノートブックでは、OSMnxで取得した道路ネットワークや建物ポリゴンを、foliumライブラリを使ってWebブラウザ上のインタラクティブマップに表示する方法を紹介します。  
foliumはLeaflet.jsベースのPythonライブラリで、ユーザーが地図をパン・ズーム・クリックできるUIを簡単に構築できます。

---

## 📍 1. ネットワークの取得

```python
import osmnx as ox

G = ox.graph_from_place("Piedmont, California, USA", network_type="drive")
```

- 指定地域の自動車道路ネットワークを取得します。

---

## 🧱 2. グラフをGeoDataFrameに変換

```python
nodes, edges = ox.graph_to_gdfs(G)
```

- foliumはGeoPandasのGeoDataFrameをベースに描画するため、ノード・エッジを分離します。

---

## 🌐 3. folium マップの作成

```python
import folium

m = folium.Map(location=[37.8289, -122.2661], zoom_start=14)
```

- `location` には中心座標を指定（緯度・経度）
- `zoom_start` は初期ズームレベルを設定

---

## 🛣️ 4. GeoDataFrameをfoliumに追加

```python
folium.GeoJson(edges).add_to(m)
```

- `edges` のライン（道路）を地図に追加
- `folium.GeoJson` は各ジオメトリを描画＋属性もポップアップ表示可能

---

## 🧱 5. 建物ポリゴンの追加（応用）

```python
tags = {"building": True}
gdf = ox.features_from_place("Piedmont, California, USA", tags)
folium.GeoJson(gdf).add_to(m)
```

- 建物データも取得して、ポリゴンとして表示可能
- ネットワークや行政境界との重ね合わせが可能

---

## 💾 6. マップの保存と表示

```python
m.save("map.html")
```

- HTMLファイルとして保存すれば、ブラウザで単独閲覧可能
- Jupyter Notebook上では `m` と書くだけでインライン表示される

---

## ✅ まとめ

| ステップ | 使用関数 | 内容 |
|----------|-----------|------|
| ネットワーク取得 | `graph_from_place` | OSMからネットワークを取得 |
| GDF変換 | `graph_to_gdfs` | folium互換の形式に変換 |
| 地図作成 | `folium.Map` | 背景地図を作成 |
| データ追加 | `folium.GeoJson(...)` | 道路・建物等を重ねて描画 |
| 書き出し | `.save("map.html")` | 地図をHTMLとして保存 |

---

foliumを使うことで、OSMnxの解析結果をWeb上で誰でも触れる形で共有できます。地図ベースのインタラクティブな可視化は、都市分析・市民向け報告・教育などに非常に効果的です。
""")

# 📄 ファイル名の例: pages/01-overview-osmnx.py

import streamlit as st
import osmnx as ox
import tempfile
import os

# ページ設定
st.set_page_config(page_title="01 - OSMnx Overview", layout="wide")
st.title("🗺️ OSMnx Overview")

# 入力フォーム（メインコンテンツ）
st.markdown("### 📍 場所とネットワークタイプを指定")

with st.form("place_form"):
    place_name = st.text_input(
        "場所の名前", placeholder="東京都千代田区丸の内", value="東京都千代田区丸の内"
    )
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    col1, col2, col3 = st.columns(3)
    with col1:
        show_graph = st.form_submit_button("① ネットワーク表示")
    with col2:
        show_buildings = st.form_submit_button("② 建物表示")
    with col3:
        show_stats = st.form_submit_button("③ 統計量表示")

# 共通処理：ネットワーク取得
G = None
if show_graph or show_stats:
    try:
        G = ox.graph_from_place(place_name, network_type=network_type)
    except Exception as e:
        st.error(f"ネットワーク取得に失敗しました: {e}")

# グラフ描画
if show_graph and G:
    with st.spinner("ネットワークを描画中..."):
        fig, ax = ox.plot_graph(
            G, bgcolor="w", node_size=0, edge_color="black", show=False, close=False
        )
        st.pyplot(fig)

# 建物表示
if show_buildings:
    with st.spinner("建物データ取得中..."):
        try:
            tags = {"building": True}
            gdf = ox.features_from_place(place_name, tags=tags)
            fig, ax = ox.plot_footprints(
                gdf, color="black", bgcolor="w", show=False, close=False
            )
            st.pyplot(fig)
        except Exception as e:
            st.error(f"建物データの取得に失敗しました: {e}")

# 統計量表示
if show_stats and G:
    with st.spinner("統計量を計算中..."):
        try:
            stats = ox.basic_stats(G)
            st.subheader("📊 基本統計量")
            for k, v in stats.items():
                st.markdown(f"- **{k}**: {v}")
        except Exception as e:
            st.error(f"統計量の取得に失敗しました: {e}")

# 保存・読み込み（ダウンロード用）
st.markdown("### 💾 データの保存")
if G:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 GraphMLとして保存"):
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".graphml"
            ) as tmp_file:
                ox.save_graphml(G, filepath=tmp_file.name)
                with open(tmp_file.name, "rb") as f:
                    st.download_button("Download GraphML", f, file_name="graph.graphml")
                os.remove(tmp_file.name)

    with col2:
        if st.button("📥 GeoPackageとして保存"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".gpkg") as tmp_file:
                ox.save_graph_geopackage(G, filepath=tmp_file.name)
                with open(tmp_file.name, "rb") as f:
                    st.download_button("Download GPKG", f, file_name="graph.gpkg")
                os.remove(tmp_file.name)

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---

# 🗺️ OSMnx Overviewの解説

OSMnx は、OpenStreetMap（OSM）から地理空間データを取得し、都市スケールのネットワーク分析や可視化を行うための Python ライブラリです。このノートブックでは、OSMnx の基礎的な使い方と、都市データの取得・描画・保存の方法を紹介します。

---

## 📍 1. 地理空間ネットワークの取得

### 関数: `graph_from_place`

```python
import osmnx as ox
G = ox.graph_from_place("Berkeley, California, USA", network_type="drive")
```

* **目的**: OSMから指定した都市範囲の道路ネットワークを取得
* **引数**:

  * `place_name`: 地名（例: "Tokyo, Japan"）
  * `network_type`: "drive", "walk", "bike", "all" など
* **返り値**: NetworkX形式のグラフ

---

## 🧭 2. ネットワークの描画

### 関数: `plot_graph`

```python
ox.plot_graph(G)
```

* 取得したグラフを地図上にプロット
* デフォルトでは Matplotlib を用いて描画

---

## 🏙️ 3. 建物ポリゴンの取得

### 関数: `features_from_place`

```python
tags = {"building": True}
gdf = ox.features_from_place("Berkeley, California, USA", tags=tags)
```

* 建物や道路など任意のOSMフィーチャを取得
* 取得されるのはGeoDataFrame形式（形状＋属性）

---

## 🎨 4. 建物フットプリントの描画

### 関数: `plot_footprints`

```python
ox.plot_footprints(gdf)
```

* 建物のポリゴン形状を地図上に可視化

---

## 💾 5. データの保存と読み込み

### 保存: `save_graphml`, `save_graph_geopackage`

```python
ox.save_graphml(G, filepath="graph.graphml")
```

* グラフを `.graphml` や `.gpkg` 形式で保存可能

### 読み込み: `load_graphml`, `load_graph_geopackage`

```python
G = ox.load_graphml("graph.graphml")
```

* 保存されたグラフを再利用する際に便利

---

## 📊 6. ネットワーク統計量の算出

### 関数: `basic_stats`

```python
stats = ox.basic_stats(G)
```

* ノード数、エッジ数、密度、平均ストリート長などを自動で計算
* 結果は辞書形式で返される

---

## ✅ まとめ

| 操作内容     | 使用関数                            | 結果                 |
| -------- | ------------------------------- | ------------------ |
| ネットワーク取得 | `graph_from_place`              | NetworkX グラフオブジェクト |
| 建物情報取得   | `features_from_place`           | GeoDataFrame       |
| 図化       | `plot_graph`, `plot_footprints` | 地図描画（Matplotlib）   |
| 保存と読込    | `save_graphml`, `load_graphml`  | グラフの再利用が可能         |
| 統計       | `basic_stats`                   | 構造的な数値分析           |

---

OSMnx は都市構造の可視化・分析において強力なツールであり、研究や実務の多様なユースケースに適用できます。今後の分析の基盤として、このノートブックが示す基本操作を理解しておくことは重要です。
"""
)

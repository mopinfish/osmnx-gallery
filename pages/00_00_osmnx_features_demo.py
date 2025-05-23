# 📄 ファイル名の例: pages/00-osmnx-features-demo.py

import streamlit as st
import osmnx as ox

# --------------------
# ページ設定
# --------------------
st.set_page_config(page_title="00 - OSMnx Features Demo", layout="wide")
st.title("📦 OSMnx Features Demo")

# --------------------
# 入力フォーム（メインカラムに配置）
# --------------------
st.markdown("### 📍 場所とネットワークタイプを指定")

with st.form("place_form"):
    place_name = st.text_input(
        "場所の名前", placeholder="東京都千代田区丸の内", value="東京都千代田区丸の内"
    )
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    col1, col2 = st.columns(2)
    with col1:
        get_graph = st.form_submit_button("ネットワークを取得・表示")
    with col2:
        get_buildings = st.form_submit_button("建物を取得・表示")

# --------------------
# ネットワーク取得と描画
# --------------------
if get_graph:
    with st.spinner("ネットワークを取得中..."):
        try:
            G = ox.graph_from_place(place_name, network_type=network_type)
            fig, ax = ox.plot_graph(
                G, bgcolor="w", node_size=0, edge_color="black", show=False, close=False
            )
            st.pyplot(fig)
        except Exception as e:
            st.error(f"ネットワークの取得に失敗しました: {e}")

# --------------------
# 建物ポリゴンの取得と描画
# --------------------
if get_buildings:
    with st.spinner("建物を取得中..."):
        try:
            tags = {"building": True}
            gdf = ox.features_from_place(place_name, tags=tags)
            fig, ax = ox.plot_footprints(
                gdf, color="black", bgcolor="w", show=False, close=False
            )
            st.pyplot(fig)
        except Exception as e:
            st.error(f"建物データの取得に失敗しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---

# 📦 OSMnx Features Demoの解説

このノートブックでは、Pythonの強力な地理空間分析ライブラリ「OSMnx」の主な機能を紹介します。OpenStreetMapのデータを活用して、都市の道路ネットワークを簡単に取得・分析・可視化することができます。

---

## 🔧 基本機能のデモ

### ✅ 1. グラフの取得（`graph_from_place`）

#### 使用方法

指定した場所の道路ネットワークを取得します。

```python
import osmnx as ox

G = ox.graph_from_place("Piedmont, California, USA", network_type="drive")
```

#### 説明

* `graph_from_place`: 地名（place name）からネットワークを取得
* `network_type="drive"`: 自動車が走行可能な道路ネットワークを対象

#### 実行結果

* NetworkX形式のグラフが生成され、ノードとエッジ情報を保持
* ノード数やエッジ数の確認が可能

```python
print(ox.stats.basic_stats(G, clean_int_tol=15))
```

---

### ✅ 2. 可視化（`plot_graph`）

#### 使用方法

取得したネットワークを描画します。

```python
ox.plot_graph(G)
```

#### 実行結果

* 地図ベースのネットワークグラフが表示されます。
* ノードとエッジが道路の形に沿って描画される。

---

### ✅ 3. 建物フットプリントの取得（`geometries_from_place`）

#### 使用方法

建物や自然地物を含むOpenStreetMapのジオメトリデータを取得します。

```python
tags = {"building": True}
gdf = ox.geometries_from_place("Piedmont, California, USA", tags)
```

#### 実行結果

* GeoDataFrame形式で建物情報を取得（ポリゴン・ライン等のジオメトリ）
* 地理空間属性（住所や用途）も含む

---

### ✅ 4. 図化（`plot_footprints`）

#### 使用方法

取得した建物を可視化します。

```python
ox.plot_footprints(gdf)
```

#### 実行結果

* 建物の形状を地図上に描画
* 市街地の形状や密度を視覚的に把握可能

---

## 🗂 その他の便利な関数

| 関数名                                         | 説明                  |
| ------------------------------------------- | ------------------- |
| `graph_from_address`                        | 住所から緯度経度を取得してグラフを取得 |
| `graph_from_point`                          | 緯度経度座標から指定範囲のグラフを取得 |
| `save_graphml` / `load_graphml`             | ネットワークの保存と再利用       |
| `add_edge_speeds` / `add_edge_travel_times` | エッジに速度や所要時間を付加      |

---

## 📌 結論

OSMnxは、都市スケールの道路ネットワーク分析や可視化、建物・土地利用データの取得などにおいて非常に強力なツールです。本ノートブックではそのエントリーポイントとなる基本機能を紹介しました。
"""
)

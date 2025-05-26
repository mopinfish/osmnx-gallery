# 📄 ファイル名: pages/08-custom-filters-infrastructure.py

import streamlit as st
import osmnx as ox

st.set_page_config(
    page_title="08 - Custom Filters for Infrastructure", layout="wide")
st.title("🏗️ Custom Filters for Infrastructure")

st.markdown("### 📍 地名とOSMカスタムフィルターを指定して、インフラ構造を抽出・可視化")

with st.form("custom_filter_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    custom_filter = st.text_input(
        "Overpass API用のカスタムフィルター（例: [\"railway\"~\"rail\"]）",
        '["railway"~"rail"]'
    )
    network_type = st.selectbox(
        "グラフ構造のタイプ", ["all", "walk", "bike", "drive", "None (custom only)"])
    show_nodes = st.checkbox("ノードを表示", value=False)
    edge_color = st.color_picker("エッジの色", "#1f77b4")
    edge_width = st.slider("エッジの太さ", 0.1, 5.0, 1.0, 0.1)
    submitted = st.form_submit_button("取得・描画")

if submitted:
    with st.spinner("カスタムフィルターでネットワークを取得中..."):
        try:
            nt = network_type if network_type != "None (custom only)" else None
            G = ox.graph_from_place(
                place, network_type=nt, custom_filter=custom_filter)

            fig, ax = ox.plot_graph(
                G,
                node_size=10 if show_nodes else 0,
                edge_color=edge_color,
                edge_linewidth=edge_width,
                bgcolor="white",
                show=False,
                close=False
            )
            st.pyplot(fig)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown("""
---
# 🏗️ Custom Filters for Infrastructure の解説

このノートブックでは、OpenStreetMapのタグを自由に指定して、道路以外のインフラ（鉄道、運河、電線、水路など）をOSMnxで抽出・可視化する方法を紹介します。

---

## 🧾 1. カスタムタグフィルターとは？

OpenStreetMapのデータは、道路以外にも様々な**インフラ情報**を持っています。  
OSMnxでは、`custom_filter` 引数を指定することで、任意のタグ条件でデータを抽出できます。

---

## 🧲 2. 鉄道ネットワークの取得（例）

```python
import osmnx as ox

place = "Manhattan, New York, USA"
cf = '["railway"~"rail"]'
G = ox.graph_from_place(place, custom_filter=cf)
```

- `"railway"~"rail"` は鉄道路線（main line）を対象とするOverpassクエリ
- 自動車・歩行者以外のネットワーク構造も `networkx.MultiDiGraph` として取得可能

---

## 🔌 3. 電力インフラの取得

```python
cf = '["power"~"line"]'
G = ox.graph_from_place(place, custom_filter=cf)
```

- 送電線などのインフラ構造を取得
- 高電圧送電のネットワーク分析や視覚化に活用可能

---

## 🏞️ 4. 河川・運河などの水路インフラ

```python
cf = '["waterway"]'
G = ox.graph_from_place(place, custom_filter=cf)
```

- 自然水路や運河などを含む「水に関する流路構造」が対象
- 特に洪水対策・流域モデリングで有用

---

## 🖼️ 5. 描画とスタイル設定

```python
ox.plot_graph(G, node_size=0, edge_color="blue", edge_linewidth=1)
```

- `node_size=0` によりインフラ構造の「線」部分を強調
- カラースキームや太さをカスタムして地図スタイルに適合

---

## ✅ まとめ

| フィルター対象 | custom_filter例 | 備考 |
|----------------|------------------|------|
| 鉄道 | `["railway"~"rail"]` | 本線・地下鉄など |
| 電力 | `["power"~"line"]` | 送電線・鉄塔など |
| 水路 | `["waterway"]` | 河川・用水路など |
| 任意インフラ | 複数のタグもAND/OR条件で記述可 | `'["railway"~"rail|subway"]'` など |

---

この方法を使えば、道路以外のネットワーク構造も自由に抽出・分析・可視化することができます。都市計画・インフラ管理・災害対策などの分野で、OSMの多様なタグ情報を活かす高度な応用が可能です。
""")

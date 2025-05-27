# 📄 ファイル名: pages/09-example-figure-ground.py

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="09 - Figure-Ground Diagram", layout="wide")
st.title("🏙️ Figure-Ground Diagram of Urban Form")

st.markdown("### 📍 場所とビジュアル設定を指定して、建物・道路・交差点を可視化")

with st.form("figure_ground_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    network_type = st.selectbox(
        "道路ネットワークの種類", ["drive", "walk", "bike", "all"]
    )

    st.markdown("#### 🎨 ビジュアル設定")
    building_color = st.color_picker("建物の色（図）", "#000000")
    road_color = st.color_picker("道路の色（地）", "#cccccc")
    show_nodes = st.checkbox("交差点（ノード）を表示", value=True)
    node_color = st.color_picker("ノードの色", "#ff0000")
    node_size = st.slider("ノードサイズ", min_value=1, max_value=20, value=5)

    submitted = st.form_submit_button("描画")

if submitted:
    with st.spinner("データ取得中..."):
        try:
            # 建物ポリゴンの取得
            tags = {"building": True}
            buildings = ox.features_from_place(place, tags=tags)

            # 道路ネットワークの取得
            G = ox.graph_from_place(place, network_type=network_type)
            nodes, edges = ox.graph_to_gdfs(G)

            # 描画
            fig, ax = plt.subplots(figsize=(8, 8))
            edges.plot(ax=ax, linewidth=0.5, color=road_color, zorder=1)
            buildings.plot(ax=ax, facecolor=building_color, edgecolor="none", zorder=2)

            if show_nodes:
                nodes.plot(ax=ax, color=node_color, markersize=node_size, zorder=3)

            ax.set_axis_off()
            plt.tight_layout()

            st.pyplot(fig)

        except Exception as e:
            st.error(f"描画中にエラーが発生しました: {e}")


# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🏙️ Example: Figure-Ground Diagram の解説

このノートブックでは、都市における建物（図）と空間（地）を対比的に可視化する「figure-ground（図と地）」図法を、OSMnxを用いて作成する方法を紹介します。  
建物と道路の密度・配置を比較することで、都市構造の可視的なパターンを理解するのに役立ちます。

---

## 📍 1. 地名から建物情報を取得

```python
import osmnx as ox

gdf = ox.geometries_from_place("Piedmont, California, USA", tags={"building": True})
```

- `geometries_from_place()` を使って、OpenStreetMap から「建物」に関するポリゴン情報を取得
- `tags={"building": True}` により、すべての建物に関するオブジェクトを対象にする

---

## 🛣️ 2. 地名から道路ネットワークを取得

```python
G = ox.graph_from_place("Piedmont, California, USA", network_type="drive")
edges = ox.graph_to_gdfs(G, nodes=False)
```

- 自動車用ネットワーク（drive）を取得
- `graph_to_gdfs()` によってエッジ（道路線形）の GeoDataFrame を得る

---

## 🖼️ 3. 図と地の重ね描画

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))
edges.plot(ax=ax, linewidth=0.5, color="gray")
gdf.plot(ax=ax, facecolor="black", edgecolor="none", alpha=1)
ax.set_axis_off()
plt.tight_layout()
```

- 背景に道路（灰色）、前景に建物（黒）を塗りつぶして描画
- `facecolor="black"` とすることで建物を「図（Figure）」として強調
- 軸は非表示にして純粋な都市パターンを視覚化

---

## 🎨 4. カスタマイズのポイント

- 建物色（`facecolor`）を白黒反転させれば「地図」的表現にも切り替え可能
- 地形や土地利用と組み合わせると、都市空間の分類や分析にも応用できる
- 都市の比較にも有効（例：東京 vs パリ）

---

## ✅ まとめ

| 要素 | 対応関数 | 内容 |
|------|----------|------|
| 建物データ | `geometries_from_place` | OSMの建物ポリゴンを取得 |
| 道路データ | `graph_from_place` + `graph_to_gdfs` | 道路線形をGeoDataFrameとして取得 |
| 描画 | `GeoDataFrame.plot()` | 建物と道路を重ねて表示（図と地） |

---

この手法は都市設計、形態分析、建築教育、空間的なプレゼンテーションなどで広く活用されています。都市の構造的違いを視覚的に捉えるための直感的かつ強力なツールです。
"""
)

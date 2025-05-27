# 📄 ファイル名: pages/15-advanced-plotting.py

import streamlit as st
import osmnx as ox
import random

st.set_page_config(page_title="15 - Advanced Plotting", layout="wide")
st.title("🎨 Advanced Plotting with OSMnx")

st.markdown(
    "高度な描画オプションを活用して、OSMnxで美しい道路ネットワークを可視化します。"
)

with st.form("plotting_form"):
    place = st.text_input("場所（例: 京都市左京区）", "京都市左京区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    node_color = st.color_picker("ノードの色", "#000000")
    edge_cmap = st.selectbox(
        "エッジのカラーマップ", ["viridis", "plasma", "inferno", "cividis"]
    )
    edge_linewidth = st.slider("エッジの太さ", 0.5, 5.0, 1.0, step=0.1)
    node_size = st.slider("ノードのサイズ", 0, 50, 10)
    bgcolor = st.color_picker("背景色", "#ffffff")
    show_route = st.checkbox("ランダムなルートを描画する", value=False)
    submitted = st.form_submit_button("描画")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        try:
            G = ox.graph_from_place(place, network_type=network_type)
            G = ox.project_graph(G)

            # エッジに距離属性を色分け
            edge_colors = ox.plot.get_edge_colors_by_attr(
                G, attr="length", cmap=edge_cmap
            )

            fig, ax = ox.plot_graph(
                G,
                bgcolor=bgcolor,
                node_color=node_color,
                node_size=node_size,
                edge_color=edge_colors,
                edge_linewidth=edge_linewidth,
                show=False,
                close=False,
            )

            if show_route:
                nodes = list(G.nodes)
                orig, dest = random.sample(nodes, 2)
                route = ox.shortest_path(G, orig, dest, weight="length")
                fig, ax = ox.plot_graph_route(
                    G,
                    route,
                    route_color="red",
                    route_linewidth=4,
                    ax=ax,
                    node_size=0,
                    edge_color="lightgray",
                    show=False,
                    close=False,
                )

            st.pyplot(fig)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🎨 Advanced Plotting with OSMnx - Streamlit アプリ解説

このアプリは、OSMnx を活用して都市の道路ネットワークを高品質かつ柔軟に描画するためのインタラクティブツールです。  
ノードやエッジのスタイルを自由に設定し、背景色やルートの重ね表示なども可能です。

---

## 🔹 ユーザー設定項目（フォーム）

- **場所（place）**：地名を入力（例：「京都市左京区」）
- **ネットワークタイプ**：`drive`, `walk`, `bike`, `all` から選択
- **ノードの色**：カラーピッカーで任意の色を指定
- **ノードサイズ**：スライダーでノードサイズを調整（0〜50）
- **エッジのカラーマップ**：`viridis`, `plasma`, `inferno`, `cividis` などから選択
- **エッジの太さ**：スライダーで線の太さを調整（0.5〜5.0）
- **背景色**：背景の色（白地図 or 黒地図などの選択に応用可能）
- **ランダムルート描画**：任意の2点を結ぶ最短経路を赤線で表示

---

## 🔹 処理フローと技術的なポイント

### 1. ネットワークの取得と投影

```python
G = ox.graph_from_place(place, network_type=network_type)
G = ox.project_graph(G)
```

- OSMから指定地域の道路ネットワークを取得
- プロットに適した座標系（投影）に変換

---

### 2. エッジの色を属性で可視化

```python
edge_colors = ox.plot.get_edge_colors_by_attr(G, attr="length", cmap=edge_cmap)
```

- 各エッジの `length`（道路の長さ）を色分けして描画
- 色のグラデーションにより都市構造の変化を直感的に把握

---

### 3. ネットワークの描画（基本）

```python
ox.plot_graph(..., node_color, node_size, edge_color, edge_linewidth, bgcolor)
```

- ノード色・サイズ、エッジのカラースケール、背景色などを反映
- `show=False, close=False` により Streamlit と連携可能な `fig, ax` を取得

---

### 4. ランダムルートの描画（オプション）

```python
route = ox.shortest_path(G, orig, dest, weight="length")
ox.plot_graph_route(G, route, route_color="red", ...)
```

- ネットワーク内の任意の2点から最短経路を求め、赤線で重ね描画
- ルーティング結果の視覚化や都市の可達性分析に利用可能

---

## ✅ このアプリで可能なこと

| 機能 | 説明 |
|------|------|
| 高品質な描画 | ノード・エッジ・背景を細かく制御 |
| 色分け表示 | 長さや属性に基づくカラーマップによる視覚化 |
| ルート描画 | ランダムな出発・目的地に対する最短経路を表示 |
| 対話的UI | Streamlitのフォームでリアルタイムに描画を変更可能 |

---

## 📌 応用展開

- エッジ属性の切り替え（スピード, 勾配, travel_timeなど）
- ルート間比較（複数ルート表示）
- 背景に建物や地形など他レイヤーを追加

---

このアプリは、都市地図のデザイン、ネットワークの構造可視化、都市の空間分析など、OSMnxの強力な描画機能を活かすための出発点となります。
"""
)

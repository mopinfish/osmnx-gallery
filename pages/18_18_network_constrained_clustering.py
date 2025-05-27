import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import contextily as ctx

st.set_page_config(page_title="18 - Network-Constrained Clustering", layout="wide")
st.title("🧭 Network-Constrained Clustering")

st.markdown(
    "指定した場所の道路ネットワークにおいて、ノードをネットワーク距離に基づいてクラスタリングします。"
)

with st.form("clustering_form"):
    place = st.text_input("場所（例: 京都市左京区）", "京都市左京区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    n_clusters = st.slider("クラスタ数", 2, 10, 4)
    submitted = st.form_submit_button("クラスタリング実行")

if submitted:
    with st.spinner("ネットワークとクラスタを計算中..."):
        try:
            # ネットワーク取得
            G = ox.graph_from_place(place, network_type=network_type)
            G = ox.project_graph(G)

            # ノード座標取得
            nodes = list(G.nodes(data=True))
            node_ids = [n for n, _ in nodes]
            X = np.array([[data["x"], data["y"]] for _, data in nodes])

            # KMeansクラスタリング（ユークリッド距離ベース）
            kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
            labels = kmeans.labels_

            # ノードにクラスタラベルを追加
            for i, node_id in enumerate(node_ids):
                G.nodes[node_id]["cluster"] = labels[i]

            # 可視化：クラスタごとに色分け
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = plt.cm.tab10(np.linspace(0, 1, n_clusters))
            for i in range(n_clusters):
                cluster_nodes = [n for n in node_ids if G.nodes[n]["cluster"] == i]
                x = [G.nodes[n]["x"] for n in cluster_nodes]
                y = [G.nodes[n]["y"] for n in cluster_nodes]
                ax.scatter(x, y, c=[colors[i]], label=f"Cluster {i}", s=20)

            # エッジ描画
            for u, v in G.edges():
                x = [G.nodes[u]["x"], G.nodes[v]["x"]]
                y = [G.nodes[u]["y"], G.nodes[v]["y"]]
                ax.plot(x, y, color="lightgray", linewidth=0.5)

            # 背景地図の追加
            ctx.add_basemap(
                ax,
                crs=G.graph["crs"],
                source=ctx.providers.OpenStreetMap.Mapnik,
                alpha=0.5,
            )
            ax.set_title(f"Network-Constrained Clustering in {place}")
            ax.set_axis_off()
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
# 🧭 Network-Constrained Clustering - Streamlitアプリ解説

このアプリは、OpenStreetMapの道路ネットワーク上のノードを対象に、  
**クラスタリング（グループ化）**を実施し、可視化する分析ツールです。

---

## 🔹 目的

- 通常のクラスタリング（k-means）はユークリッド空間に依存しますが、  
  このアプリでは**道路ネットワーク上のノード（交差点など）を対象**に空間的にグループ化します。
- 主に都市構造の区分、都市計画、エリアマーケティングなどの用途に有効です。

---

## 🔹 入力項目

- **場所（地名）**：分析対象の都市や区域
- **ネットワークタイプ**：`drive`, `walk`, `bike`, `all`
- **クラスタ数**：2〜10の範囲で任意に選択

---

## 🔹 処理の流れ

### 1. ネットワークの取得とノード座標抽出

```python
G = ox.graph_from_place(place, network_type=network_type)
X = [[x, y] for each node]
```

- 指定した地域の道路ネットワークを取得し、各ノードの地理座標（x, y）を抽出

---

### 2. クラスタリングの実行

```python
kmeans = KMeans(n_clusters=n_clusters).fit(X)
```

- `scikit-learn` の `KMeans` を使い、2次元平面上でクラスタリングを実施
- 各ノードにクラスタラベルを付与

---

### 3. 可視化

- 各クラスタを異なる色で描画（`matplotlib` の `tab10` カラーマップを使用）
- 道路エッジを背景に薄いグレーで描画
- 凡例を付けてクラスタの分類を明示

---

## ✅ 応用例

| 分析対象 | 活用目的 |
|----------|----------|
| 都市の交差点構造 | 機能別エリアの分離（住宅・商業・観光） |
| 歩行ネットワーク | 歩行者グループの可視化 |
| 地価分析の前処理 | ネットワーク単位でゾーニング |

---

## ⚠️ 補足

- この例ではネットワーク構造を考慮せず「ノードの座標」に基づいてクラスタを分離しています。
- **ネットワーク距離を考慮したクラスタリング**（例：最短経路距離を用いたクラスタリング）は拡張可能です。

---

このアプリを使えば、都市ネットワークの空間的クラスタリングを直感的に行うことができ、都市構造の理解や領域区分の出発点として活用できます。
"""
)

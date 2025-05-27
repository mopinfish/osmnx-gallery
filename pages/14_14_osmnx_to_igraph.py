# 📄 ファイル名: pages/14-osmnx-to-igraph.py

import streamlit as st
import osmnx as ox
import igraph as ig
import pandas as pd

st.set_page_config(page_title="14 - Convert to iGraph", layout="wide")
st.title("🔁 Convert OSMnx Network to iGraph")

st.markdown(
    "OSMnxで取得した道路ネットワークをNetworkX形式からiGraph形式に変換し、基本的な分析を行います。"
)

with st.form("osmnx_to_igraph_form"):
    place = st.text_input("場所を指定（例: 東京都千代田区）", "東京都千代田区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    directed = st.checkbox("有向グラフとして変換", value=True)
    submitted = st.form_submit_button("ネットワークを取得・変換")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        try:
            # OSMnxでネットワーク取得（デフォルトで簡素化済み）
            G_nx = ox.graph_from_place(place, network_type=network_type)
            if not directed:
                G_nx = G_nx.to_undirected()

            # igraphへの変換
            G_ig = ig.Graph(directed=directed)
            node_mapping = {}  # NetworkXノードID → igraphノードID
            for i, node in enumerate(G_nx.nodes()):
                G_ig.add_vertex(name=str(node))
                node_mapping[node] = i

            for u, v in G_nx.edges():
                G_ig.add_edge(node_mapping[u], node_mapping[v])

            # 基本統計表示
            st.subheader("📊 基本統計")
            st.markdown(f"- ノード数: `{G_ig.vcount()}`")
            st.markdown(f"- エッジ数: `{G_ig.ecount()}`")
            st.markdown(f"- 有向グラフ: `{G_ig.is_directed()}`")

            # Degree Centralityを計算
            degrees = G_ig.degree()
            top_k = 10
            top_nodes = sorted(enumerate(degrees), key=lambda x: x[1], reverse=True)[
                :top_k
            ]
            df_top = pd.DataFrame(
                {
                    "igraph_node_id": [n for n, _ in top_nodes],
                    "degree": [d for _, d in top_nodes],
                }
            )
            st.subheader(f"⭐ Degree Centrality 上位 {top_k} ノード")
            st.dataframe(df_top)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🔁 OSMnx to iGraph - Streamlit アプリ解説

このアプリは、OSMnxで取得した都市の道路ネットワークを NetworkX形式で取得し、それを iGraph形式に変換して解析するデモツールです。  
Node数・Edge数の基本統計に加えて、Degree Centrality（次数中心性）の上位ノードを表示します。

---

## 🔹 入力パラメータ

- **場所（place）**：例：「東京都千代田区」
- **ネットワークタイプ**：`drive`, `walk`, `bike`, `all` など
- **有向グラフフラグ**：有向グラフ（`True`）または無向グラフ（`False`）

---

## 🔹 処理ステップ

### 1. OSMnx による道路ネットワーク取得

```python
G_nx = ox.graph_from_place(place, network_type=network_type)
```

- 指定された地域から OpenStreetMap の道路ネットワークを取得
- 結果は NetworkX の `MultiDiGraph` として構成される

---

### 2. NetworkX → iGraph への変換

```python
G_ig = ig.Graph(directed=directed)
```

- 各ノードは `add_vertex()`、エッジは `add_edge()` で再構成
- `node_mapping` を使って NetworkX ノードIDを iGraphノードID に変換

---

### 3. 基本統計情報の表示

```python
G_ig.vcount()  # ノード数
G_ig.ecount()  # エッジ数
G_ig.is_directed()  # 有向性の確認
```

- グラフ構造の規模を把握するのに有用

---

### 4. Degree Centrality（次数中心性）の計算と表示

```python
degrees = G_ig.degree()
```

- 各ノードの次数を計算
- 上位10ノードを抽出して表として表示

```python
pd.DataFrame({
    "igraph_node_id": [...],
    "degree": [...]
})
```

---

## ✅ 出力内容

- ネットワークの基本統計量（ノード数、エッジ数、有向グラフかどうか）
- Degree Centrality 上位10ノードのリスト（iGraphノードIDと次数）

---

## 📌 応用展開のヒント

| 指標 | 関数 |
|------|------|
| 媒介中心性 (Betweenness) | `G_ig.betweenness()` |
| 近接中心性 (Closeness) | `G_ig.closeness()` |
| ページランク | `G_ig.pagerank()` |
| 固有ベクトル中心性 | `G_ig.eigenvector_centrality()` |

---

このアプリを活用することで、NetworkXでは扱いづらい大規模ネットワークの解析や、パフォーマンスの求められる中心性計算を `igraph` を用いて効率よく行うことができます。
"""
)

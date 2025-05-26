# 📄 ファイル名: pages/06-stats-indicators-centrality.py

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import streamlit as st
import osmnx as ox
import networkx as nx

st.set_page_config(
    page_title="06 - Network Statistics and Centrality", layout="wide")
st.title("📊 Street Network Statistics and Centrality Indicators")

st.markdown("### 📍 場所と解析対象の選択")

# --- 事前に追加 ---


@st.cache_data(show_spinner="Closeness中心性をキャッシュから取得中...")
def compute_closeness(_G_proj):
    return nx.closeness_centrality(_G_proj, distance="length")


@st.cache_data(show_spinner="Betweenness中心性をキャッシュから取得中...")
def compute_betweenness(_G_proj, use_approximation=False):
    if use_approximation:
        return nx.betweenness_centrality(_G_proj, weight="length", normalized=True, k=100)
    else:
        return nx.betweenness_centrality(_G_proj, weight="length", normalized=True)


with st.form("centrality_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    analyze_stats = st.checkbox("📈 基本統計量を表示", value=True)
    analyze_centrality = st.checkbox("🧠 中心性を可視化", value=True)
    submitted = st.form_submit_button("解析実行")

if submitted:
    with st.spinner("ネットワークを取得中..."):
        try:
            G = ox.graph_from_place(place, network_type=network_type)
            G_proj = ox.project_graph(G)

            # --------------------
            # 基本統計量の出力
            # --------------------
            if analyze_stats:
                st.subheader("📈 基本統計量")
                stats = ox.basic_stats(G)  # ✅ clean_intersects 引数は削除
                for k, v in stats.items():
                    st.markdown(f"- **{k}**: {v}")

            # --------------------
            # 中心性の可視化
            # --------------------
            if analyze_centrality:
                st.subheader("🧠 中心性（Closeness / Betweenness）")

                # -----------------------
                # Closeness中心性
                # -----------------------
                closeness = compute_closeness(G_proj)
                st.markdown("#### 📍 近接中心性（Closeness Centrality）")

                nc_close = [closeness[node] for node in G_proj.nodes()]
                cmap = cm.get_cmap("viridis")
                norm = colors.Normalize(vmin=min(nc_close), vmax=max(nc_close))

                fig1, ax1 = plt.subplots(figsize=(8, 8))
                ox.plot_graph(
                    G_proj,
                    ax=ax1,
                    show=False,
                    close=False,
                    edge_color="lightgray",
                    edge_linewidth=0.5,
                    node_size=0,
                )
                x = [G_proj.nodes[n]["x"] for n in G_proj.nodes()]
                y = [G_proj.nodes[n]["y"] for n in G_proj.nodes()]
                sc = ax1.scatter(x, y, c=nc_close, cmap=cmap,
                                 norm=norm, s=10, zorder=3)
                fig1.colorbar(sc, ax=ax1, shrink=0.7).set_label(
                    "Closeness Centrality")
                st.pyplot(fig1)

                # -----------------------
                # Betweenness中心性（ノード数が多い場合は近似）
                # -----------------------
                st.markdown("#### 📍 媒介中心性（Betweenness Centrality）")
                use_approx = G_proj.number_of_nodes() > 300  # 任意の閾値
                if use_approx:
                    st.info(
                        "ノード数が多いため、betweennessは近似（k=100）で計算します。"
                    )
                else:
                    st.info("正確なbetweennessを計算します。")

                betweenness = compute_betweenness(
                    G_proj, use_approximation=use_approx)
                nc_btw = [betweenness[node] for node in G_proj.nodes()]
                norm = colors.Normalize(vmin=min(nc_btw), vmax=max(nc_btw))

                fig2, ax2 = plt.subplots(figsize=(8, 8))
                ox.plot_graph(
                    G_proj,
                    ax=ax2,
                    show=False,
                    close=False,
                    edge_color="lightgray",
                    edge_linewidth=0.5,
                    node_size=0,
                )
                sc = ax2.scatter(x, y, c=nc_btw, cmap=cmap,
                                 norm=norm, s=10, zorder=3)
                fig2.colorbar(sc, ax=ax2, shrink=0.7).set_label(
                    "Betweenness Centrality"
                )
                st.pyplot(fig2)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 📊 Street Network Statistics and Centrality Indicators の解説

このノートブックでは、OSMnxで取得した都市の道路ネットワークに対して、基本的な統計量と中心性（centrality）指標を計算する方法を紹介します。これらの指標は、ネットワークの構造的特徴を定量的に把握するのに役立ちます。

---

## 🌐 1. ネットワークの取得

```python
import osmnx as ox

G = ox.graph_from_place("Piedmont, California, USA", network_type="drive")
```

- 指定した都市の自動車用道路ネットワークを取得します。

---

## 📐 2. ネットワークの基本統計量を取得

### 関数: `ox.basic_stats()`

```python
stats = ox.basic_stats(G)
```

- ノード数、エッジ数、交差点数、平均ストリート長、ネットワーク密度などが含まれます。
- 結果は辞書形式で返され、レポートや可視化に活用可能です。

---

## 🔁 3. 交差点の正規化

```python
stats = ox.basic_stats(G, clean_intersects=True)
```

- `clean_intersects=True` を指定すると、近接するノードを1つの交差点とみなして再計算します。

---

## 🧠 4. 中心性指標の計算（NetworkX）

ネットワークを簡素化・投影し、中心性指標を計算します。

```python
import networkx as nx
G_proj = ox.project_graph(G)
bc = nx.betweenness_centrality(G_proj, weight="length")
cc = nx.closeness_centrality(G_proj, distance="length")
```

- **Betweenness centrality（媒介中心性）**：ネットワーク上での重要な通過点を示す
- **Closeness centrality（近接中心性）**：他ノードへの距離の近さを示す

---

## 🖼️ 5. 可視化（中心性の空間分布）

```python
nc = [bc[node] for node in G_proj.nodes()]
ox.plot_graph(G_proj, node_color=nc, node_size=10, node_zorder=2, edge_linewidth=0.5)
```

- 中心性の値を色で表現することで、構造的に重要な位置が視覚的にわかる

---

## ✅ まとめ

| 分析内容 | 使用関数 | 出力形式 |
|----------|-----------|------------|
| 基本統計量 | `ox.basic_stats` | 辞書形式（ノード数、密度など） |
| 中心性（近接・媒介） | `nx.closeness_centrality`, `nx.betweenness_centrality` | 各ノードへのスカラー値 |
| 可視化 | `ox.plot_graph()` | ノードカラーによる空間分布 |

---

これらの統計量と中心性指標を活用することで、道路ネットワークの構造的特性や機能的中心性を把握し、都市設計や交通分析に役立てることができます。
"""
)

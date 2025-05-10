import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide")
st.title("📊 OSMnx Network Statistics & Centrality Indicators")

st.markdown("""
このページでは、都市の道路ネットワークから基本的なグラフ統計量と、
NetworkX を用いた中心性（centrality）指標（closeness・betweenness）を計算・可視化します。
""")

st.markdown("""
---
## 📘 実行している処理の解説

### ネットワーク取得と投影変換
```python
G = ox.graph.graph_from_place(place, network_type="drive")
G_proj = ox.projection.project_graph(G)
```

### 基本統計量の取得
```python
stats = ox.basic_stats.basic_stats(G_proj)
```

### 中心性指標（NetworkX を使用）
```python
nx.closeness_centrality(G_proj, distance="length")
nx.betweenness_centrality(G_proj, weight="length")
```
---
""")

with st.form("centrality_form"):
    place = st.text_input(
        "都市名（例: Piedmont, California, USA）", "Piedmont, California, USA")
    submitted = st.form_submit_button("指標計算を実行")

if submitted:
    try:
        st.info(f"{place} のネットワークを取得しています...")
        G = ox.graph.graph_from_place(place, network_type="drive")
        G_proj = ox.projection.project_graph(G)

        # 基本統計の表示
        st.subheader("📈 基本統計量")
        stats = ox.basic_stats(G_proj, clean_int_tol=15)
        for key, val in stats.items():
            if isinstance(val, (int, float)):
                st.write(f"- **{key}**: {val:.4f}")

        # 中心性の計算
        st.subheader("🔁 中心性指標の計算")
        st.caption("※ 距離に基づく closeness と重み付き betweenness を表示")
        closeness = nx.closeness_centrality(G_proj, distance="length")
        betweenness = nx.betweenness_centrality(
            G_proj, weight="length", normalized=True)

        top_close = sorted(closeness.items(),
                           key=lambda x: x[1], reverse=True)[:5]
        top_between = sorted(betweenness.items(),
                             key=lambda x: x[1], reverse=True)[:5]

        st.markdown("#### 🔝 Closeness 上位 5 ノード")
        for node, val in top_close:
            st.write(f"Node {node}: {val:.4f}")

        st.markdown("#### 🔝 Betweenness 上位 5 ノード")
        for node, val in top_between:
            st.write(f"Node {node}: {val:.4f}")

        # ネットワーク可視化
        st.subheader("🖼 ネットワーク構造の可視化")
        fig, ax = ox.plot.plot_graph(
            G_proj, show=False, close=False, node_size=8, edge_color="#999999")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

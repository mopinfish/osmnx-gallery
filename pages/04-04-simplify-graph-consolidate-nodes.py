import streamlit as st
import osmnx as ox

st.set_page_config(layout="wide")
st.title("🧱 OSMnx Graph Simplification & Node Consolidation Demo")

st.markdown(
    """
このページでは、OSMnx を使って取得した道路ネットワークを「簡素化（simplification）」し、
また複数ノードを代表点に「集約（consolidation）」する処理を体験できます。

特に、分岐のない中間ノードの削除や、交差点クラスタの代表ノード生成といった操作を扱います。
"""
)

st.markdown(
    """
---
## 📘 実行している処理の解説

### 1. ネットワークの取得と簡素化
```python
G = ox.graph.graph_from_place(place, network_type="drive", simplify=True)
```
`simplify=True` により、トポロジ的に意味のないノード（例：直線上の中間点）を削除し、エッジをまとめます。

### 2. ノードの集約（クラスタリング）
```python
G_consolidated = ox.simplification.consolidate_intersections(G_proj, tolerance=15, rebuild_graph=True)
```
これは半径15m以内の交差点ノードを1つの代表点に集約する操作です。
---
"""
)

with st.form("simplify_form"):
    place = st.text_input("都市名または地名", "Piedmont, California, USA")
    tolerance = st.slider("交差点クラスタの許容距離 (meters)", 5, 50, 15)
    submitted = st.form_submit_button("簡素化と集約を実行")

if submitted:
    try:
        G = ox.graph.graph_from_place(
            place, network_type="drive", simplify=True)
        G_proj = ox.projection.project_graph(G)

        G_cons = ox.simplification.consolidate_intersections(
            G_proj, tolerance=tolerance, rebuild_graph=True
        )

        # 可視化
        fig, ax = ox.plot.plot_graph(
            G_cons, node_size=10, node_color="red", show=False, close=False
        )
        ax.set_title(f"{place} の簡素化＋ノード集約ネットワーク")
        st.pyplot(fig)

        st.success("グラフの簡素化と集約が完了しました。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🧱 OSMnx Custom Infrastructure Filtering Demo")

st.markdown("""
このページでは、OSMnx でカスタムな Overpass クエリを用いて、
特定の道路タイプ（例：高速道路・歩道など）や施設（例：駐車場・橋など）を抽出・可視化する方法を紹介します。
""")

st.markdown("""
---
## 📘 実行している処理の解説

### カスタム Overpass フィルタの指定
```python
custom_filter = '["highway"]["area"!~"yes"]["access"!~"private"]'
G = ox.graph.graph_from_place(place, custom_filter=custom_filter, simplify=True)
```

`custom_filter` によって、OSMのタグ条件を自由に指定してインフラを絞り込み可能です。
この例では、私有地や面積タグが付与された道路を除外しています。
---
""")

with st.form("filter_form"):
    place = st.text_input("都市名またはエリア名", "Piedmont, California, USA")
    custom_filter = st.text_area("Overpass クエリ（例: [\"highway\"][\"area\"!~\"yes\"][\"access\"!~\"private\"]）",
        '["highway"]["area"!~"yes"]["access"!~"private"]', height=100)
    submitted = st.form_submit_button("カスタムフィルタで取得・表示")

if submitted:
    try:
        st.info("カスタムフィルタでネットワークを取得しています...")
        G = ox.graph.graph_from_place(place, custom_filter=custom_filter, simplify=True)
        G_proj = ox.projection.project_graph(G)

        # 描画
        fig, ax = ox.plot.plot_graph(G_proj, show=False, close=False, edge_color="#555555", node_size=0)
        ax.set_title(f"{place} - Custom Filtered Network")
        st.pyplot(fig)

        st.success("ネットワーク取得と表示が完了しました。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

import streamlit as st

st.set_page_config(page_title="OSMnx デモギャラリー", layout="wide")
st.title("📦 OSMnx デモギャラリー")
st.markdown(
    """
このアプリは [OSMnx](https://osmnx.readthedocs.io/) の公式ノートブックをベースにした Streamlit デモギャラリーです。

以下のページでは、都市の道路ネットワーク解析や空間分析、描画、ルーティング、クラスタリングなど多彩な機能を体験できます。

---

## 📂 利用可能なデモページ一覧

### 基本デモ

- [00-osmnx-features-demo.py](00-osmnx-features-demo)
- [01-overview-osmnx.py](01-overview-osmnx)
- [02-routing-speed-time.py](02-routing-speed-time)

### ネットワーク構築・操作・保存

- [03-graph-place-queries.py](03-graph-place-queries)
- [04-simplify-graph-consolidate-nodes.py](04-simplify-graph-consolidate-nodes)
- [05-save-load-networks.py](05-save-load-networks)
- [06-stats-indicators-centrality.py](06-stats-indicators-centrality)

### 描画とカスタム表示

- [07-plot-graph-over-shape.py](07-plot-graph-over-shape)
- [08-custom-filters-infrastructure.py](08-custom-filters-infrastructure)
- [09-example-figure-ground.py](09-example-figure-ground)
- [10-building-footprints.py](10-building-footprints)

### 応用機能・解析

- [11-interactive-web-mapping.py](11-interactive-web-mapping)
- [12-node-elevations-edge-grades.py](12-node-elevations-edge-grades)
- [13-isolines-isochrones.py](13-isolines-isochrones)
- [14-osmnx-to-igraph.py](14-osmnx-to-igraph)
- [15-advanced-plotting.py](15-advanced-plotting)
- [16-download-osm-geospatial-features.py](16-download-osm-geospatial-features)
- [17-street-network-orientations.py](17-street-network-orientations)
- [18-network-constrained-clustering.py](18-network-constrained-clustering)

---

各ページは左のサイドバーからもアクセス可能です。
"""
)

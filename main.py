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

- [00_osmnx_features_demo](00_osmnx_features_demo)  
  👉 OSMnxの機能を簡単に体験できるミニマルなデモ
- [01_overview_osmnx](01_overview_osmnx)  
  👉 都市ポリゴンとネットワークの重ね合わせ
- [02_routing_speed_time](02_routing_speed_time)  
  👉 最短距離と所要時間のルート比較

### ネットワーク構築・操作・保存

- [03_graph_place_queries](03_graph_place_queries)  
  👉 地名・住所・座標からネットワークを取得
- [04_simplify_graph_consolidate_nodes](04_simplify_graph_consolidate_nodes)  
  👉 ノード統合による交差点の前処理
- [05_save_load_networks](05_save_load_networks)  
  👉 ネットワークの保存と再利用
- [06_stats_indicators_centrality](06_stats_indicators_centrality)  
  👉 統計指標と中心性分析

### 描画とカスタム表示

- [07_plot_graph_over_shape](07_plot_graph_over_shape)  
  👉 都市境界とネットワークの重ね表示
- [08_custom_filters_infrastructure](08_custom_filters_infrastructure)  
  👉 OSMタグでインフラ要素を抽出
- [09_example_figure_ground](09_example_figure_ground)  
  👉 建物と空間の図式的表示
- [10_building_footprints](10_building_footprints)  
  👉 建物ポリゴンの取得と可視化

### 応用機能・解析

- [11_interactive_web_mapping](11_interactive_web_mapping)  
  👉 Leafletベースの動的マップ描画
- [12_node_elevations_edge_grades](12_node_elevations_edge_grades)  
  👉 標高・勾配の付加と可視化
- [13_isolines_isochrones](13_isolines_isochrones)  
  👉 徒歩圏等時間線の描画
- [14_osmnx_to_igraph](14_osmnx_to_igraph)  
  👉 OSMnxのネットワークをiGraph形式に変換
- [15_advanced_plotting](15_advanced_plotting)  
  👉 エッジ属性に応じた色分け描画
- [16_download_osm_geospatial_features](16_download_osm_geospatial_features)  
  👉 任意タグで地物データを取得
- [17_street_network_orientations](17_street_network_orientations)  
  👉 方位角分布による街路方向の分析
- [18_network_constrained_clustering](18_network_constrained_clustering)  
  👉 ノード位置に基づく空間クラスタリング

---

各ページは左のサイドバーからもアクセス可能です。
"""
)

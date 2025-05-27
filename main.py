import streamlit as st

st.set_page_config(page_title="📦 OSMnx デモギャラリー", layout="wide")
st.title("📦 OSMnx デモギャラリー")
st.markdown(
    """
このアプリは [OSMnx](https://osmnx.readthedocs.io/) の公式デモノートブックをもとに作成した Streamlit アプリのギャラリーページです。
都市ネットワーク解析・地理空間処理・可視化の実演をインタラクティブに体験できます。
"""
)

# リンクリスト
demos = [
    {
        "title": "00 - OSMnx Features Demo",
        "url": "https://osmnx-gallery.streamlit.app/00_osmnx_features_demo",
        "desc": "OSMnxの主要機能（ネットワーク取得、可視化、ルート探索など）をデモ形式でまとめた基本機能紹介ページです。",
    },
    {
        "title": "01 - Overview of OSMnx",
        "url": "https://osmnx-gallery.streamlit.app/01_overview_osmnx",
        "desc": "OSMnxの設計思想と主要コンポーネントの概要を示し、ネットワーク構築から可視化までの基本フローを学べます。",
    },
    {
        "title": "02 - Routing: Speed and Travel Time",
        "url": "https://osmnx-gallery.streamlit.app/02_routing_speed_time",
        "desc": "移動速度や所要時間に基づいた最短経路探索を行い、距離ルートと時間ルートを比較表示するルーティングデモです。",
    },
    {
        "title": "03 - Graph Place Queries",
        "url": "https://osmnx-gallery.streamlit.app/03_graph_place_queries",
        "desc": "地名や境界から道路ネットワークを取得し、ポリゴン範囲を指定して抽出する方法を紹介します。",
    },
    {
        "title": "04 - Simplify Graph and Consolidate Nodes",
        "url": "https://osmnx-gallery.streamlit.app/04_simplify_graph_consolidate_nodes",
        "desc": "複雑な交差点や分岐ノードを統合し、ネットワークを分析や描画に適した形に簡素化します。",
    },
    {
        "title": "05 - Save and Load Networks",
        "url": "https://osmnx-gallery.streamlit.app/05_save_load_networks",
        "desc": "取得したネットワークをGraphMLまたはGeoPackage形式で保存・再読み込みし、データ永続化を体験できます。",
    },
    {
        "title": "06 - Stats and Centrality Indicators",
        "url": "https://osmnx-gallery.streamlit.app/06_stats_indicators_centrality",
        "desc": "道路ネットワークの基本統計量と中心性（Closeness, Betweenness）を計算・可視化する分析デモです。",
    },
    {
        "title": "07 - Plot Graph Over Shape",
        "url": "https://osmnx-gallery.streamlit.app/07_plot_graph_over_shape",
        "desc": "都市ポリゴンの上にネットワークを重ねて描画し、地域的な構造との関係を可視化します。",
    },
    {
        "title": "08 - Custom Filters for Infrastructure",
        "url": "https://osmnx-gallery.streamlit.app/08_custom_filters_infrastructure",
        "desc": "カスタムOSMタグ（例：鉄道・電力線・水路）を指定して、特定インフラネットワークを取得・描画できます。",
    },
    {
        "title": "09 - Figure-Ground Diagram",
        "url": "https://osmnx-gallery.streamlit.app/09_example_figure_ground",
        "desc": "建物と道路の図と地（figure-ground）を描画し、都市の空間密度や構造パターンを視覚化します。",
    },
    {
        "title": "10 - Building Footprints",
        "url": "https://osmnx-gallery.streamlit.app/10_building_footprints",
        "desc": "OpenStreetMapの建物ポリゴンを取得し、面積に基づいた色分けなどの視覚化を行うデモです。",
    },
    {
        "title": "11 - Interactive Web Mapping",
        "url": "https://osmnx-gallery.streamlit.app/11_interactive_web_mapping",
        "desc": "foliumを用いて取得したネットワークや建物をインタラクティブなWeb地図上に可視化します。",
    },
    {
        "title": "12 - Node Elevations and Edge Grades",
        "url": "https://osmnx-gallery.streamlit.app/12_node_elevations_edge_grades",
        "desc": "ノードに標高を付加し、道路の勾配（傾斜）を算出・カラーマッピングして表示します。",
    },
    {
        "title": "13 - Isochrones and Isolines",
        "url": "https://osmnx-gallery.streamlit.app/13_isolines_isochrones",
        "desc": "ある地点から到達可能な範囲（等時間圏アイソクロン）を道路ネットワークに沿って描画します。",
    },
    {
        "title": "14 - Convert to iGraph",
        "url": "https://osmnx-gallery.streamlit.app/14_osmnx_to_igraph",
        "desc": "OSMnxのNetworkXグラフをigraphに変換し、中心性などの高速分析を行う準備をします。",
    },
    {
        "title": "15 - Advanced Plotting",
        "url": "https://osmnx-gallery.streamlit.app/15_advanced_plotting",
        "desc": "ノード色・エッジ色・背景色をカスタマイズし、より美しい地図描画を作成できます。",
    },
    {
        "title": "16 - Download OSM Features",
        "url": "https://osmnx-gallery.streamlit.app/16_download_osm_geospatial_features",
        "desc": "建物・土地利用・水域などの地理空間フィーチャをOSMから取得・可視化するツールです。",
    },
    {
        "title": "17 - Street Orientation Histogram",
        "url": "https://osmnx-gallery.streamlit.app/17_street_network_orientations",
        "desc": "都市内の道路方位角をヒストグラム化し、グリッド構造や方向性の偏りを分析します。",
    },
    {
        "title": "18 - Network-Constrained Clustering",
        "url": "https://osmnx-gallery.streamlit.app/18_network_constrained_clustering",
        "desc": "ノードの座標に基づいてネットワーク内でクラスタリングを行い、色分けして表示します。",
    },
]

st.markdown("## 📂 利用可能なデモ一覧")
for demo in demos:
    st.markdown(f"- [{demo['title']}]({demo['url']})  \n  _{demo['desc']}_")

st.markdown(
    """
各ページは左のサイドバーからもアクセス可能です。
"""
)

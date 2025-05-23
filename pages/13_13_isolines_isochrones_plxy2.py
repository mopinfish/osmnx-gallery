import streamlit as st
import networkx as nx
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# --- アプリ設定 ---
st.set_page_config(page_title="OSMnx等時圏分析", layout="wide")
ox.settings.log_console = True
ox.settings.use_cache = True

# --- 主要関数解説 ---
st.markdown(
    """
## OSMnx等時圏分析の主要関数

### `ox.graph_from_place()`
```
def graph_from_place(
    query: Union[str, dict],
    network_type: str = "all_private",
    simplify: bool = True,
    retain_all: bool = False,
    truncate_by_edge: bool = False,
    buffer_dist: float = None
) -> nx.MultiDiGraph:
    '''
    地名から道路ネットワークを取得
    パラメータ:
        query: 検索地名（例: "東京都新宿区"）
        network_type: ネットワーク種別（walk/drive/bike等）
    戻り値: NetworkXグラフオブジェクト
    '''
```

### `ox.project_graph()`
```
def project_graph(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    '''
    グラフをUTM座標系に投影変換
    目的: メートル単位の正確な距離計算
    戻り値: 投影変換済みグラフ
    '''
```

### `ox.distance.nearest_nodes()`
```
def nearest_nodes(
    G: nx.MultiDiGraph,
    X: float,
    Y: float,
    return_dist: bool = False
) -> Union[int, Tuple[int, float]]:
    '''
    座標から最近傍ノードを検索
    戻り値: ノードID
    '''
```
"""
)

# --- サイドバー設定 ---
with st.sidebar:
    st.header("分析パラメータ")
    place = st.text_input("分析地域", "東京都新宿区")
    network_type = st.selectbox("移動手段", ["walk", "bike", "drive"], index=0)
    trip_times = st.multiselect(
        "時間範囲（分）", [5, 10, 15, 20, 25, 30], default=[5, 10, 15]
    )
    travel_speed = st.slider("移動速度 (km/h)", 1.0, 10.0, 4.5)
    buffer_method = st.radio("等時線生成法", ["Convex Hull", "Buffer"])

# --- メイン処理 ---


def main():
    st.title("OSMnx等時圏分析ツール")

    if st.button("等時圏生成開始"):
        with st.spinner("地理データ処理中..."):
            try:
                # 道路ネットワーク取得
                G = ox.graph_from_place(place, network_type=network_type)
                G_proj = ox.project_graph(G)

                # 中心ノード計算
                gdf_nodes = ox.convert.graph_to_gdfs(G_proj, edges=False)
                x, y = gdf_nodes.geometry.unary_union.centroid.xy
                center_node = ox.distance.nearest_nodes(G_proj, x[0], y[0])

                # エッジ移動時間計算
                meters_per_minute = travel_speed * 1000 / 60
                for u, v, k, data in G_proj.edges(data=True, keys=True):
                    data["time"] = data["length"] / meters_per_minute

                # 等時圏生成
                isochrone_polys = []
                for time in sorted(trip_times, reverse=True):
                    subgraph = nx.ego_graph(
                        G_proj, center_node, radius=time, distance="time"
                    )

                    if buffer_method == "Convex Hull":
                        poly = gpd.GeoSeries(
                            [
                                Point(data["x"], data["y"])
                                for node, data in subgraph.nodes(data=True)
                            ]
                        ).unary_union.convex_hull
                    else:
                        edge_lines = []
                        for u, v in subgraph.edges():
                            edge_data = G_proj.get_edge_data(u, v)[0]
                            if "geometry" in edge_data:
                                edge_lines.append(edge_data["geometry"])

                        nodes_gdf = gpd.GeoDataFrame(
                            geometry=[
                                Point(data["x"], data["y"])
                                for node, data in subgraph.nodes(data=True)
                            ]
                        )
                        n = nodes_gdf.buffer(50)
                        e = gpd.GeoSeries(edge_lines).buffer(20)
                        poly = n.union(e).unary_union

                    isochrone_polys.append(poly)

                # 可視化
                fig, ax = plt.subplots(figsize=(10, 10))
                ox.plot_graph(
                    G_proj, ax=ax, node_size=0, edge_color="gray", edge_linewidth=0.5
                )

                colors = ox.plot.get_colors(len(trip_times), cmap="plasma", start=0)
                for poly, color in zip(isochrone_polys, colors):
                    gpd.GeoSeries([poly]).plot(ax=ax, color=color, alpha=0.4, ec="none")

                st.pyplot(fig)
                st.session_state.isochrones = gpd.GeoDataFrame(geometry=isochrone_polys)

            except Exception as e:
                st.error(f"エラー発生: {str(e)}")


# --- データエクスポート ---
if "isochrones" in st.session_state:
    with st.expander("📤 データ出力"):
        geojson = st.session_state.isochrones.to_json()
        st.download_button(
            label="GeoJSONダウンロード",
            data=geojson,
            file_name="isochrones.geojson",
            mime="application/json",
        )

# --- ソースコード表示 ---
with st.sidebar.expander("📜 ソースコード"):
    with open(__file__, "r") as f:
        st.download_button(
            "Pythonファイルをダウンロード",
            data=f,
            file_name="isochrone_app.py",
            mime="text/python",
        )

# --- ソースコードダウンロード ---
with st.expander("📜 このページのソースコード"):
    with open(__file__, "r") as f:
        st.code(f.read(), language="python")

if __name__ == "__main__":
    main()

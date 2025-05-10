import streamlit as st
import osmnx as ox
from pathlib import Path

st.set_page_config(layout="wide")
st.title("💾 OSMnx Network Save & Load Demo")

st.markdown("""
このページでは、OSMnx を使って取得した道路ネットワークをローカルに保存したり、
保存済みのネットワークデータを再読み込みして再利用する方法を紹介します。
""")

st.markdown("""
---
## 📘 実行している処理の解説

### ネットワークを取得して保存
```python
G = ox.graph.graph_from_place(place, network_type="drive")
ox.io.save_graphml(G, filepath)
ox.io.save_graphml(G, filepath, gephi=True)
ox.save_graph_geopackage(G, filepath)
```

### 保存したネットワークを読み込む
```python
G_loaded = ox.io.load_graphml(filepath)
```

ファイル形式は `.graphml`、`.gpkg`（GeoPackage）、`.osm.pbf`（OpenStreetMap形式）などに対応しています。
---
""")

with st.form("save_load_form"):
    place = st.text_input(
        "都市名（例: Piedmont, California, USA）", "Piedmont, California, USA")
    file_prefix = st.text_input("保存ファイルのプレフィックス", "piedmont")
    submitted = st.form_submit_button("ネットワークを取得して保存・読込")

if submitted:
    try:
        st.info(f"{place} のネットワークを取得中...")
        G = ox.graph.graph_from_place(place, network_type="drive")
        path_dir = Path("networks")
        path_dir.mkdir(exist_ok=True)

        # 保存パスの定義
        graphml_path = path_dir / f"{file_prefix}.graphml"
        gpkg_path = path_dir / f"{file_prefix}.gpkg"

        # 保存
        ox.io.save_graphml(G, graphml_path)
        ox.io.save_graph_geopackage(G, gpkg_path)

        st.success(f"以下のファイルに保存しました：\n- {graphml_path}\n- {gpkg_path}")

        # 読み込みと可視化
        st.info("保存した .graphml を再読み込み中...")
        G_loaded = ox.io.load_graphml(graphml_path)
        fig, ax = ox.plot.plot_graph(G_loaded, show=False, close=False)
        ax.set_title("再読み込みされたネットワーク")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

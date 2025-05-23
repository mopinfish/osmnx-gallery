# 📄 ファイル名: pages/05-save-load-networks.py

import streamlit as st
import osmnx as ox
import tempfile
import os
import geopandas as gpd

st.set_page_config(page_title="05 - Save and Load Networks", layout="wide")
st.title("💾 Save and Load Street Networks")

st.markdown("### 📍 ネットワークの取得と保存・読み込みのデモ")

# --------------------
# 場所指定フォーム
# --------------------
with st.form("save_load_form"):
    place_name = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    action = st.radio(
        "操作を選択", ["ネットワークを取得して保存", "保存済みファイルから読み込み"]
    )
    file_format = st.selectbox("ファイル形式", ["graphml", "gpkg"])
    uploaded_file = (
        st.file_uploader("読み込み用ファイルを選択", type=["graphml", "gpkg"])
        if action == "保存済みファイルから読み込み"
        else None
    )
    submitted = st.form_submit_button("実行")

# --------------------
# 実行処理
# --------------------
G = None

if submitted:
    with st.spinner("処理中..."):
        try:
            if action == "ネットワークを取得して保存":
                # ネットワーク取得
                G = ox.graph_from_place(place_name, network_type=network_type)
                fig, ax = ox.plot_graph(G, bgcolor="white", show=False, close=False)
                st.pyplot(fig)

                # 一時保存 → ダウンロードリンク
                suffix = ".graphml" if file_format == "graphml" else ".gpkg"
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=suffix
                ) as tmp_file:
                    if file_format == "graphml":
                        ox.save_graphml(G, filepath=tmp_file.name)
                    elif file_format == "gpkg":
                        ox.save_graph_geopackage(G, filepath=tmp_file.name)
                    with open(tmp_file.name, "rb") as f:
                        st.download_button(
                            label=f"{file_format.upper()}形式でダウンロード",
                            data=f,
                            file_name=f"network.{file_format}",
                            mime="application/octet-stream",
                        )
                    os.remove(tmp_file.name)

            elif action == "保存済みファイルから読み込み":
                if uploaded_file:
                    # ファイルを一時保存
                    suffix = ".graphml" if file_format == "graphml" else ".gpkg"
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=suffix
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_file_path = tmp_file.name

                    # ファイルから読み込み
                    if file_format == "graphml":
                        G = ox.load_graphml(tmp_file_path)
                    elif file_format == "gpkg":
                        nodes = gpd.read_file(tmp_file_path, layer="nodes")
                        edges = gpd.read_file(tmp_file_path, layer="edges")

                        # 明示的に u, v, key を型変換（文字列として統一）
                        edges["u"] = edges["u"].astype(str)
                        edges["v"] = edges["v"].astype(str)
                        edges["key"] = edges["key"].astype(str)

                        # MultiIndex を安全に設定
                        edges.set_index(["u", "v", "key"], inplace=True)

                        # ノードIDとエッジIDの型を一致させる（文字列統一）
                        nodes["osmid"] = nodes["osmid"].astype(str)
                        nodes.set_index("osmid", inplace=True)

                        # グラフに変換
                        G = ox.graph_from_gdfs(nodes, edges)

                    fig, ax = ox.plot_graph(G, bgcolor="white", show=False, close=False)
                    st.pyplot(fig)
                    os.remove(tmp_file_path)
                else:
                    st.warning("読み込むファイルを選択してください。")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 💾 Save and Load Street Networks の解説

このノートブックでは、OSMnxで取得した道路ネットワークをファイルに保存し、後から再読み込みする方法を紹介します。ファイル形式には `.graphml`, `.gpkg`, `.osm` などがあり、用途に応じて使い分けることができます。

---

## 🌐 1. ネットワークの取得

```python
import osmnx as ox

G = ox.graph_from_place("Piedmont, California, USA", network_type="drive")
```

- 指定した場所の自動車用ネットワークを取得します。

---

## 💾 2. GraphML形式で保存

```python
ox.save_graphml(G, filepath="graph.graphml")
```

- `.graphml` は NetworkX と互換性があり、ネットワーク構造や属性をすべて保持します。
- 最も柔軟な形式であり、再利用や解析に便利です。

---

## 💾 3. GeoPackage形式で保存

```python
ox.save_graph_geopackage(G, filepath="graph.gpkg")
```

- `.gpkg` は空間データベースとしてQGISなどでも直接扱える形式。
- ノードとエッジが別のレイヤーとして保存されます。

---

## 💾 4. OSM XML形式で保存

```python
ox.save_graph_osm(G, filepath="graph.osm")
```

- OpenStreetMap互換の `.osm` 形式で保存。
- 他のOSMツール（JOSMなど）と連携できます。

---

## 📂 5. GraphMLファイルから読み込み

```python
G_loaded = ox.load_graphml("graph.graphml")
```

- `.graphml` ファイルを再読み込みして NetworkX グラフとして利用可能。

---

## 🗂️ 6. GeoPackageファイルから読み込み

```python
G_loaded = ox.load_graph_geopackage("graph.gpkg")
```

- `.gpkg` からグラフを再構成できます（ノードとエッジを結合）。

---

## ✅ まとめ

| 操作 | 関数 | 拡張子 | 特徴 |
|------|------|--------|------|
| 保存（GraphML） | `save_graphml` | `.graphml` | 構造＋属性、最も汎用的 |
| 保存（GeoPackage） | `save_graph_geopackage` | `.gpkg` | GISソフトにそのまま利用可 |
| 保存（OSM XML） | `save_graph_osm` | `.osm` | OSMツール向け |
| 読み込み（GraphML） | `load_graphml` | `.graphml` | 高速・安定 |
| 読み込み（GeoPackage） | `load_graph_geopackage` | `.gpkg` | 空間属性対応 |

---

OSMnxは、グラフ構造を柔軟に保存・読み込みする機能を提供しています。形式ごとの特性を理解し、ワークフローに最適な形式を選択しましょう。
"""
)

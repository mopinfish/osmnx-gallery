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

このアプリでは、OSMnxで取得した道路ネットワークをファイルに保存し、あとから再読み込みして再利用する方法を体験できます。保存形式は `.graphml` および `.gpkg`（GeoPackage）に対応しています。

---

## 🌐 1. ネットワークの取得

```python
G = ox.graph_from_place("東京都千代田区", network_type="drive")
```

- 指定した地名からOSM道路ネットワークを取得します。
- `network_type` は "drive", "walk", "bike", "all" などから選択可能です。

---

## 💾 2. 保存機能（ダウンロード可能）

### GraphML形式で保存

```python
ox.save_graphml(G, filepath="network.graphml")
```

- NetworkX互換の形式。構造・属性を完全に保持します。
- 軽量で高速な保存／読み込みが可能です。

### GeoPackage形式で保存

```python
ox.save_graph_geopackage(G, filepath="network.gpkg")
```

- QGISなどのGISツールで直接開ける形式。
- `nodes` と `edges` がレイヤーとして保存されます。

Streamlitアプリでは、いずれの形式でも一時ファイルを生成し、ダウンロードボタンから取得できます。

---

## 📂 3. 読み込み機能（アップロード対応）

### GraphML読み込み

```python
G = ox.load_graphml("network.graphml")
```

- `.graphml` 形式はそのまま `ox.load_graphml()` で読み込み可能です。

### GeoPackage（.gpkg）読み込み手順

```python
import geopandas as gpd

nodes = gpd.read_file("network.gpkg", layer="nodes")
edges = gpd.read_file("network.gpkg", layer="edges")

edges["u"] = edges["u"].astype(str)
edges["v"] = edges["v"].astype(str)
edges["key"] = edges["key"].astype(str)
edges.set_index(["u", "v", "key"], inplace=True)

nodes["osmid"] = nodes["osmid"].astype(str)
nodes.set_index("osmid", inplace=True)

G = ox.graph_from_gdfs(nodes, edges)
```

- `u, v, key` の列を文字列化し、MultiIndexに設定する必要があります。
- `graph_from_gdfs` を用いて再構築します。

---

## ✅ 機能まとめ

| 機能           | 関数／操作                              | 拡張子    |
|----------------|------------------------------------------|-----------|
| ネットワーク取得 | `graph_from_place`                      | -         |
| 保存（GraphML） | `save_graphml`                          | `.graphml`|
| 保存（GeoPackage） | `save_graph_geopackage`              | `.gpkg`   |
| 読み込み（GraphML） | `load_graphml`                      | `.graphml`|
| 読み込み（GeoPackage） | `graph_from_gdfs` + `geopandas` | `.gpkg`   |

---

## 📝 注意点

- `.gpkg` 読み込みは明示的な前処理が必要です（インデックスと型整合）。
- `.graphml` の方がPython環境では取り扱いが容易です。
- Streamlitのアップロード機能を使って、`.graphml` または `.gpkg` ファイルを読み込めます。

---
"""
)

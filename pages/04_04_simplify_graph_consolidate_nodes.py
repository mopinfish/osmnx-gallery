# 📄 ファイル名: pages/04-simplify-graph-consolidate-nodes.py

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm

# --------------------
# ✅ 日本語フォント設定（Noto Sans CJK JPを使う）
# --------------------
# 利用可能なフォントから Noto Sans CJK JP を優先設定
jp_font_candidates = [
    f
    for f in fm.findSystemFonts()
    if "NotoSansCJK" in f or "NotoSansCJKjp" in f or "Noto Sans CJK JP" in f
]
if jp_font_candidates:
    rcParams["font.family"] = fm.FontProperties(fname=jp_font_candidates[0]).get_name()
else:
    rcParams["font.family"] = "IPAexGothic"  # フォールバック（あれば）

st.set_page_config(page_title="04 - Simplify and Consolidate", layout="wide")
st.title("🔧 Simplify Graph and Consolidate Nodes")

st.markdown("### 📍 地名と処理パラメータを指定")

with st.form("simplify_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    tolerance = st.slider(
        "ノード統合の許容距離（メートル）", min_value=5, max_value=50, value=15, step=5
    )
    submitted = st.form_submit_button("グラフを取得・処理・描画")

if submitted:
    with st.spinner("データ取得と処理中..."):
        try:
            G_raw = ox.graph_from_place(place, network_type="drive", simplify=False)
            G_simple = ox.simplify_graph(G_raw)
            G_proj = ox.project_graph(G_simple)
            G_cons = ox.consolidate_intersections(G_proj, tolerance=tolerance)

            nodes_before, _ = ox.graph_to_gdfs(G_proj)
            nodes_after, _ = ox.graph_to_gdfs(G_cons)

            fig, ax = plt.subplots(figsize=(8, 8))
            nodes_before.plot(ax=ax, color="red", markersize=8, label="元のノード")
            nodes_after.plot(ax=ax, color="blue", markersize=8, label="統合後ノード")
            ax.set_title("ノード統合前後の比較")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"処理中にエラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🔧 Simplify Graph and Consolidate Nodes の解説

このノートブックでは、OSMnxで取得した道路ネットワークグラフを「簡素化」し、視覚的・構造的に扱いやすい状態に整える方法を解説します。

---

## 🏗️ 1. ネットワークの取得と描画（未簡素化）

```python
import osmnx as ox
G_unsimplified = ox.graph_from_place("Piedmont, California, USA", simplify=False)
ox.plot_graph(G_unsimplified)
```

- `simplify=False` により、OpenStreetMapに登録された「生のジオメトリ」をそのまま使用
- 各交差点に対して、実際よりも多くのノードが含まれてしまう

---

## 🔧 2. 簡素化処理の適用

```python
G = ox.simplify_graph(G_unsimplified)
```

- 冗長なノード（例：同一直線上に並ぶノード）を削除し、交差点や屈曲点だけを残す
- `geometry` 属性により、元の形状は保持される

---

## 🧱 3. ノードの統合（スナップ）

### 関数: `consolidate_intersections`

```python
import osmnx as ox
G_proj = ox.project_graph(G)
nodes_proj, edges_proj = ox.graph_to_gdfs(G_proj)
nodes_cons = ox.consolidate_intersections(nodes_proj, tolerance=15, rebuild_graph=False)
```

- `tolerance`: 統合する範囲（単位: メートル）
- 近接する複数の交差点ノードを1つにまとめ、後続処理を容易にする
- `rebuild_graph=True` を指定すると、統合済みノードを使って新しいグラフを作成

---

## 📐 4. 可視化：統合前後のノード比較

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
nodes_proj.plot(ax=ax, color="r", markersize=8, label="original")
nodes_cons.plot(ax=ax, color="b", markersize=8, label="consolidated")
plt.legend()
```

- 統合処理により、複雑だったノード配置が簡素な構造に整うことが視覚的に分かる

---

## ✅ まとめ

| ステップ | 関数 | 説明 |
|----------|------|------|
| 未簡素化で取得 | `graph_from_place(..., simplify=False)` | OSMの生データに近い形で取得 |
| グラフの簡素化 | `simplify_graph` | 冗長ノードを削除しスッキリした構造に |
| ノード統合 | `consolidate_intersections` | 指定範囲内のノードを統合 |

---

道路ネットワークの解析・可視化・モデリングを行う上で、グラフの簡素化とノード統合は非常に重要な前処理です。精度と計算効率の両立のために、目的に応じたスナップ設定や簡素化処理を行いましょう。
"""
)

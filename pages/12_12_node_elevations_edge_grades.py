import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import contextily as ctx

st.set_page_config(page_title="12 - Elevation and Grade", layout="wide")
st.title("🏔️ Node Elevations and Edge Grades")

st.markdown("### 📍 場所を指定して、標高と道路の勾配を可視化（カラースキーマ凡例付き）")

with st.form("elevation_form"):
    place = st.text_input("場所（例: 東京都文京区）", "東京都文京区")
    network_type = st.selectbox("ネットワークタイプ", ["walk", "drive", "bike", "all"])
    api_key = st.text_input("Google Elevation APIキー", type="password")
    submitted = st.form_submit_button("取得・表示")

if submitted:
    with st.spinner("ネットワークと標高データを取得中..."):
        try:
            # 1. ネットワーク取得
            G = ox.graph_from_place(place, network_type=network_type)

            # 2. 標高データ付加
            if not api_key:
                st.error("Google Elevation APIキーが必要です。")
                st.stop()

            G = ox.elevation.add_node_elevations_google(G, api_key=api_key)

            # 3. 勾配の計算
            G = ox.elevation.add_edge_grades(G)

            # 4. 勾配リスト抽出
            grades = [
                d["grade"]
                for _, _, _, d in G.edges(keys=True, data=True)
                if "grade" in d
            ]

            # 5. カラーマッピング設定
            cmap = cm.terrain
            norm = mcolors.Normalize(vmin=min(grades), vmax=max(grades))
            edge_colors = [cmap(norm(grade)) for grade in grades]

            # 6. 描画（カラーバー付き）
            fig, ax = plt.subplots(figsize=(10, 8))
            ox.plot_graph(
                G,
                ax=ax,
                edge_color=edge_colors,
                edge_linewidth=1,
                node_size=0,
                bgcolor="white",
                show=False,
                close=False,
            )
            ctx.add_basemap(
                ax,
                crs=G.graph["crs"],
                source=ctx.providers.OpenStreetMap.Mapnik,
                alpha=0.5,
            )

            # カラーバー（凡例）を追加
            sm = cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = fig.colorbar(sm, ax=ax, shrink=0.6,
                                label="Edge Grade (slope)")
            cbar.ax.tick_params(labelsize=8)

            st.pyplot(fig)

            # 7. 勾配ヒストグラム
            st.markdown("#### 📊 勾配の分布（ヒストグラム）")
            fig2, ax2 = plt.subplots()
            ax2.hist(grades, bins=30, color="purple", edgecolor="black")
            ax2.set_title("Edge Grade Distribution")
            ax2.set_xlabel("Grade (slope)")
            ax2.set_ylabel("Frequency")
            st.pyplot(fig2)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")


# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🏔️ Node Elevations and Edge Grades の解説

このノートブックでは、OSMnxを使って道路ネットワークのノード（交差点など）の標高を取得し、それに基づいて各エッジ（道路区間）の勾配（傾斜）を計算する方法を紹介します。  
これにより、地形的な困難度（坂のきつさ）を可視化・分析でき、都市設計やモビリティ分析に役立ちます。

---

## 🗺️ 1. 道路ネットワークの取得

```python
import osmnx as ox

G = ox.graph_from_place("Piedmont, California, USA", network_type="walk")
```

- 歩行者ネットワーク（`network_type="walk"`）を使用
- 傾斜分析は徒歩や自転車のルート選択に有用

---

## 🏔️ 2. ノードの標高を取得

```python
G = ox.elevation.add_node_elevations_google(G, api_key="YOUR_GOOGLE_ELEVATION_API_KEY")
```

- 各ノードに `"elevation"` 属性が追加される
- Google Elevation API を使用（要APIキー）

---

## 🧮 3. エッジの勾配（傾斜）を計算

```python
G = ox.elevation.add_edge_grades(G)
```

- 各エッジに `"grade"` 属性が追加される
- 勾配（slope）は -1〜1 の範囲で表現（負: 下り坂、正: 上り坂）

---

## 🎨 4. 勾配に応じたエッジの可視化

```python
import matplotlib.cm as cm
import matplotlib.colors as colors

edge_colors = ox.plot.get_edge_colors_by_attr(G, attr="grade", cmap="plasma", num_bins=10)
ox.plot_graph(G, edge_color=edge_colors, edge_linewidth=1, node_size=0)
```

- `get_edge_colors_by_attr()` で勾配に応じた色を生成
- `plasma`, `viridis`, `coolwarm` などのカラーマップが使用可能

---

## 📊 5. 勾配のヒストグラム

```python
grades = [d["grade"] for u, v, k, d in G.edges(keys=True, data=True) if "grade" in d]
plt.hist(grades, bins=30)
```

- 都市全体の坂の分布を視覚化
- 自転車政策や高齢者対応の都市設計などに応用できる

---

## ✅ まとめ

| 処理 | 使用関数 | 結果 |
|------|-----------|------|
| 標高取得 | `add_node_elevations_google` | 各ノードに `"elevation"` 属性が追加 |
| 勾配計算 | `add_edge_grades` | 各エッジに `"grade"` 属性が追加 |
| 可視化 | `plot_graph` + 勾配色 | 勾配分布を色で表示 |
| 分布分析 | `plt.hist` | 勾配ヒストグラムを作成 |

---

この分析は、坂道の多い地域のモビリティ政策、歩行・自転車アクセスの最適化、都市地形の特徴分析に有効です。APIキー不要なDEMソース（SRTMなど）を使うことも可能です。
"""
)

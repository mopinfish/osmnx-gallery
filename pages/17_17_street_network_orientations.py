import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="17 - Street Orientation Histogram", layout="wide")
st.title("🧭 Street Network Orientation Analysis")

st.markdown(
    "指定した場所の道路ネットワークに基づいて、方位角（北からの角度）を分析し、都市構造のグリッド性や方向性を可視化します。"
)

with st.form("orientation_form"):
    place = st.text_input("場所（例: 京都市左京区）", "京都市左京区")
    network_type = st.selectbox("ネットワークタイプ", ["drive", "walk", "bike", "all"])
    bins = st.slider("ビンの数（角度の分割数）", 4, 72, 36)
    submitted = st.form_submit_button("解析・表示")

if submitted:
    with st.spinner("ネットワークと道路方位の取得中..."):
        try:
            # ネットワーク取得
            G = ox.graph_from_place(place, network_type=network_type)

            # エッジに bearing（方位角）を追加
            G = ox.bearing.add_edge_bearings(G)
            # bearing属性を抽出
            bearings = [
                d["bearing"] for _, _, d in G.edges(data=True) if "bearing" in d
            ]

            # ヒストグラムの作成
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.hist(
                bearings, bins=bins, density=True, color="skyblue", edgecolor="black"
            )
            ax.set_title(f"Street Orientation Histogram: {place}")
            ax.set_xlabel("方位角 (degrees from North)")
            ax.set_ylabel("割合")
            ax.set_xticks(np.arange(0, 361, 45))
            st.pyplot(fig)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🧭 Street Orientation Analysis - Streamlitアプリ解説

このStreamlitアプリは、OSMnxを使って都市の道路ネットワークを取得し、  
各道路の**方位角（bearing）**を計算してヒストグラムで可視化することで、  
都市構造の**方向性やグリッドパターン**を直感的に把握するためのツールです。

---

## 🔹 入力パラメータ

- **場所**：対象となる都市または地名（例：「京都市左京区」）
- **ネットワークタイプ**：`drive`（車道）、`walk`（歩道）、`bike`（自転車道）、`all`（すべて）
- **ビンの数**：ヒストグラムの角度分割数（例：36ビンなら10度刻み）

---

## 🔹 処理の流れ

### 1. ネットワークの取得

```python
G = ox.graph_from_place(place, network_type=network_type)
```

- 指定された地名のOpenStreetMap道路ネットワークをOSMnxで取得します。
- 選択したネットワークタイプに応じて取得される道路が異なります。

---

### 2. 方位角（bearing）の付加

```python
G = ox.bearing.add_edge_bearings(G)
```

- 各道路エッジに `"bearing"` 属性（0～360°の角度）を計算して付加します。
- 方位角はエッジの始点から終点に向かって、北を0度として時計回りに測定されます。

---

### 3. 方位角の抽出とヒストグラム描画

```python
bearings = [d["bearing"] for _, _, d in G.edges(data=True) if "bearing" in d]
```

- `"bearing"` を持つすべてのエッジから角度リストを作成。

```python
ax.hist(bearings, bins=bins, density=True)
```

- ヒストグラムにより道路方向の分布を視覚化します。
- 明確なピークがある場合、**都市に特定の方向性（軸）**があることを意味します。
- 例：碁盤目状の都市（京都、ニューヨーク）では90°刻みでピークが出現します。

---

## ✅ 出力結果

- 方位角（0〜360°）を水平方向に表示したヒストグラム
- X軸：方位角（45度刻み）、Y軸：正規化頻度（割合）
- 都市の道路構造における**方向の偏り**が一目でわかる

---

## 📌 活用例

| 分析対象 | 利用目的 |
|----------|----------|
| グリッド型 vs 放射型都市 | 都市構造の類型分類 |
| 都市間比較 | 方向分布の共通性・差異を比較分析 |
| ネットワーク計画 | 移動効率、歩行者経路設計、方向バイアスの把握 |

---

このアプリは、都市の隠れた空間的構造や歴史的成り立ちを探るヒントを与えてくれます。  
さらに、円形の極座標グラフ（rose diagram）や方向性のクラスタリングにも拡張可能です。
"""
)

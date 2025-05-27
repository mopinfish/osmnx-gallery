# 📄 ファイル名: pages/10-building-footprints.py

import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="10 - Building Footprints", layout="wide")
st.title("🏢 Building Footprints from OpenStreetMap")

st.markdown("### 📍 場所を指定して、建物ポリゴンを取得・可視化・面積分析")

with st.form("building_form"):
    place = st.text_input("場所（例: 東京都千代田区）", "東京都千代田区")
    show_area = st.checkbox("建物の面積を計算・色分け表示", value=True)
    submitted = st.form_submit_button("実行")

if submitted:
    with st.spinner("建物データを取得中..."):
        try:
            # 建物ポリゴンの取得
            tags = {"building": True}
            gdf = ox.features_from_place(place, tags=tags)

            if gdf.empty:
                st.warning(
                    "建物データが取得できませんでした。対象地域を変更して再試行してください。"
                )
            else:
                # 投影（面積計算のため）
                gdf_proj = gdf.to_crs(ox.settings.default_crs)

                # 面積の計算
                if show_area:
                    gdf_proj["area_m2"] = gdf_proj.geometry.area

                # 描画
                fig, ax = plt.subplots(figsize=(8, 8))
                if show_area:
                    gdf_proj.plot(
                        ax=ax,
                        column="area_m2",
                        cmap="OrRd",
                        legend=True,
                        legend_kwds={"label": "建物面積 (m²)"},
                    )
                else:
                    gdf.plot(ax=ax, facecolor="black", edgecolor="none")

                ax.set_title(f"{place} - 建物フットプリント", fontsize=12)
                ax.set_axis_off()
                plt.tight_layout()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 🏢 Building Footprints with OSMnx の解説

このノートブックでは、OSMnxを用いてOpenStreetMapから建物のフットプリント（外周形状）を取得し、都市の建物分布や形状を可視化・分析する方法を紹介します。

---

## 📍 1. 建物データの取得

```python
import osmnx as ox

gdf = ox.features_from_place("Piedmont, California, USA", tags={"building": True})
```

- `features_from_place()` を使うことで、建物に関するジオメトリ（ポリゴン）を取得
- `"building": True` により、あらゆる建物タイプを一括で抽出

---

## 🧭 2. 投影（地図座標系への変換）

```python
gdf_proj = gdf.to_crs(ox.settings.default_crs)
```

- 緯度経度（WGS84）から平面座標系へ変換（面積や距離の計算が可能に）
- `default_crs` や `UTM` 系を使って自動的に適切な投影を選ぶことも可能

---

## 📐 3. 建物統計量の計算（面積など）

```python
gdf_proj["area_m2"] = gdf_proj["geometry"].area
```

- 投影されたジオメトリをもとに、各建物の面積を平方メートル単位で計算
- この列を使って、ヒストグラムやランキングを作成可能

---

## 📊 4. 可視化：建物フットプリントをマップに表示

```python
ox.plot_footprints(gdf, figsize=(8, 8))
```

- 建物ポリゴンを地図上に塗りつぶして描画
- 都市の密度や形態を視覚的に把握可能

---

## 🎨 5. 面積別の色分けや分析（応用）

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))
gdf_proj.plot(ax=ax, column="area_m2", cmap="OrRd", legend=True)
```

- 建物の面積に応じてカラースケーリング（例：大きい建物ほど濃く）
- ヒートマップ風に都市の建物規模分布を把握できる

---

## ✅ まとめ

| 処理 | 使用関数・属性 | 説明 |
|------|----------------|------|
| 建物取得 | `features_from_place` + `{"building": True}` | 建物ポリゴンを取得 |
| 投影 | `.to_crs()` | 面積計算のために平面座標へ変換 |
| 面積計算 | `.area` | 各建物の面積（m²）を取得 |
| 可視化 | `plot_footprints()` / `.plot()` | 建物分布を描画・分析 |

---

この手法は、都市の建築密度分析、容積率評価、地図の視覚デザイン、環境評価など多くの応用分野で利用可能です。OSMデータを活用した都市モデリングの第一歩として有効です。
"""
)

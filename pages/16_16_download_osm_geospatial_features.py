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

st.set_page_config(page_title="16 - Download OSM Features", layout="wide")
st.title("📥 Download OSM Geospatial Features")

st.markdown(
    "指定した地名またはジオメトリ範囲から、OpenStreetMapの地理空間フィーチャ（建物、公園、水路など）を取得して可視化します。"
)

with st.form("feature_form"):
    place = st.text_input("地名または住所（例: 京都市左京区）", "京都市左京区")
    tag_key = st.selectbox(
        "OSMタグキー",
        ["building", "landuse", "highway", "leisure", "natural", "waterway", "amenity"],
    )
    tag_value = st.text_input("タグ値（例: residential, park など。空欄で全て）", "")
    submitted = st.form_submit_button("データを取得・表示")

if submitted:
    with st.spinner("データを取得中..."):
        try:
            # タグ指定の準備
            tags = {tag_key: True} if tag_value == "" else {tag_key: tag_value}

            # データ取得
            gdf = ox.features_from_place(place, tags=tags)

            if gdf.empty:
                st.warning("指定された条件に一致するデータが見つかりませんでした。")
            else:
                # 投影
                gdf_proj = gdf.to_crs(ox.settings.default_crs)

                # 可視化
                fig, ax = plt.subplots(figsize=(8, 8))
                gdf_proj.plot(ax=ax, facecolor="cornflowerblue", edgecolor="black")
                ax.set_title(
                    f"OSMフィーチャ: {tag_key} = {tag_value or 'ANY'}", fontsize=12
                )
                ax.set_axis_off()
                st.pyplot(fig)

                # 属性データ表示
                st.subheader("📋 属性テーブル（先頭10行）")
                st.dataframe(gdf_proj.drop(columns="geometry").head(10))

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown(
    """
---
# 📥 OSM Geospatial Features Downloader - Streamlitアプリ解説

このアプリは、OpenStreetMap（OSM）から建物、公園、水路などの地理空間データ（フィーチャ）を取得し、可視化・属性確認できるインタラクティブツールです。

---

## 🔹 主な機能

- **地名入力**：市区町村や地域名をもとに検索範囲を自動設定
- **タグキー選択**：OSMの主要なタグカテゴリを選択（例：`building`, `landuse`, `waterway`）
- **タグ値指定**：特定の値に絞り込むことも可能（例：`residential`, `park`）

---

## 🔹 処理の流れ

### 1. 地理空間データの取得

```python
gdf = ox.features_from_place(place, tags={tag_key: tag_value})
```

- `place` に一致するポリゴン（市区町村範囲など）内でタグに合致するフィーチャを抽出
- `tag_value` が空の場合はそのキー全体を対象にする（例：すべての建物）

---

### 2. 投影変換（CRS）

```python
gdf_proj = gdf.to_crs(ox.settings.default_crs)
```

- 座標系を平面直交座標系に変換して、正確な面積や距離の計算に対応

---

### 3. 地図描画

```python
gdf_proj.plot(ax=ax, facecolor="cornflowerblue", edgecolor="black")
```

- 建物・公園・土地利用などを塗りつぶして視覚的に表示
- 地図軸はオフにしてビジュアル重視

---

### 4. 属性の表示（DataFrame）

```python
st.dataframe(gdf_proj.drop(columns="geometry").head(10))
```

- 空間情報を除いた先頭10件の属性情報を表形式で表示
- 施設名、カテゴリ、用途などのタグ情報が閲覧可能

---

## ✅ 活用例

| タグキー | 用途例 |
|----------|--------|
| `building` | 建物密度分析、防災分析 |
| `landuse` | 土地利用マップの作成（住宅地・商業地など） |
| `leisure` | 公園や運動場の分布確認 |
| `waterway` | 河川や運河のネットワーク構築 |
| `amenity` | 駅、病院、学校などの抽出 |

---

このアプリを使えば、任意の地域の空間フィーチャをすぐに抽出・可視化・分析に利用できます。都市設計・環境評価・施設配置などに応用可能です。
"""
)

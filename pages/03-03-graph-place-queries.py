import streamlit as st
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🗺️ OSMnx Place Queries Demo")

st.markdown("""
このページでは、OSMnx を使って単一または複数の都市・地域・国の地理的境界ポリゴンを取得し、可視化します。
`geocode_to_gdf` 関数による地名からのポリゴン取得や、複数地名をまとめて取得する機能のデモを含みます。
""")

st.markdown("""
---
## 📘 実行している処理の解説

### 地名を空間ポリゴンに変換
```python
gdf = ox.geocoder.geocode_to_gdf("Manhattan, New York, USA")
```

### 複数の場所もまとめて取得可能
```python
places = ["United Kingdom", "Ireland"]
gdf = ox.geocoder.geocode_to_gdf(places)
```

取得した GeoDataFrame は `.plot()` による描画や、属性確認に活用できます。
---
""")

# フォーム
with st.form("place_query_form"):
    st.write("以下に地名を入力してください。1行に1件、複数指定も可能です。")
    place_input = st.text_area(
        "場所の一覧", "Manhattan, New York, USA\nBrooklyn, New York, USA")
    submitted = st.form_submit_button("場所の境界を取得")

if submitted:
    try:
        place_list = [line.strip()
                      for line in place_input.splitlines() if line.strip()]
        gdf = ox.geocoder.geocode_to_gdf(place_list)
        gdf_proj = gdf.to_crs(epsg=3857)

        st.success(f"{len(gdf)} 件の場所を取得しました。")
        st.dataframe(gdf[["display_name", "geometry"]])

        # 可視化
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf_proj.plot(ax=ax, alpha=0.6, edgecolor="k")
        ax.set_title("取得した地理的境界")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

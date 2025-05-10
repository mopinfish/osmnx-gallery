import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

st.set_page_config(page_title="Figure-Ground Diagram", layout="wide")

st.title("Figure-Ground Diagram Example")

st.markdown("""
### 📌 概要

このページでは、**フィギュア・グラウンド図（Figure-Ground Diagram）** を作成します。都市における建物と空間の対比を視覚的に表現することで、密度や都市構造の理解に役立ちます。

---

### 🛠 使用する主な関数の解説

- `ox.geocode_to_gdf(place)`：都市のポリゴンを取得します。
- `ox.features_from_place(place, tags)`：建物（building）など特定のタグに該当する要素を取得します。
- `matplotlib` を使って、背景（空間）に対する建築物の構成を可視化します。

---

### ⚙️ 実行
""")

with st.form("fg_form"):
    place = st.text_input("都市名（例: Shibuya, Tokyo, Japan）",
                          value="Shibuya, Tokyo, Japan")
    submitted = st.form_submit_button("図を生成")

if submitted:
    with st.spinner("データを取得して描画中..."):
        gdf = ox.geocode_to_gdf(place)
        buildings = ox.features_from_place(place, tags={"building": True})

        st.success("図の描画が完了しました。")

        fig, ax = plt.subplots(figsize=(8, 8))
        gdf.plot(ax=ax, facecolor="white", edgecolor="none")
        buildings.plot(ax=ax, facecolor="black", edgecolor="none")
        ax.set_title("Figure-Ground Diagram")
        ax.axis("off")
        st.pyplot(fig)

import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="02 - Routing: Speed and Time", layout="wide")
st.title("🚗 Routing: Speed and Travel Time in OSMnx")

st.markdown("### 📍 場所と経路探索パラメータの指定")
with st.form("routing_form"):
    place_name = st.text_input(
        "場所の名前", placeholder="東京都千代田区丸の内", value="東京都千代田区丸の内")
    route_type = st.radio(
        "重みの種類（最短経路の基準）", ["距離（length）", "所要時間（travel_time）"])
    submitted = st.form_submit_button("ルートを計算・表示")

if submitted:
    with st.spinner("ネットワークとルートを取得中..."):
        try:
            # ✅ グラフの取得と最大連結成分の抽出（ox.graphで統一）
            G = ox.graph.graph_from_place(place_name, network_type="drive")

            # エッジ属性追加
            G = ox.add_edge_speeds(G)
            G = ox.add_edge_travel_times(G)

            # ランダムな出発地・目的地
            nodes = list(G.nodes())
            orig, dest = random.sample(nodes, 2)
            weight = "length" if route_type == "距離（length）" else "travel_time"

            # 経路計算と描画
            route = ox.routing.shortest_path(G, orig, dest, weight=weight)
            fig, ax = ox.plot.plot_graph_route(G, route, route_color="red", route_linewidth=4,
                                               bgcolor="white", show=False, close=False)
            st.pyplot(fig)

            # 属性の合計を計算
            route_edges = list(zip(route[:-1], route[1:]))
            length = 0
            travel_time = 0
            for u, v in route_edges:
                data = G.get_edge_data(u, v)
                attr = data[0] if 0 in data else list(data.values())[0]
                length += attr.get("length", 0)
                travel_time += attr.get("travel_time", 0)

            st.subheader("📊 経路の統計情報")
            st.markdown(f"- 📏 **距離**: `{length:.1f} m`")
            st.markdown(f"- ⏱ **所要時間**: `{travel_time / 60:.1f} 分`")

        except Exception as e:
            st.error(f"ルートの計算に失敗しました: {e}")

# --------------------
# 解説マークダウン
# --------------------
st.markdown("""
---

# 🚗 Routing: Speed and Travel Time in OSMnx の解説

このノートブックでは、OSMnx を使って道路ネットワーク上でのルート探索を行い、各ルートにおける **距離**・**速度**・**所要時間** を計算する方法を紹介します。

---

## 📍 1. 道路ネットワークの取得

```python
import osmnx as ox

place = "Piedmont, California, USA"
G = ox.graph_from_place(place, network_type="drive")
```

- 指定した場所の「drive」ネットワーク（自動車用）を取得します。

---

## ⛽ 2. 各エッジに速度と所要時間を付加

```python
G = ox.add_edge_speeds(G)         # デフォルトまたは OSM データから速度を追加
G = ox.add_edge_travel_times(G)   # 距離と速度から所要時間を算出
```

- `add_edge_speeds`: 各エッジに `speed_kph` 属性を付加
- `add_edge_travel_times`: 距離と速度から `travel_time` 属性を計算（単位: 秒）

---

## 📌 3. 最短経路の計算（距離ベース）

```python
import networkx as nx

orig, dest = list(G.nodes)[0], list(G.nodes)[-1]
route = nx.shortest_path(G, orig, dest, weight="length")
```

- `weight="length"`: 距離が最小となる経路を探索

---

## ⏱️ 4. 最短経路の計算（時間ベース）

```python
route_tt = nx.shortest_path(G, orig, dest, weight="travel_time")
```

- `weight="travel_time"`: 所要時間が最小となる経路を探索

---

## 🎨 5. 経路の可視化

```python
ox.plot_graph_route(G, route, route_color="r", route_linewidth=4)
ox.plot_graph_route(G, route_tt, route_color="g", route_linewidth=4)
```

- `plot_graph_route`: 経路をネットワーク上に描画
- 経路ごとに色や太さを指定可能

---

## 📊 6. 距離・所要時間の取得

```python
import numpy as np

length = sum(ox.utils_graph.get_route_edge_attributes(G, route, "length"))
travel_time = sum(ox.utils_graph.get_route_edge_attributes(G, route, "travel_time"))
```

- `get_route_edge_attributes`: 経路上の属性値を抽出（リストまたは合計）

---

## ✅ まとめ

| 項目           | 処理内容                                     |
|----------------|----------------------------------------------|
| ネットワーク取得 | `graph_from_place`                          |
| 速度付加       | `add_edge_speeds`                            |
| 時間付加       | `add_edge_travel_times`                      |
| 距離最短経路   | `nx.shortest_path(..., weight="length")`     |
| 時間最短経路   | `nx.shortest_path(..., weight="travel_time")`|
| 属性合計       | `get_route_edge_attributes(..., attr)`       |
| 描画           | `plot_graph_route`                           |

---

OSMnx を使うことで、速度と時間の情報を含んだネットワーク解析を簡単に行うことができます。ルート探索の目的に応じて「距離」か「時間」を選択し、交通戦略や都市分析に応用可能です。

""")

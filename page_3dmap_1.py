import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("🏙️ 台北市商圈 3D 熱度地圖")

# --- 1. 生成台北市商圈範圍內的隨機資料 ---
# 模擬「人潮位置」，主要分布在幾個商圈中心附近
np.random.seed(42)

# 商圈中心點（經緯度）
centers = {
    "西門町": [25.0422, 121.5085],
    "信義區": [25.0340, 121.5645],
    "東區": [25.0419, 121.5440],
    "士林夜市": [25.0880, 121.5250],
    "公館": [25.0142, 121.5340],
    "永康街": [25.0330, 121.5290],
}

# 依據各商圈中心生成隨機人流點
data_list = []
for name, (lat, lon) in centers.items():
    for _ in range(200):  # 每個商圈生成 200 筆資料
        data_list.append({
            "商圈": name,
            "lat": lat + np.random.randn() / 500,  # 在附近隨機散布
            "lon": lon + np.random.randn() / 500,
        })

data = pd.DataFrame(data_list)

st.subheader("📍 模擬商圈人流資料（前10筆）")
st.dataframe(data.head(10))

# --- 2. 建立 3D HexagonLayer ---
layer_hexagon = pdk.Layer(
    "HexagonLayer",
    data=data,
    get_position='[lon, lat]',
    radius=120,  # 六角格半徑（公尺）
    elevation_scale=50,  # 高度比例
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# --- 3. 設定攝影機視角 ---
view_state = pdk.ViewState(
    latitude=25.04,
    longitude=121.54,
    zoom=12,
    pitch=55,
)

# --- 4. 顯示 3D 地圖 ---
r_hexagon = pdk.Deck(
    layers=[layer_hexagon],
    initial_view_state=view_state,
    map_style="light",  # 可改成 "dark" 或 "satellite"
    tooltip={"text": "熱度：{elevationValue}"}
)

st.pydeck_chart(r_hexagon)

st.caption("資料為模擬生成，用於展示台北市主要商圈的3D人流熱度分布效果。")

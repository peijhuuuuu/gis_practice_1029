import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("🏙️ 台北市商業活動 3D 熱度地圖")

# --- 1. 模擬全台北市商業區人流資料 ---
np.random.seed(42)

# 商業聚集區中心點
centers = {
    "信義計畫區": [25.0340, 121.5645],
    "東區商圈": [25.0419, 121.5440],
    "西門町": [25.0422, 121.5085],
    "南西商圈": [25.0523, 121.5189],
    "公館商圈": [25.0142, 121.5340],
    "士林夜市": [25.0880, 121.5250],
    "內湖科技園區": [25.0806, 121.5754],
    "南港園區": [25.0528, 121.6060],
}

# 生成模擬人流資料
data_list = []
for name, (lat, lon) in centers.items():
    n_points = np.random.randint(300, 800)  # 每區生成點數
    for _ in range(n_points):
        data_list.append({
            "商業區": name,
            "lat": lat + np.random.randn() / 600,
            "lon": lon + np.random.randn() / 600,
        })

data = pd.DataFrame(data_list)

# --- 2. 設定 Pydeck 3D HexagonLayer ---
layer_hexagon = pdk.Layer(
    "HexagonLayer",
    data=data,
    get_position='[lon, lat]',
    radius=180,           # 每個六角格的半徑（公尺）
    elevation_scale=12,   # 高度比例（越大越高）
    elevation_range=[0, 500],
    pickable=True,
    extruded=True,
)

# --- 3. 攝影機視角 ---
view_state = pdk.ViewState(
    latitude=25.04,
    longitude=121.54,
    zoom=12,
    pitch=50,
)

# --- 4. 顯示地圖 ---
r = pdk.Deck(
    layers=[layer_hexagon],
    initial_view_state=view_state,
    map_style="light",  # 可改 "dark" / "satellite"
    tooltip={"text": "{商業區}\n熱度：{elevationValue}"}
)

st.pydeck_chart(r)

st.caption("資料為模擬生成，用於展示台北市商業活動的 3D 熱度分布效果。")

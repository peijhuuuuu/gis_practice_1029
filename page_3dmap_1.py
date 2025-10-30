import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("🏙️ 台北市主要商業區 3D 熱度地圖")

# --- 1. 模擬全台北市商業區人流資料 ---
np.random.seed(42)

centers = {
    "信義計畫區": [25.0340, 121.5645],
    "東區商圈": [25.0419, 121.5440],
    "西門町": [25.0422, 121.5085],
    "南西商圈": [25.0523, 121.5189],
    "中山商圈": [25.0525, 121.5255],
    "永康街商圈": [25.0330, 121.5290],
    "公館商圈": [25.0142, 121.5340],
    "士林夜市": [25.0880, 121.5250],
    "饒河街夜市": [25.0503, 121.5770],
    "松菸文創園區": [25.0447, 121.5572],
    "南港園區": [25.0528, 121.6060],
    "內湖科技園區": [25.0806, 121.5754],
    "天母商圈": [25.1204, 121.5337],
    "大直美麗華": [25.0825, 121.5553],
    "木柵景美": [24.9888, 121.5419],
}

# 生成模擬人流資料
data_list = []
for name, (lat, lon) in centers.items():
    n_points = np.random.randint(300, 800)  # 每區隨機生成點數
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
    radius=180,           # 六角格大小（公尺）
    elevation_scale=10,   # 高度比例
    elevation_range=[0, 500],
    pickable=True,
    extruded=True,
)

# --- 3. 攝影機視角 ---
view_state = pdk.ViewState(
    latitude=25.05,
    longitude=121.54,
    zoom=11.7,
    pitch=50,
)

# --- 4. 顯示 3D 地圖 ---
r = pdk.Deck(
    layers=[layer_hexagon],
    initial_view_state=view_state,
    map_style="light",  # 可改 "dark"、"satellite"
    tooltip={"text": "{商業區}\n熱度：{elevationValue}"}
)

st.pydeck_chart(r)

st.caption("資料為模擬生成，用於展示台北市主要商業聚集區的 3D 熱度分布。")


st.title("台北市商業熱度 3D 模擬地形圖（免金鑰版）")

# 模擬網格範圍（整個台北市）
x, y = np.meshgrid(np.linspace(-1, 1, 80), np.linspace(-1, 1, 80))

# 模擬幾個商圈中心（信義、西門、東區、士林、南港）
def gaussian_peak(x, y, cx, cy, h, s):
    return h * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * s**2))

z = (
    gaussian_peak(x, y, 0.4, -0.2, 1.2, 0.25) +  # 信義區
    gaussian_peak(x, y, -0.4, 0.1, 0.9, 0.25) +  # 士林
    gaussian_peak(x, y, 0.0, 0.5, 0.8, 0.3) +    # 東區
    gaussian_peak(x, y, -0.2, -0.3, 1.0, 0.2) +  # 西門町
    gaussian_peak(x, y, 0.6, 0.5, 0.7, 0.25)     # 南港
) * 1000  # 高度放大倍數

# 整理成 DataFrame
data_dem_list = []
base_lat, base_lon = 25.04, 121.55
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        data_dem_list.append({
            "lon": base_lon + x[i, j] * 0.1,
            "lat": base_lat + y[i, j] * 0.1,
            "elevation": z[i, j]
        })
df_dem = pd.DataFrame(data_dem_list)

# ===============================================
# 2. Pydeck GridLayer（立體方塊圖）
# ===============================================
layer_grid = pdk.Layer(
    'GridLayer',
    data=df_dem,
    get_position='[lon, lat]',
    get_elevation_weight='elevation',
    elevation_scale=1.5,      # 柱子高度加強
    cell_size=1200,           # 柱子更密集
    extruded=True,
    pickable=True
)

# ===============================================
# 3. 視角設定
# ===============================================
view_state = pdk.ViewState(
    latitude=base_lat,
    longitude=base_lon,
    zoom=11.5,
    pitch=55
)

# ===============================================
# 4. 組合與顯示
# ===============================================
r = pdk.Deck(
    layers=[layer_grid],
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
    tooltip={"text": "商業熱度: {elevationValue}"}
)

st.pydeck_chart(r)

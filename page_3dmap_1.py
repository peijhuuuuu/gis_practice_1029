import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
st.title("Pydeck 3D 地圖 (向量 - 密度圖)")

# --- 1. 生成範例資料 (向量) ---
data = pd.DataFrame({
    'lat': 25.0478 + np.random.randn(1000) / 50,
    'lon': 121.5170 + np.random.randn(1000) / 50,
})

# --- 2. 設定 Pydeck 圖層 (Layer) ---
layer_hexagon = pdk.Layer(
    'HexagonLayer',
    data=data,
    get_position='[lon, lat]',
    radius=100,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# --- 3. 設定攝影機視角 (View State) ---
view_state_hexagon = pdk.ViewState(
    latitude=25.0478,
    longitude=121.5170,
    zoom=12,
    pitch=50,
)

# --- 4. 組合圖層和視角並顯示 (不使用 Mapbox Key) ---
r_hexagon = pdk.Deck(
    layers=[layer_hexagon],
    initial_view_state=view_state_hexagon,
    map_style='light',  # <-- 使用免費內建樣式，不需金鑰
    tooltip={"text": "這個區域有 {elevationValue} 個熱點"}
)

st.pydeck_chart(r_hexagon)

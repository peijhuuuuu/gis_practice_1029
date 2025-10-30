import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("台北市商圈 3D 立體熱度圖（免金鑰版）")

# --- 1. 模擬台北市商業聚集區資料（更多點、更密集） ---
np.random.seed(42)
data = pd.DataFrame({
    "lat": 25.03 + np.random.randn(3500) / 200,  # 原本 2000 → 現在 3500
    "lon": 121.53 + np.random.randn(3500) / 200,
})

# --- 2. 建立 HexagonLayer ---
layer = pdk.Layer(
    "HexagonLayer",
    data=data,
    get_position='[lon, lat]',
    radius=80,
    elevation_scale=5,  # 原本 3 → 現在 5，讓柱子更高
    elevation_range=[0, 800],
    pickable=True,
    extruded=True,
)

# --- 3. 設定攝影機視角 ---
view_state = pdk.ViewState(
    latitude=25.04,
    longitude=121.53,
    zoom=12.5,
    pitch=55,  # 稍微再仰一點，看起來更立體
)

# --- 4. 顯示地圖（使用 OpenStreetMap 底圖） ---
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
    tooltip={"text": "熱度值: {elevationValue}"}
)

st.pydeck_chart(r)


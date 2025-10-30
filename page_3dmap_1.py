import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("🏙️ 台北市城市商圈熱度地圖")

# --- 1. 建立台北主要商圈資料 ---
data = pd.DataFrame([
    ["西門町商圈", 25.0422, 121.5085],
    ["東區商圈", 25.0419, 121.5440],
    ["信義商圈", 25.0340, 121.5645],
    ["士林夜市", 25.0880, 121.5250],
    ["饒河街夜市", 25.0503, 121.5770],
    ["南西商圈", 25.0523, 121.5189],
    ["公館商圈", 25.0142, 121.5340],
    ["永康街商圈", 25.0330, 121.5290],
    ["南港車站商圈", 25.0528, 121.6060],
    ["內湖科技園區", 25.0806, 121.5754],
], columns=["name", "lat", "lon"])

st.subheader("📍 商圈資料預覽")
st.dataframe(data)

# --- 2. 設定 Pydeck HexagonLayer ---
layer = pdk.Layer(
    "HexagonLayer",
    data=data,
    get_position='[lon, lat]',
    radius=300,  # 每個六角格的半徑（單位: 公尺）
    elevation_scale=30,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# --- 3. 設定地圖視角 ---
view_state = pdk.ViewState(
    latitude=25.04,
    longitude=121.54,
    zoom=12,
    pitch=45,
)

# --- 4. 顯示地圖 ---
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="light",  # 可改成 "dark", "satellite", "road"
    tooltip={"text": "{name}"}
)

st.pydeck_chart(r)

st.caption("資料來源：台北市主要商圈位置（示意用）")

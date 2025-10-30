import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


st.title("🔥美國火災地圖 (NASA FIRMS 資料)")
# --- 載入資料 ---
url = "https://drive.google.com/uc?id=1kEhZRm9cIpeO4xKvtl1EHc8cpm86K1To"
df = pd.read_csv(url)

# --- 畫地圖 ---
fig = px.scatter_geo(
    df,
    lat="latitude",
    lon="longitude",
    color="brightness",
    hover_name="acq_date",
    projection="orthographic",
    title="全球火災偵測 (最近 24 小時)"
)

st.plotly_chart(fig, use_container_width=True)

# use_container_width=True:當設定為 True 時，Streamlit 會忽略 Plotly 圖表物件本身可能設定的寬度，
# 並強制讓圖表的寬度自動延展，以填滿其所在的 Streamlit 容器 (例如，主頁面的寬度、某個欄位 (column) 的寬度，
# 或是一個展開器 (expander) 的寬度)。
import numpy as np

st.title("🌆 全球城市人口 3D 高度圖 (Surface)")

# --- 1. 讀取城市資料 ---
url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75/worldcities.csv"
df = pd.read_csv(url)
df = df[df['population'] > 1000000]  # 只取人口超過 100 萬

# --- 2. 建立網格 (經緯度格子) ---
lon_bins = np.linspace(-180, 180, 100)  # 經度格子數
lat_bins = np.linspace(-90, 90, 50)     # 緯度格子數

# 每個格子的人口總和
grid_population = np.zeros((len(lat_bins), len(lon_bins)))

# 把每個城市加到對應格子
for _, row in df.iterrows():
    lon_idx = np.searchsorted(lon_bins, row['lng']) - 1
    lat_idx = np.searchsorted(lat_bins, row['lat']) - 1
    if 0 <= lon_idx < len(lon_bins) and 0 <= lat_idx < len(lat_bins):
        grid_population[lat_idx, lon_idx] += row['population']

# --- 3. 建立 3D Surface ---
fig = go.Figure(data=[go.Surface(
    z=grid_population,
    x=lon_bins,
    y=lat_bins,
    colorscale="Viridis"
)])

fig.update_layout(
    title="全球人口超過 100 萬城市 3D Surface",
    scene=dict(
        xaxis_title='經度',
        yaxis_title='緯度',
        zaxis_title='人口'
    ),
    width=900,
    height=700
)

# --- 4. 顯示 ---
st.plotly_chart(fig, use_container_width=True)

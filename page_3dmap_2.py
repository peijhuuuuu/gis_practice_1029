import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


st.title("🔥全球火災地圖 (NASA FIRMS 資料)")
# --- 載入資料 ---
url = "https://drive.google.com/uc?export=download&id=1nZ6Y19CWta8TU8KNae_KhMudVnkygLZT"
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
import requests
import io
import pandas as pd
# --- 1. 設定標題 ---
import numpy as np
st.title("Plotly 3D 地圖 (聖海倫火山DEM)")
# --- 2. 使用 requests 下載 CSV，再用 pandas 讀取 ---
url = "https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv"
response = requests.get(url)
response.raise_for_status()  # 如果下載失敗會直接報錯
z_data = pd.read_csv(io.StringIO(response.text), header=None)  # 直接讀成 2D 陣列

# --- 3. 建立 3D Surface 圖 ---
fig = go.Figure(
    data=[
        go.Surface(
            z=z_data.values,
            colorscale="Viridis"
        )
    ]
)

# --- 4. 調整 3D 視角和外觀 ---
fig.update_layout(
    title="Everest 山區 3D 地形圖 (可旋轉)",
    width=800,
    height=700,
    scene=dict(
        xaxis_title='X (格網索引)',
        yaxis_title='Y (格網索引)',
        zaxis_title='海拔 (Z)'
    )
)

# --- 5. 在 Streamlit 中顯示 ---
st.plotly_chart(fig)

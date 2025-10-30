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

st.title("Plotly 3D 地圖 - 阿爾卑斯山 DEM")
z_data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_alps_elevation.csv")

# --- 2. 建立 3D Surface 圖 ---
fig = go.Figure(
    data=[
        go.Surface(
            z=z_data.values,
            colorscale="Viridis"
        )
    ]
)

# --- 3. 調整 3D 視角和外觀 ---
fig.update_layout(
    title="阿爾卑斯山 3D 地形圖",
    width=800,
    height=700,
    scene=dict(
        xaxis_title='經度 (X)',
        yaxis_title='緯度 (Y)',
        zaxis_title='海拔 (Z)'
    )
)

# --- 4. 在 Streamlit 顯示 ---
st.plotly_chart(fig)

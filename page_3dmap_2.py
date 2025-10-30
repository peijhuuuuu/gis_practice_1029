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
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Plotly 3D 地圖 (網格 - DEM 表面)")

# --- 1. 讀取範例 DEM 資料 (Mount Eden / Maunga Whau) ---
# 這是一個 2D 陣列，每個格子的值就是海拔 (公尺)
z_data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_eden_elevation.csv")

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
    title="Mount Eden 3D 地形圖 (可旋轉)",
    width=800,
    height=700,
    scene=dict(
        xaxis_title='經度 (X)',
        yaxis_title='緯度 (Y)',
        zaxis_title='海拔 (Z)'
    )
)

# --- 4. 在 Streamlit 中顯示 ---
st.plotly_chart(fig)

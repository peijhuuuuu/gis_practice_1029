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

st.title("🌊 全球海洋表面溫度 3D 曲面圖")

# --- 2. 載入海溫資料 (NOAA 公開資料範例) ---
# 這是一份模擬全球海溫格點資料
# （實際來源：https://raw.githubusercontent.com/plotly/datasets/master/ocean_surface.csv）
url = "https://raw.githubusercontent.com/plotly/datasets/master/ocean_surface.csv"
df = pd.read_csv(url)

# 這個資料中：
# X = 經度, Y = 緯度, Z = 海表溫度 (°C)
x = np.linspace(-180, 180, df.shape[1])
y = np.linspace(-90, 90, df.shape[0])
z = df.values

# --- 3. 建立 3D 曲面圖 ---
fig = go.Figure(
    data=[
        go.Surface(
            x=x,
            y=y,
            z=z,
            colorscale="RdBu_r",  # 紅藍反轉色階：紅=高溫, 藍=低溫
            colorbar_title="海溫 (°C)",
        )
    ]
)

# --- 4. 外觀設定 ---
fig.update_layout(
    title="🌍 全球海洋表面溫度分布 (3D)",
    scene=dict(
        xaxis_title="經度 (Longitude)",
        yaxis_title="緯度 (Latitude)",
        zaxis_title="溫度 (°C)",
        aspectratio=dict(x=2, y=1, z=0.4)
    ),
    width=900,
    height=700,
)

# --- 5. 顯示 ---
st.plotly_chart(fig)
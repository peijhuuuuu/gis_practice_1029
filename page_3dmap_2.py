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

st.title("🌆 全球城市人口 3D 高度圖")

# --- 1. 載入資料 ---
# 使用 GeoNames 公開城市資料 (你也可以換成自己的 CSV)
# CSV 格式需包含: city, country, lat, lon, population
url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75/worldcities.csv"
df = pd.read_csv(url)

# 只選取人口超過 1,000,000 的城市，避免圖太密
df = df[df['population'] > 1000000]

# --- 2. 建立 3D 散點圖 ---
fig = go.Figure(data=[go.Bar3d(
    x=df['lng'],               # 經度
    y=df['lat'],               # 緯度
    z=[0]*len(df),             # 柱子底部從 0 開始
    dx=0.5,                    # X 軸柱子寬度
    dy=0.5,                    # Y 軸柱子寬度
    dz=df['population'],       # 高度對應人口
    text=df['city'] + ", " + df['country'],  # 滑鼠提示
    hoverinfo='text+z',
    opacity=0.8
)])

# --- 3. 調整 3D 視角 ---
fig.update_layout(
    scene=dict(
        xaxis_title='經度',
        yaxis_title='緯度',
        zaxis_title='人口 (百萬)',
    ),
    title="全球人口超過 100 萬的城市 3D 分布",
    width=900,
    height=700
)

# --- 4. 顯示在 Streamlit ---
st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
st.title("台灣地震高風險區域 (自動抓資料)")

# 1. 抓取即時地震資料（歷史／高風險區視需要）  
#   這裡以政府開放資料「地震目錄」為例 :contentReference[oaicite:3]{index=3}
url = "https://data.gov.tw/api/v1/rest/dataset/97095?format=json"  # 注意：根據實際 API 端點可能需改
resp = requests.get(url)
if resp.status_code != 200:
    st.error("無法取得地震資料")
    st.stop()

data_json = resp.json()
# 假設 JSON 中有「資料」欄位且包含經緯度（緯度 lat, 經度 lon）與震級 magnitude
df = pd.json_normalize(data_json['resources'])  # 根據實際欄位結構調整
# 我們只取經緯、震級作為「風險指標」
df = df[['EpicenterLatitude', 'EpicenterLongitude', 'LocalMagnitude']]
df.columns = ['lat', 'lon', 'magnitude']

# 2. 可以新增一個「風險等級」欄位，例如震級 >= 5 為高風險，4‑5 中，低於4 低風險
def risk_level(mag):
    if mag >= 5:
        return 3
    elif mag >= 4:
        return 2
    else:
        return 1

df['risk'] = df['magnitude'].apply(risk_level)

# 3. 使用 Pydeck 的 HexagonLayer 來呈現密度／風險熱區
layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position='[lon, lat]',
    radius=1000,             # hexagon 半徑可調
    elevation_scale=50,       # 3D 高度比例
    elevation_range=[0, 5000],
    extruded=True,
    pickable=True,
    auto_highlight=True,
    # 根據 risk 等級給予顏色漸層：低藍→中黃→高紅
    color_range=[
        [0, 0, 255],    # 藍
        [255, 255, 0],  # 黃
        [255, 0, 0]     # 紅
    ],
    # 依據欄位「risk」來分類色彩／高度
    get_elevation='risk',
    get_fill_color='[risk * 85, (3-risk) * 85, 0]'
)

view_state = pdk.ViewState(
    latitude=23.5,
    longitude=121,
    zoom=6,
    pitch=50
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='dark',  # 你也可以改成 'light' 或其他
    tooltip={"text": "這個六角格內最高風險等級：{elevationValue}"}
)

st.pydeck_chart(r)


# --- 2. 設定 Pydeck 圖層 (GridLayer) ---
layer_grid = pdk.Layer( # 稍微改個名字避免混淆
    'GridLayer',
    data=df_dem,
    get_position='[lon, lat]',
    get_elevation_weight='elevation', # 使用 'elevation' 欄位當作高度
    elevation_scale=1,
    cell_size=2000,
    extruded=True,
    pickable=True # 加上 pickable 才能顯示 tooltip
)

# --- 3. 設定視角 (View) ---
view_state_grid = pdk.ViewState( # 稍微改個名字避免混淆
    latitude=base_lat, longitude=base_lon, zoom=10, pitch=50
)

# --- 4. 組合並顯示 (第二個地圖) ---
r_grid = pdk.Deck( # 稍微改個名字避免混淆
    layers=[layer_grid],
    initial_view_state=view_state_grid,
    # mapbox_key=MAPBOX_KEY, # <--【修正點】移除這裡的 mapbox_key
    tooltip={"text": "海拔高度: {elevationValue} 公尺"} # GridLayer 用 elevationValue
)
st.pydeck_chart(r_grid)
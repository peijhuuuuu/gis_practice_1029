import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


st.title("Plotly 3D 地圖 (台灣各鄉鎮 3D 地球儀互動地圖)")
# 上傳 CSV
uploaded_file = st.file_uploader("請上傳人口密度 CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 經緯度字典
    city_coords = {
        "臺北市": {"lat": 25.0330, "lon": 121.5654},
        "新北市": {"lat": 25.016, "lon": 121.462},
        "桃園市": {"lat": 24.993, "lon": 121.296},
        "臺中市": {"lat": 24.1477, "lon": 120.6736},
        "臺南市": {"lat": 22.9999, "lon": 120.2270},
        "高雄市": {"lat": 22.6273, "lon": 120.3014},
        "基隆市": {"lat": 25.128, "lon": 121.739},
        "新竹市": {"lat": 24.805, "lon": 120.971},
        "新竹縣": {"lat": 24.833, "lon": 121.089},
        "苗栗縣": {"lat": 24.567, "lon": 120.819},
        "彰化縣": {"lat": 24.080, "lon": 120.541},
        "南投縣": {"lat": 23.909, "lon": 120.685},
        "雲林縣": {"lat": 23.709, "lon": 120.431},
        "嘉義市": {"lat": 23.480, "lon": 120.449},
        "嘉義縣": {"lat": 23.458, "lon": 120.573},
        "屏東縣": {"lat": 22.550, "lon": 120.548},
        "宜蘭縣": {"lat": 24.702, "lon": 121.737},
        "花蓮縣": {"lat": 23.987, "lon": 121.601},
        "臺東縣": {"lat": 22.758, "lon": 121.144},
        "澎湖縣": {"lat": 23.565, "lon": 119.623},
        "金門縣": {"lat": 24.436, "lon": 118.318},
        "連江縣": {"lat": 26.160, "lon": 119.934}
    }

    # 將經緯度加入 DataFrame
    df["lat"] = df["區域別"].map(lambda x: city_coords[x]["lat"])
    df["lon"] = df["區域別"].map(lambda x: city_coords[x]["lon"])

    # 畫地圖
    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size="人口密度",
        color="人口密度",
        hover_name="區域別",
        projection="natural earth",
        scope="asia"
    )

    st.plotly_chart(fig, use_container_width=True)

# use_container_width=True:當設定為 True 時，Streamlit 會忽略 Plotly 圖表物件本身可能設定的寬度，
# 並強制讓圖表的寬度自動延展，以填滿其所在的 Streamlit 容器 (例如，主頁面的寬度、某個欄位 (column) 的寬度，
# 或是一個展開器 (expander) 的寬度)。

st.title("Plotly 3D 地圖 (網格 - DEM 表面)")

# --- 1. 讀取範例 DEM 資料 ---
# Plotly 內建的 "volcano" (火山) DEM 數據 (儲存為 CSV)
# 這是一個 2D 陣列 (Grid)，每個格子的值就是海拔
z_data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv")

# --- 2. 建立 3D Surface 圖 ---
# 建立一個 Plotly 的 Figure 物件，它是所有圖表元素的容器
fig = go.Figure(
    # data 參數接收一個包含所有 "trace" (圖形軌跡) 的列表。
    # 每個 trace 定義了一組數據以及如何繪製它。
    data=[
        # 建立一個 Surface (曲面) trace
        go.Surface(
            # *** 關鍵參數：z ***
            # z 參數需要一個 2D 陣列 (或列表的列表)，代表在 X-Y 平面上每個點的高度值。
            # z_data.values 會提取 pandas DataFrame 底層的 NumPy 2D 陣列。
            # Plotly 會根據這個 2D 陣列的結構來繪製 3D 曲面。
            z=z_data.values,

            # colorscale 參數指定用於根據 z 值 (高度) 對曲面進行著色的顏色映射方案。
            # "Viridis" 是 Plotly 提供的一個常用且視覺效果良好的顏色漸層。
            # 高度值較低和較高的點會有不同的顏色。
            colorscale="Viridis"
        )
    ] # data 列表結束
)

# --- 3. 調整 3D 視角和外觀 ---
# 使用 update_layout 方法來修改圖表的整體佈局和外觀設定
fig.update_layout(
    # 設定圖表的標題文字
    title="Mt. Bruno 火山 3D 地形圖 (可旋轉)",

    # 設定圖表的寬度和高度 (單位：像素)
    width=800,
    height=700,

    # scene 參數是一個字典，用於配置 3D 圖表的場景 (座標軸、攝影機視角等)
    scene=dict(
        # 設定 X, Y, Z 座標軸的標籤文字
        xaxis_title='經度 (X)',
        yaxis_title='緯度 (Y)',
        zaxis_title='海拔 (Z)'
        # 可以在 scene 字典中加入更多參數來控制攝影機初始位置、座標軸範圍等
    )
)

# 這段程式碼執行後，變數 `fig` 將包含一個設定好的 3D Surface Plotly 圖表物件。
# 你可以接著使用 fig.show() 或 st.plotly_chart(fig) 將其顯示出來。
# 這個圖表通常是互動式的，允許使用者用滑鼠旋轉、縮放和平移 3D 視角。

# --- 4. 在 Streamlit 中顯示 ---
st.plotly_chart(fig)
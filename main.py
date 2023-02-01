import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
import folium


# --- Page Setting ---
st.set_page_config(
    page_title="英会話講師の出身地",
    page_icon="🌍",
    layout="wide"
)

st.title("Native Campでレッスンを受けた講師達の出身地")
st.write("2023年は毎朝オンライン英会話！")
st.write("講師の出身地が見られるんですが、場所がわからなかったので図示してみました。")

gdf = gpd.read_file('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') 

c_df = pd.read_csv("countries.csv", header=0, names=["country", "code"])
c_df["from"] = "1"
c_df = c_df.groupby("code").max().reset_index().sort_values("from", ascending=False)

gdf_c = gdf.merge(c_df, left_on="id", right_on="code", how="left")
gdf_c = gdf_c.fillna(0)
gdf1 = gpd.GeoDataFrame(gdf_c)

centroid=gdf1.geometry.centroid
m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=1.5, tiles='OpenStreetMap')

folium.GeoJson(gdf1[['geometry', 'name', 'from']], 
               name = "Where My teachers are from",
               style_function = lambda x: {"weight":1, 'color':'grey','fillColor':'#bcbcbc' if x['properties']['from'] == 0 else '#C81D25', 'fillOpacity':0.8, 'colorOpacity': 0.1},
               highlight_function=lambda x: {'weight':3, 'color':'grey', 'fillOpacity':1},
               smooth_factor=2.0,
               tooltip=folium.features.GeoJsonTooltip(fields=['name'],
                                              aliases=['Country:'], 
                                              labels=True, 
                                              sticky=True,
                                             )
).add_to(m)

# st_data = st_folium(m, width=1200, height=500)

components.html(folium.Figure().add_child(m).render(), height=500)
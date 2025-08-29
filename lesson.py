import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
st.title("McDonalds Map")
zip_path = "data/archive(1).zip" 
csv_filename = "McDonalds.csv" 

with zipfile.ZipFile(zip_path) as z:
    with z.open(csv_filename) as f:
        df = pd.read_csv(f)

print(df.head())

#Try to make a map with locations of McDonalds in San Diego. 
# The McDonalds Data is already loaded
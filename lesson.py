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

# --- Step 1: Load McDonalds data ---

#--- Step 2: Convert to GeoDataFrame ---

#--- Step 3: Get coordinates for zip code 92130(or wherever you want it to be) ---

# --- Step 4: Project to meters for distance calculations ---

# --- Step 5: Filter McDonalds within 10 miles of zip code ---

# --- Step 6: Create a Folium map centered on the zip code ---

# --- Step 7: Add McDonalds locations to the map with MarkerCluster ---

# --- Step 8: Display the map in Streamlit ---

#Do not edit below this line
#change m to whatever your map variable is called
st_folium = st.components.v1.html(m._repr_html_(), height=600)
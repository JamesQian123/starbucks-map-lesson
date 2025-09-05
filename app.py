import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
st.title("Starbucks Map in Del Mar")


# --- Step 1: Load Starbucks data ---
#df stands for dataframe
all_starbucks_df = pd.read_csv(
    "http://s3.amazonaws.com/radius.civicknowledge.com/chrismeller.github.com-starbucks-2.1.1/data/all_starbucks.csv"
)
us_starbucks_df = pd.read_csv(
    "http://s3.amazonaws.com/radius.civicknowledge.com/chrismeller.github.com-starbucks-2.1.1/data/us_starbucks.csv"
)

st.write("Loaded", len(us_starbucks_df), "US Starbucks locations.")

# --- Step 2: Convert to GeoDataFrame ---

us_starbucks_gdf = gpd.GeoDataFrame(
    us_starbucks_df,
    geometry=gpd.points_from_xy(us_starbucks_df.lon, us_starbucks_df.lat),

    #A CRS defines how the coordinates in your data relate to real locations on Earth.
    #Without a CRS, your latitude/longitude numbers are just numbers—they don’t know where they are on the globe.
    #EPSG codes are standard IDs for CRSs.
    #EPSG:4326 specifically refers to the WGS 84 geographic coordinate system:
    crs="EPSG:4326"
)

# --- Step 3: Get coordinates for zip code 92130 ---

#Nominatim converts Addresses to Coordinates or Coordinates to adressess
#In this case it converts the 92130, USA zipcode to coordinates.

geolocator = Nominatim(user_agent="geo_app")
location = geolocator.geocode("92130, USA")
zip_point = Point(location.longitude, location.latitude)

# --- Step 4: Project to meters for distance calculations ---


us_starbucks_gdf = us_starbucks_gdf.to_crs(epsg=3857)

#geometry = [zip_point] gets the zipcode

zip_point_gdf = gpd.GeoDataFrame(geometry=[zip_point], crs="EPSG:4326").to_crs(epsg=3857)

#.iloc:
#like counting seats in a classroom: “I want the 2nd seat in the 1st row.”
#.loc:
#like asking for a student by name: “Give me Alice’s desk.”
#You want to use iloc when you’re selecting by position, and loc when you’re selecting by label.

zip_geom = zip_point_gdf.geometry.iloc[0]

# --- Step 5: Filter stores within 10 miles (16,093 meters) ---
radius = 16093  # 10 miles in meters
stores_in_radius = us_starbucks_gdf[us_starbucks_gdf.geometry.distance(zip_geom) <= radius]

st.write(f"Found {len(stores_in_radius)} Starbucks within 10 miles of 92130.")

# --- Step 6: Plot interactive map ---

#Folium is a library for making interactive Leaflet maps in Python 
#(e.g., zoomable maps with markers, shapes, layers)
#In the Folium library, folium.Map() is the constructor that creates a base map object. 
#Think of it as the “canvas” you’ll later add markers, polygons, and layers onto.
#In folium.Map(), you can customize various parameters to control the map’s appearance
# and behavior
#You can have: location of the center of the map, initial zoom level, basemap style (tiles),
# map dimensions, zoom limits, and more.

m = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

#Here we add a circle to the map to represent the 10-mile radius around the zip code.
# folium.Circle() creates a circle overlay on the map.
#You can have various parameters like location (center of the circle),
# radius (in meters), fill color, opacity, and popup text.
#The .add_to(m) method attaches the circle to the map object m we created earlier

folium.Circle(
    location=[location.latitude, location.longitude],
    radius=radius,
    fill=True,
    fill_opacity=0.0,
    popup="10-mile radius"
).add_to(m)

#Here we add markers for each Starbucks location within the radius.
#MarkerCluster groups nearby markers into clusters for better visualization.
# folium.Marker() creates a marker at a specific location with an optional popup.
#The .add_to(marker_cluster) method attaches each marker to the MarkerCluster we created.

#Because Folium doesn’t know how to automatically take an 
#entire GeoDataFrame and plot all markers at once, you need a for loop to plot all the datas
#You need to go row by row, extract coordinates + attributes, and then create one marker per row.
#The for loop does exactly that: “for each store, place a marker on the map.”


marker_cluster = MarkerCluster().add_to(m)
for idx, row in stores_in_radius.to_crs(epsg=4326).iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row["name"]).add_to(marker_cluster)

st.subheader("Map of Starbucks within 10 miles")
st_folium = st.components.v1.html(m._repr_html_(), height=600)

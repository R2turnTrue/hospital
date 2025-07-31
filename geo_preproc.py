import fiona
import geopandas as gpd
import os
from shapely.ops import unary_union

path = "data_shapes/ctprvn.shp"
print(path)
c = fiona.open(path, encoding='cp949')
print(c.crs)
gdf = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174
gdf = gdf.union_all()
gdf = gpd.GeoDataFrame(geometry=[gdf], crs="epsg:5174")
gdf.to_file("data_shapes/ctprvn_processed.shp", encoding='utf-8')
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import fiona
import geopandas as gpd
import os

path = "data_shapes/ctprvn_processed.shp"
print(path)
c = fiona.open(path, encoding='utf-8')
print(c.crs)
gdf = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174
gdf.info()

gdf['coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
gdf['coords'] = [coords[0] for coords in gdf['coords']]
fig, ax = plt.subplots(figsize = (10,10))
gdf.plot(ax=ax, color='yellow', edgecolor='black')
for idx, row in gdf.iterrows():
   plt.annotate(str(row['FID']), xy=row['coords'], horizontalalignment='center', color='blue')

plt.show()
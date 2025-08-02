import matplotlib.pyplot as plt
import fiona
import geopandas as gpd
import os
from shapely.ops import unary_union
import matplotlib.font_manager as fm

fe = fm.FontEntry(
    fname='conconfont.ttf',
    name='Ownglyph corncorn')
fm.fontManager.ttflist.insert(0, fe)
plt.rcParams.update({'font.size': 12, 'font.family': 'Ownglyph corncorn'})

path = "data_shapes/result_voro.shp"
print(path)
c = fiona.open(path, encoding='utf-8')
print(c.crs)
gdf = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174
gdf.info()
gdf.plot(column='acceptance', legend=True, edgecolor='face', linewidth=0.4, antialiased=False)
plt.title("의료 시설 부담 지수 (높을수록 의료 시설이 더 많은 인원을 수용해야함)")

plt.show()
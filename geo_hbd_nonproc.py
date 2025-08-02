import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import fiona
import geopandas as gpd
import os

fe = fm.FontEntry(
    fname='conconfont.ttf',
    name='Ownglyph corncorn')
fm.fontManager.ttflist.insert(0, fe)
plt.rcParams.update({'font.size': 12, 'font.family': 'Ownglyph corncorn'})

path = "data_shapes/ctprvn.shp"
print(path)
c = fiona.open(path, encoding='utf-8')
print(c.crs)
gdf = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174
gdf.info()
gdf.plot()
plt.show()
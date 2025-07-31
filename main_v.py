import matplotlib.pyplot as plt
import geopandas as gpd
import os
from shapely.ops import unary_union
import matplotlib.font_manager as fm

fe = fm.FontEntry(
    fname='conconfont.ttf',
    name='Ownglyph corncorn')
fm.fontManager.ttflist.insert(0, fe)
plt.rcParams.update({'font.size': 12, 'font.family': 'Ownglyph corncorn'})

path = "data_shapes/ctprvn_processed.shp"
print(path)
gdf = gpd.read_file(path, encoding='utf-8')
#gdf = gdf.convex_hull
gdf.plot(color='lightblue', edgecolor='black')
plt.title('한국 행정구역')
plt.show()
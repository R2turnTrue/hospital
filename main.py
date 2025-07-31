import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi

fe = fm.FontEntry(
    fname='conconfont.ttf',
    name='Ownglyph corncorn')
fm.fontManager.ttflist.insert(0, fe)
plt.rcParams.update({'font.size': 12, 'font.family': 'Ownglyph corncorn'})

df = pd.read_csv("data_hospital/HospitalData.csv", encoding='utf-8')
df = df[df['영업상태구분코드'] == 1] # 영업중인 병원만

points = []
address = []
for index, row in df.iterrows():
    # NaN 제거
    if row['좌표정보y(epsg5174)'] == row['좌표정보y(epsg5174)'] and row['좌표정보x(epsg5174)'] == row['좌표정보x(epsg5174)']:
        points.append((row['좌표정보x(epsg5174)'], row['좌표정보y(epsg5174)']))
        address.append(row['도로명전체주소'])

sido_list = [addr.split()[0] if isinstance(addr, str) else "기타" for addr in address]

points = np.array(points)
vor = Voronoi(points)

regions = []
sido_filtered = []
for i, region_index in enumerate(vor.point_region):
    region = vor.regions[region_index]
    if not region or -1 in region:
        # 무한한 지역 X
        continue
    polygon = Polygon([vor.vertices[j] for j in region])
    regions.append(polygon)
    sido_filtered.append(sido_list[i])

# GeoDataFrame 생성
gdf = gpd.GeoDataFrame({'sido': sido_filtered, 'geometry': regions}, crs='epsg:5174')
gdf.plot(column='sido', cmap='tab20', legend=True, edgecolor='black')

plt.title('의료시설 보로노이 다이어그램')
plt.tight_layout()
plt.show()
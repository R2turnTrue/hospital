import matplotlib.pyplot as plt
import fiona
import geopandas as gpd
import os
from shapely.ops import unary_union

population_data = {
    "전국": 51159889,
    "서울특별시": 9323492,
    "부산광역시": 3251625,
    "대구광역시": 2357040,
    "인천광역시": 3041215,
    "광주광역시": 1398538,
    "대전광역시": 1460682,
    "울산광역시": 1093317,
    "세종특별자치시": 392154,
    "경기도": 13715016,
    "강원특별자치도": 1510181,
    "충청북도": 1591815,
    "충청남도": 2136299,
    "전라북도": 1729337,
    "전라남도": 1782183,
    "경상북도": 2516753,
    "경상남도": 3214016,
    "제주특별자치도": 666226
}

path = "data_shapes/ctprvn.shp"
print(path)
c = fiona.open(path, encoding='cp949')
print(c.crs)
gdf = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174

gdf.plot()

plt.show()
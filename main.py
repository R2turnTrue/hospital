print('importing gpd')
import geopandas as gpd

print('importing pd')
import pandas as pd

print('importing shapely')
from shapely.geometry import Polygon, Point
from shapely import intersection, area
from shapely.ops import unary_union

print('importing matplotlib')
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

print('importing numpy')
import numpy as np

print('importing scipy')
from scipy.spatial import Voronoi

print('importing fiona')
import fiona

print('importing tqdm')
from tqdm import tqdm

# 2025년 7월 기준 데이터 (출처: https://jumin.mois.go.kr/)
"""
population_data = {
    #"전국": 51159889,
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
"""
# 근데 이렇게 하려니 값이 너무 커져서 그냥 상대도수로 계산
population_data = {
    #"전국": 51159889,
    "서울특별시": 9323492/51159889.0,
    "부산광역시": 3251625/51159889.0,
    "대구광역시": 2357040/51159889.0,
    "인천광역시": 3041215/51159889.0,
    "광주광역시": 1398538/51159889.0,
    "대전광역시": 1460682/51159889.0,
    "울산광역시": 1093317/51159889.0,
    "세종특별자치시": 392154/51159889.0,
    "경기도": 13715016/51159889.0,
    "강원특별자치도": 1510181/51159889.0,
    "충청북도": 1591815/51159889.0,
    "충청남도": 2136299/51159889.0,
    "전라북도": 1729337/51159889.0,
    "전라남도": 1782183/51159889.0,
    "경상북도": 2516753/51159889.0,
    "경상남도": 3214016/51159889.0,
    "제주특별자치도": 666226/51159889.0
}

# 지역 넓이 (gdf_city의 geometry 컬럼 기준)
area_data = {}

fe = fm.FontEntry(
    fname='conconfont.ttf',
    name='Ownglyph corncorn')
fm.fontManager.ttflist.insert(0, fe)
plt.rcParams.update({'font.size': 12, 'font.family': 'Ownglyph corncorn'})

print('filtering hospital data...')

# 병원 데이터 로드
df = pd.read_csv("data_hospital/HospitalData.csv", encoding='utf-8')
df = df[df['영업상태구분코드'] == 1] # 영업중인 병원만
df = df[df['의료인수'] != 0] # 의료인수가 0인 병원 제외 (아마 데이터 오류?)

points = []
beds = []
address = []
for index, row in df.iterrows():
    # NaN 제거
    if row['좌표정보y(epsg5174)'] == row['좌표정보y(epsg5174)'] and row['좌표정보x(epsg5174)'] == row['좌표정보x(epsg5174)']:
        points.append((row['좌표정보x(epsg5174)'], row['좌표정보y(epsg5174)']))
        beds.append(row['의료인수']) # 이름만 beds지 (과거 병상수로 카운트),,, 의료인수임.
        address.append(row['도로명전체주소']) # 사실 예전엔 도로명주소 기반으로 병원 수용도 계산. 지금은 디버깅 용도로만 사용.

#### 과거 사용. 디버깅용.
sido_list = [addr.split()[0] if isinstance(addr, str) else "기타" for addr in address]

points = np.array(points)
vor = Voronoi(points)

regions = []
sido_filtered = []
beds_filtered = []
for i, region_index in enumerate(vor.point_region):
    region = vor.regions[region_index]
    if not region or -1 in region:
        # 무한한 지역 X
        continue
    polygon = Polygon([vor.vertices[j] for j in region])
    regions.append(polygon)
    sido_filtered.append(sido_list[i])
    beds_filtered.append(beds[i])

# 보로노이 다이어그램 + 의료인 수 + 지역 이름
gdf_voronoi = gpd.GeoDataFrame({'sido': sido_filtered, 'geometry': regions, 'beds': beds_filtered}, crs='epsg:5174')
#gdf_hospital.plot(column='sido', cmap='tab20', legend=True, edgecolor='black')

print('loading city shapes')

# 도시 정보 포함 (area_data 측정 + 면적 대비 인구 계산)
c = fiona.open("data_shapes/ctprvn.shp", encoding='cp949')
print(c.crs)
gdf_city = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174

# 남한 국토 (Intersect 용도, 데이터 더 보기 쉽게 하려고.)
c = fiona.open("data_shapes/ctprvn_processed.shp", encoding='cp949')
print(c.crs)
gdf_country = gpd.GeoDataFrame.from_features(c, crs=c.crs).to_crs('epsg:5174') #epsg5174
country_geo = gdf_country['geometry'].iloc[0]
#print('country geometry:', country_geo)

# 도시 면적 게산 (shapely 날먹)
for ic, c_row in gdf_city.iterrows():
    city_name = c_row['CTP_KOR_NM']
    area_data[city_name] = area(c_row['geometry'])
    print(f"calculated {city_name} area: {area_data[city_name]}")

print('calculating hospital acceptances')

pbar = tqdm(total=len(gdf_voronoi) * len(gdf_city), desc='Calculating acceptance', unit='hospital-city')
for iv, v_row in gdf_voronoi.iterrows():
    people_cnt = 0
    
    for ic, c_row in gdf_city.iterrows():
        city_name = c_row['CTP_KOR_NM']
        if city_name not in population_data:
            continue
        city_area = area_data[city_name]
        people_count = population_data[city_name]
        intersect = intersection(v_row['geometry'], c_row['geometry'])
        intersect_area = area(intersect)
        
        #if intersect_area > 0:
            #print('collapsing hospital at', v_row['sido'], 'with city', city_name, 'area:', intersect_area)

        #print()
        #print(intersect_area / float(city_area))
        people_cnt += (intersect_area / float(city_area)) * people_count # 면적대비 인구 비례
        pbar.update(1)

    gdf_voronoi.at[iv, 'geometry'] = intersection(v_row['geometry'], country_geo) # 국가 경계 안에 있는지 확인. 디버그할땐 없는게 나음; 속도 개느림.
    gdf_voronoi.at[iv, 'acceptance'] = people_cnt / float(v_row['beds']) # 의료인 수는 반비례
    
    #### 의료 시설 부담 지수
    # ((병원이 수용해야하는 면적/도시 면적) * 도시 인구) / 병상 수
    # 얘가 높을수록 병원이 엄청 더 많은 사람을 수용해야함. ---> 병원이 부족함.
    # 낮을수록 병원이 적은 사람을 수용함. ---> 여유, 혹은 병원이 너무 많음.

gdf_voronoi.to_file("data_shapes/result_voro.shp", encoding='utf-8')
print("wrote result to data_shapes/result_voro.shp")
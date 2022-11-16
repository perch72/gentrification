import urllib.request ,os
import json 
from search_juso import *
import folium

juso_keyword = '부산역'
juso_cnt = 5 
addresses = search_juso(juso_keyword, juso_cnt)
# print(addresses)
for address in addresses:
    
    encoding_address = urllib.parse.quote_plus(address[4])
    url =f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={encoding_address}'
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID","g16y0o5aaa")
    request.add_header("X-NCP-APIGW-API-KEY","0FqB7fToW2cclewTZVL87xFWn7HV6mH0Kb6UvXEo")

    response = urllib.request.urlopen(request)
    response_code = response.getcode()
    if response_code == 200:
        try: 
            response_body = response.read().decode('utf-8')
            data = json.loads(response_body)

            address.append([float(data['addresses'][0]['y']),float(data['addresses'][0]['x'])])
            print(data['addresses'][0]['x'] + "-" + data['addresses'][0]['y'])  
            continue
        except:
            address.append([0,0]) 
            print(f'error:{response_code}')


m = folium.Map(
  location=addresses[0][5],
  zoom_start=17
)

from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

for i in range(len(addresses)):
    print(f'{addresses[i][5][0]} {addresses[i][5][1]}  {addresses[i][4]}')
    folium.Marker(
        location=addresses[i][5],
        popup='test',
        icon=folium.Icon(color='red',icon='ok'),
    ).add_to(marker_cluster)

m.save('map.html')
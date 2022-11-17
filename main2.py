
from bs4 import BeautifulSoup
import time
import urllib.request
import json 
from search_juso import *
import folium
from selenium import webdriver

from folium.plugins import MarkerCluster


driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(10)

driver.get("https://www.instagram.com/explore/locations/c1288116/yongin-south-korea/")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

my_titles = soup.select('ul>li>a')
baseurl='https://www.instagram.com/explore/tags/'

data = []
for title in my_titles[0:15]:
    origin_title = title.get_text()
    param = origin_title.replace("(","").replace(")","").replace(",","").replace(" ","")
    print("["+param+"]")
    param = urllib.parse.quote(param)
    driver.get(baseurl + param) 
    time.sleep(2)
    htmls  = driver.page_source
    bs=BeautifulSoup(htmls,'html.parser')  

    mydivs = bs.find_all("span",{"class":"_ac2a"})
    for dd in mydivs:
        data.append([title.get_text(),dd.get_text(),origin_title])
print(data)

print("search end") 
juso_cnt = 1 
iCount = 0 
map_data = []
for (address_name,view,orign_address_name) in data:
    addresses = search_juso(orign_address_name, juso_cnt)
    if(len(addresses)):
        address = addresses[0]
        print(address[4])
        encoding_address = urllib.parse.quote_plus(address[4])
        url =f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={encoding_address}'
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID","g16y0o5aaa")
        request.add_header("X-NCP-APIGW-API-KEY","0FqB7fToW2cclewTZVL87xFWn7HV6mH0Kb6UvXEo")
        response = urllib.request.urlopen(request)
        time.sleep(1)
        response_code = response.getcode()
        print(response_code)
        if response_code == 200:
            try: 
                print("searching")
                response_body = response.read().decode('utf-8')
                data = json.loads(response_body)
                map_data.append([address_name,address[4],[float(data['addresses'][0]['y']),float(data['addresses'][0]['x'])]])

                print(map_data)  
                continue
            except:
                # address.append(address[4],[0,0]) 
                print(f'error:{response_code}')
                continue
        iCount = iCount + 1
    
if(len(map_data)>0):

    m = folium.Map(
        location=map_data[0][2],
        zoom_start=12
        )
    marker_cluster = MarkerCluster().add_to(m)

    for i in range(len(map_data)):
        print(f'{map_data[i][0]}')
        folium.Marker(
            location=map_data[i][2],
            # popup=map_data[i][0],
            tooltip=map_data[i][0],
            icon=folium.Icon(color='red',icon='ok'),
        ).add_to(marker_cluster)

        # folium.CircleMarker(
        #             location=map_data[i][2],
        #             tooltip=map_data[i][0],
        #             color='tomato',
        #             radius = 200).add_to(marker_cluster)g


    m.save('map.html')
    driver.get("file:///C:/Users/home/Documents/%EA%B1%B4%EC%9A%B0/map.html")
    input("종료를 원하시면 아무런 키를 눌러주세요 ")

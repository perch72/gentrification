
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
for title in my_titles[0:5]:
    param = title.get_text().replace("(","").replace(")","").replace(",","").replace(" ","")
    print("["+param+"]")
    param = urllib.parse.quote(param)
    driver.get(baseurl + param) 
    time.sleep(2)
    htmls  = driver.page_source
    bs=BeautifulSoup(htmls,'html.parser')  

    mydivs = bs.find_all("span",{"class":"_ac2a"})
    for dd in mydivs:
        data.append([title.get_text(),dd.get_text()])


print("search end") 
juso_cnt = 1 
iCount = 0;
map_data = []
for row in data:
    addresses = search_juso(row[0], juso_cnt)
    # print(addresses)
    address = addresses[0]
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

            map_data.append(address[4],[float(data['addresses'][0]['y']),float(data['addresses'][0]['x'])])
            print(data['addresses'][0]['x'] + "-" + data['addresses'][0]['y'])  

            continue
        except:
            # address.append(address[4],[0,0]) 
            print(f'error:{response_code}')
    iCount = iCount + 1
    
if(len(map_data)>0):

    m = folium.Map(
    location=addresses[0][5],
    zoom_start=17
    )
    marker_cluster = MarkerCluster().add_to(m)

    for i in range(len(map_data)):
        print(f'{addresses[i][5][0]} {addresses[i][5][1]}  {addresses[i][4]}')
        folium.Marker(
            location=addresses[i][5],
            popup='test',
            icon=folium.Icon(color='red',icon='ok'),
        ).add_to(marker_cluster)


m.save('map.html')
driver.get("map.html")

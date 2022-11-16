from selenium import webdriver

from bs4 import BeautifulSoup
import time
import urllib.request

# chromedriver = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get("https://www.instagram.com/explore/locations/c1288116/yongin-south-korea/")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

my_titles = soup.select('ul>li>a')
baseurl='https://www.instagram.com/explore/tags/'

placedata=[]
for title in my_titles[0:10]:
    param = title.get_text().replace("(","").replace(")","").replace(",","").replace(" ","")
    print("["+param+"]")
    param = urllib.parse.quote(param)
    driver.get(baseurl + param) 
    time.sleep(2)
    htmls  = driver.page_source
    bs=BeautifulSoup(htmls,'html.parser')  

    mydivs = bs.find_all("span",{"class":"_ac2a"})
    data = []
    for dd in mydivs:
        data.append([title.get_text(),dd.get_text()])

    print("search end")
    print(data)
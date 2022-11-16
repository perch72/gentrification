import time, random, re
import requests
from bs4 import BeautifulSoup

def search_juso(workbook_name,juso_sheetname,keyword, juso_cnt):
    ## 추출한 주소 저장할 엑셀 생성 


    ## 주소 추출하기
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }

    ext_cnt = int(juso_cnt//10) + 1
    row = 2
    rows = []
    for page in range(1, ext_cnt + 1):
        url = f'https://www.juso.go.kr/support/AddressMainSearch.do?currentPage={page}&countPerPage=10&&searchType=\\n        TOTAL&searchKeyword={keyword}&firstSort=none&ablYn=Y&synnYn=N'

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        ol_lis = soup.select('#searchAddress > div.container.support_search_list > div.search_list > ol > li')
        
        for li in ol_lis:
            if juso_cnt == (row - 2):
                break
            try:
                roed_juso = li.find('div', class_='subejct_1').find('span', class_='roadNameText').text
                road = re.sub('&nbsp;|\t|\r|\n', '', roed_juso).strip().replace('  ', ' ')
                print(f'\n[{row-1}] 주소추출:\n{road}')
                
                road_eng = li.find('div', class_='addrEngInfo').find('span', class_='addrEng').text
                eng_roadname = re.sub('&nbsp;|\t|\r|\n', '', road_eng).strip().replace('  ', ' ')
                print(eng_roadname)                
                
                jibeon_juso = li.find('div', class_='subejct_2').find('span', class_='roadNameText').text
                jibeon = re.sub('&nbsp;|\t|\r|\n', '', jibeon_juso).strip().replace('  ', ' ')
                print(jibeon)
                
                zipcode = li.select_one('div.addrWrap > div.zipcode > div > strong').text
                print(zipcode)
                
                btn = li.find('button', class_='btn_dtaddr_on')

                ## 상세주소(동.층.호) 버튼이 있는 경우만 엑셀에 저장 
                if btn: 
                    rows.append( [row - 1,zipcode,road,eng_roadname,jibeon])
                    row += 1
                else:
                    continue
            except Exception as e:
                print(f'\nError: {e}\n')
                err = f'Error: {e}\n'
                with open('error.txt', 'a') as f:
                    f.write(err)
                continue
    return rows
        # time.sleep(random.uniform(0.5, 1))
from selenium import webdriver
import time
from selenium.webdriver.common.by import By



id = 'gunoue@naver.com'
pw = 'rlarjsdn313'

#chromedriver = r'C:\dev_python\Webdriver\chromedriver.exe'
driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get('https://www.instagram.com/?hl=ko')

time.sleep(1)

id_inp = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label')
id_inp.click()
id_inp.send_keys(id)

pw_inp = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label')
pw_inp.click()
pw_inp.send_keys(pw)

log_btn = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')
log_btn.click()

time.sleep(1)
option_btn = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/section/main/div/div/div/div/button')
option_btn.click()

print("test")
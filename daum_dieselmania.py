from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os
import pyperclip
import time
from datetime import datetime

id = " "
pw = " "
df = pd.read_excel('data.xlsx')

# 최종 업로드 일시로 오름차순 정렬
df.sort_values(by=['업로드'], axis=0, inplace=True) 

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path='C:/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttp%253A%252F%252Fcafe.daum.net%252F_c21_%252Fhome%253Fgrpid%253D10akR')

driver.find_element_by_xpath('//*[@id="id_email_2"]').send_keys(id)
driver.find_element_by_xpath('//*[@id="id_password_3"]').send_keys(pw)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
time.sleep(1)

no_up = 0
outer = 0
coat = 0
shirts = 0
pants = 0

for i in range(len(df.index)):
    
    if df.loc[i, '다음디매'] == 'N':
        no_up = no_up + 1
        continue
    
    # 해당 카테고리 등록 3회 초과할 경우 패스
    if df.loc[i, '카테고리'] in ('점퍼'):
        ctgr = 'IyAy'
        outer = outer + 1
        if outer > 3:
            continue
    elif df.loc[i, '카테고리'] in ('코트'):
        ctgr = 'RjEm'
        coat = coat + 1
        if coat > 3:
            continue
    elif df.loc[i, '카테고리'] in ('셔츠'):
        ctgr = 'Rnru'
        shirts = shirts + 1
        if shirts > 3:
            continue
    elif df.loc[i, '카테고리'] in ('바지'):
        ctgr = 'Falq'
        pants = pants + 1
        if pants > 3:
            continue
        
    driver.get('http://cafe.daum.net/dieselmania/'+ctgr)

    driver.switch_to.frame('down')
    driver.find_element_by_xpath('//*[@id="article-write-btn"]').click()
    
    driver.find_element_by_xpath('//*[@id="primaryContent"]/div[1]/div[1]/div[1]/div[2]/a').click()
    driver.find_element_by_xpath('//*[@id="primaryContent"]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/a').click()
    driver.find_element_by_xpath('//*[@id="title-input"]').send_keys(df.loc[i, '다음디매상품명'])
    
    driver.switch_to.frame('keditorContainer_ifr')
    driver.find_element_by_xpath('//*[@id="tinymce"]/p').click()
    
    webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    webdriver.ActionChains(driver).key_down(Keys.SHIFT).perform()
    
    for j in range(1, 12):
        webdriver.ActionChains(driver).send_keys(Keys.ARROW_UP).perform()

    webdriver.ActionChains(driver).key_up(Keys.SHIFT).perform()
    webdriver.ActionChains(driver).send_keys(Keys.DELETE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    webdriver.ActionChains(driver).send_keys(df.loc[i, '다음디매내용']).perform()

    driver.switch_to.default_content()
    driver.switch_to.frame('down')
    driver.find_element_by_xpath('//*[@id="mceu_0"]').click()
    driver.find_element_by_css_selector("input[id='openFile']").send_keys(df.loc[i, '이미지'])
    time.sleep(5)

    os.system(r'FileOpen_Close.exe')

    driver.find_element_by_xpath('//*[@id="primaryContent"]/div[1]/div[6]/div[2]/button[3]').click()

    now = str(datetime.now())
    df.loc[i, '업로드'] = now[5:7] + now[8:10] + now[11:13] + now[14:16]

driver.quit()

df.to_excel('data.xlsx', index=False)
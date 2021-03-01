from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import pyperclip
import time

id = " "
pw = " "

df = pd.read_excel('data.xlsx')

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path='C:/chromedriver.exe')
driver.implicitly_wait(5)
driver.get('http://cafe.naver.com/joonggonara')

login_btn = driver.find_element_by_id('gnb_login_button')
login_btn.click()

tag_id = driver.find_element_by_id('id')
tag_pw = driver.find_element_by_id('pw')

tag_id.click()
pyperclip.copy(id)
tag_id.send_keys(Keys.CONTROL, 'v')

tag_pw.click()
pyperclip.copy(pw)
tag_pw.send_keys(Keys.CONTROL, 'v')

driver.find_element_by_id('log.login').click()
driver.find_element_by_id('new.save').click()

no_up = 0

for i in range(len(df.index)):
    
    if df.loc[i, '중고나라'] == 'N':
        no_up = no_up + 1
        continue
    
    if df.loc[i, '카테고리'] in ('코트', '점퍼', '셔츠'):
        driver.find_element_by_id('menuLink358').click()
    elif df.loc[i, '카테고리'] in ('바지'):
        driver.find_element_by_id('menuLink359').click()
    elif df.loc[i, '카테고리'] in ('청소기'):
        driver.find_element_by_id('menuLink452').click()
    
    driver.switch_to.frame('cafe_main')
    driver.find_element_by_id('writeFormBtn').click()
    driver.switch_to.window(driver.window_handles[i+1-no_up])
    
    try:
        driver.find_element_by_class_name('se-popup-close-button').click()
    except:
        pass
    
    driver.find_element_by_class_name('textarea_input').send_keys(df.loc[i, '상품명'])
    driver.find_element_by_class_name('input_text').send_keys(int(df.loc[i, '판매가격']))  
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[2]/div/button').click()

    if df.loc[i, '카테고리'] in ('니트', '바지', '셔츠', '재킷', '점퍼', '코트', '티셔츠'):        
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[1]/li[9]/button').click()
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[2]/li[2]/button').click()

        if df.loc[i, '카테고리'] == '니트':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[1]/button'
        elif df.loc[i, '카테고리'] == '바지':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[3]/button'
        elif df.loc[i, '카테고리'] == '셔츠':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[4]/button'
        elif df.loc[i, '카테고리'] == '재킷':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[6]/button'
        elif df.loc[i, '카테고리'] == '점퍼':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[7]/button'
        elif df.loc[i, '카테고리'] == '코트':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[13]/button'
        elif df.loc[i, '카테고리'] == '티셔츠':
            ctgr_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[15]/button'        
        
        driver.find_element_by_xpath(ctgr_xpath).click()

    elif df.loc[i, '카테고리'] == '청소기':                       
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[1]/li[2]/button').click()
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[2]/li[10]/button').click()
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[2]/div/div/ul[3]/li[18]/button').click()
        
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[10]/div/div/div[3]/a').click()
    
    if df.loc[i, '상태'] == '미개봉':
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[3]/div/div[1]/label').click()
    elif df.loc[i, '상태'] == '거의새것':
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/label').click()
    elif df.loc[i, '상태'] == '사용감있음':
        driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[3]/div/div[3]/label').click()
        
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[4]/div/button[2]').click()
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[6]/div/div[1]/label').click()
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[6]/div/div[2]/label').click()
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[8]/div/div/div[1]/label').click()
    driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[8]/div/div/div[2]/label').click()
    driver.find_element_by_class_name('se-container').click()
    
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    webdriver.ActionChains(driver).send_keys(Keys.DELETE).perform()
    webdriver.ActionChains(driver).send_keys(df.loc[i, '중고나라내용']).perform()
    
    driver.find_element_by_class_name("se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button").click()
    time.sleep(1)

    os.system(r'FileOpen_Close.exe')
    
    driver.find_element_by_css_selector("input[type='file']").send_keys(df.loc[i, '이미지'])
    time.sleep(5)
    
    driver.find_element_by_class_name('BaseButton.BaseButton--skinGreen.size_default').click()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()
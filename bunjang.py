from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import pandas as pd
import os
import pyperclip
import time
from datetime import datetime

id = " "
pw = " "

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path='C:/chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://m.bunjang.co.kr/')

driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div[2]/button').click()
driver.find_element_by_xpath('//*[@id="root"]/div/div/div[7]/div/div[1]/div[3]/button[1]').click()

driver.switch_to.window(driver.window_handles[1])
driver.find_element_by_id('id_email_2').send_keys(id)
driver.find_element_by_id('id_password_3').send_keys(pw)

driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
time.sleep(1)

driver.switch_to.window(driver.window_handles[0])
driver.get('https://m.bunjang.co.kr/shop/3300054/products')
time.sleep(1)

driver.find_element_by_xpath('//*[@id="root"]/div/div/div[5]/div/div[1]/div/div[1]/div/div[2]/div[3]/a').click()
time.sleep(1)

page = 2

while(1):

    status = driver.find_elements_by_class_name('css-1uccc91-singleValue')
    btns = driver.find_elements_by_tag_name('button')

    selling = 0
    ups = []

    for sts in status:
        if sts.text == '판매 중':
            selling = selling + 1

    for btn in btns:
        if btn.text == 'UP':
            ups.append(btn)

    if selling == 0:
        break
    
    for i in range(selling):
        ups[i].click()
        time.sleep(1)
        try:
            da = Alert(driver)
            da.accept()
        except:
            pass

    driver.get('https://m.bunjang.co.kr/products/manage?page='+str(page))
    page = page + 1

driver.quit()

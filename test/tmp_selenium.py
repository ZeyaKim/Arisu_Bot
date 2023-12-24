import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

sourcenao_url = 'https://saucenao.com/'
image_url ='https://cdn.discordapp.com/attachments/736308994733375602/1111317327875690496/viewimage.png'
driver = webdriver.Chrome()
driver.get(sourcenao_url)




input()

search_box = driver.find_element(By.XPATH, '//*[@id="urlInput"]')
search_box.send_keys(image_url)

database_button = driver.find_element(By.XPATH, '//*[@id="database-dropdown-button"]')
database_button.click()

checkbox = driver.find_element(By.XPATH, '//*[@id="searchRowContainer"]/div/div[2]/label[4]')
checkbox.click()

back_button = driver.find_element(By.XPATH, '//*[@id="searchRowContainer"]/div/div[3]')
back_button.click()

button = driver.find_element(By.XPATH, '//*[@id="searchButton"]')
button.click()

input()

#next page
pixiv_button = driver.find_element(By.XPATH, '//*[@id="middle"]/div[2]/table/tbody/tr/td[2]/div[2]/div[2]/a[1]')
print(pixiv_button.text)
# import libraries
from bs4 import BeautifulSoup
#import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# specify the url
url = 'https://www.bps.go.id/dynamictable/2016/06/16/1211/indeks-pembangunan-manusia-menurut-provinsi-2010-2018-metode-baru-.html'

# The path to where you have your chrome webdriver stored:
webdriver_path = 'C:\Users\haditiyawijaya\Downloads\chromedriver_win32\chromedriver.exe'

    # Add arguments telling Selenium to not actually open a window
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')

    # Fire up the headless browser
browser = webdriver.Chrome(executable_path=webdriver_path,
                               options=chrome_options)

    # Load webpage
browser.get(url)

    # It can be a good idea to wait for a few seconds before trying to parse the page
    # to ensure that the page has loaded completely.
time.sleep(10)

    # Parse HTML, close browser
soup = BeautifulSoup(browser.page_source, 'html.parser')
browser.quit()

# find results within table
result_wilayah  = soup.find('table', attrs={'id': 'tableLeftBottom'})
result_value    = soup.find('table', attrs={'id': 'tableRightBottom'})

rows_wilayah    = result_wilayah.find_all('tr')
rows_value      = result_value.find_all('tr')

list_wilayah = []
value = []

# print(rows)
for id, r in enumerate(rows_wilayah[:-1]):
    # find all columns per result
    data_wilayah = r.find_all('td', attrs={'id': 'th4'})
    data_value = rows_value[id].find_all('td', attrs={'class': 'datas'})

    # check that columns have data
    if len(data_wilayah) == 0:
        continue

    # write columns to variables
    wilayah = data_wilayah[0].find('b').getText()
    nilai = data_value[-1].getText()
    # Remove decimal point
    #nilai = nilai.replace('.','')
    # Cast Data Type Integer
    nilai = float(nilai)
    list_wilayah.append(wilayah)
    value.append(nilai)

# # Convert to numpy
np_array2 = np.array(list_wilayah)
np_value2= np.array(value)


# Naming label
plt.xlabel('provinsi')
plt.ylabel('tingkat IPM')

# styling x,y value
plt.xticks(rotation=30,ha='right')
plt.yticks(np.arange(np_value2.min(),np_value2.max(),4000000))

# plot data
plt.plot(np_array2,np_value2,color='green',label='Tingkat IPM',linestyle='--', marker='o')
plt.legend(loc='upper right')
plt.yscale('linear')
plt.show()

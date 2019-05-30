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
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression


# specify the url
url = 'https://kawalpemilu.org/#pilpres:0'

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
# print(soup)
pretty = soup.prettify()
browser.quit()
# find results within table
results = soup.find('table',{'class':'table'})
rows = results.find_all('tr',{'class':'row'})
#array = []
jokowi = []
#prabowo = []
sah = []

# print(rows)
for r in rows:
    # find all columns per result
    data = r.find_all('td')
    # check that columns have data
    if len(data) == 0:
        continue
# write columns to variables
    #wilayah = data[1].find('a').getText()
    satu = data[2].find('span', attrs={'class':'abs'}).getText()
    #dua = data[3].find('span', attrs={'class': 'abs'}).getText()
    tiga = data[4].find('span', attrs={'class': 'sah'}).getText()
    # Remove decimal point
    satu = satu.replace('.','')
    #dua = dua.replace('.','')
    tiga = tiga.replace('.','')
    # Cast Data Type Integer
    satu = int(satu )
    #dua = int(dua)
    tiga = int(tiga)
    #array.append(wilayah)
    jokowi.append(satu)
    #prabowo.append(dua)
    sah.append(tiga)

# Create Dictionary
#my_dict = {'wilayah':array,'value1':jokowi,'value2':prabowo,'value3':sah}
my_dict = {'value1':jokowi,'value2':sah}

# Create Dataframe
df = pd.DataFrame(my_dict)
#print(df)

#slicing data
X = df.iloc[:, :-1].values
y = df.iloc[:, 1].values

# Membagi data menjadi Training Set dan Test Set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

#Feature Scaling

"""from sklearn.preprocessing import StandardScaler

scale_X = StandardScaler()

X_train = scale_X.fit_transform(X_train)
X_test = scale_X.transform(X_test)"""

# Fitting Simple Linear Regression terhadap Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Memprediksi hasil Test Set
#y_pred = regressor.predict(X_test)

# Visualisasi hasil Training Set
plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('Jokowi vs Suara Sah (Training set)')
plt.xlabel('Jokowi')
plt.ylabel('Suara Sah')
plt.show()

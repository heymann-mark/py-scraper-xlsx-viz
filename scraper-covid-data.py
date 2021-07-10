import requests
from bs4 import BeautifulSoup
import datetime
import csv
import matplotlib.pyplot as plt
import pandas as pd
out_list = []
# Collect the github page
page = requests.get('https://www.mass.gov/info-details/archive-of-covid-19-cases-in-massachusetts')
# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
repo = soup.find(class_="main-content main-content--two")
repo_list = repo.find_all('a')
#month = input("Enter month:").lower()
#day = input("Enter day:")
#year = input("Enter year:")
year = str(datetime.date.today().year)
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
month = months[datetime.date.today().month-1]
day = str(datetime.date.today().day+1)#tomorrow
found = 0
arr = []
while found == 0:
    day = str(int(day) - 1)
    for r in repo_list:
        arr = r.get('href').split(month+'-'+day+'-'+year)
        if(len(arr) >1):
            found  = 1
            url = r.get('href')
            url = 'https://www.mass.gov' + url
            res = requests.get(url)
            with open('./data'+month+day+year+'.xlsx', 'wb') as f:
                f.write(res.content)

data =  pd.read_excel('./data'+month+day+year+'.xlsx', 'DeathsReported (Report Date)', usecols = 'A,C') 
data.Date = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S.%f')
data.set_index('Date',inplace=True)
data.plot()
plt.title('Covid Deaths')
plt.show()



    
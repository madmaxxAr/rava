#from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import requests

from lxml import html

def getBonosName(bonosName,bonosN):
    i=0
    for child in bonosN:
        #nom = child[0].replace(' data-v-1c9ddfd8="">','')#get BONO nombre
        nom = child[0]
        #print(nom[20:])
        bonosName.insert(i,nom[20:])
        i+=1

def getBonosPre(bonosPre,bonosP):
    i=0
    for child in bonosP:
        precio = child[0]#.replace('="">','')
        precio = precio[12:]
        precio = precio.replace('.','')
        precio = precio.replace(',','.')
        #print(precio)
        if i%4==0:#get BONO precio en posiciones 0,4,8,12,16,20,24
            bonosPre.insert(i,precio)
        i+=1

def stripTablaBono(divBonos):
    a = re.findall('<a((.|\s)+?)</a>',str(divBonos))
    b = re.findall('<b((.|\s)+?)</b>',str(a))
    return a,b

def stripBonoPrices(divBono):
    return re.findall('<span data-v-((.|\s)+?)</span>',str(divBono))

#html_doc = 'https://datos.rava.com/'

#driver = webdriver.Firefox(executable_path="C:\\Users\\Maxx\\Downloads\\geckodriver-v0.29.1-win64\\geckodriver.exe")
#driver.get(html_doc)

url = 'https://datos.rava.com/'
data = requests.get(url,verify=False)

# This will get the initial html - before javascript
#html1 = driver.page_source
# This will get the html after on-load javascript
#html2 = driver.execute_script("return document.documentElement.innerHTML;")

#soup = BeautifulSoup(html2, 'lxml')
soup = BeautifulSoup(data.content, 'lxml')
soup = BeautifulSoup(data.content, 'html.parser')
#type(soup)
tree = html.fromstring(data.content)
soup = BeautifulSoup(html.tostring(tree), 'lxml')
soup = BeautifulSoup(html.tostring(tree), 'html.parser')

divBonosUSD = soup.select('div#tabla-dolares-usd') #get tabla nombre BONO USD especifica
divBonosARS = soup.select('div#tabla-dolares-ars') #get tabla nombre BONO ARS especifica


#strip tabla BONO USD
a,b = stripTablaBono(divBonosUSD)

#strip and get Bonds Names
bonoUSDNom=[]
getBonosName(bonoUSDNom,b)

#strip and get Bonds Prices
a = stripBonoPrices(divBonosUSD)
bonoUSDPre=[]
getBonosPre(bonoUSDPre,a)

#strip tabla BONO ARS
a,b = stripTablaBono(divBonosARS)

#strip and get Bonds Names
bonoARSNom=[]
getBonosName(bonoARSNom, b)
#strip and get Bonds Prices
a = stripBonoPrices(divBonosARS)
bonoARSPre=[]
getBonosPre(bonoARSPre,a)


bonosUSD = {
    "nombreUSD":bonoUSDNom,
    "precioUSD":bonoUSDPre
}

#print(bonosUSD)
bonosDF_USD = pd.DataFrame(bonosUSD)

bonosARS= {
    "nombreARS":bonoARSNom,
    "precioARS":bonoARSPre
}

bonosDF_ARS = pd.DataFrame(bonosARS)

bonosDF_ARS['ticker'] = bonosDF_ARS['nombreARS'] + str('D')
#or bonosDF_USD['nombreUSD'].str[:-1]

bonosDF = bonosDF_ARS.merge(bonosDF_USD,left_on='ticker',right_on='nombreUSD')

bonosDF['compraMEP'] = bonosDF['precioARS'].astype(float) / bonosDF['precioUSD'].astype(float)
bonosDF['compraMEP_AVG'] = bonosDF['compraMEP'].mean()
bonosDF['momento'] = datetime.datetime.now()

print(bonosDF)
print(bonosDF[bonosDF['compraMEP']==bonosDF['compraMEP'].min()])


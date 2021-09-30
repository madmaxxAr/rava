html_doc = 'https://datos.rava.com/'

from selenium import webdriver

from bs4 import BeautifulSoup
import urllib.request
from IPython.display import HTML
import re
import pandas as pd
import numpy as np
import sys
import datetime

driver = webdriver.Firefox(executable_path="C:\\Users\\Maxx\\Downloads\\geckodriver-v0.29.1-win64\\geckodriver.exe")
driver.get(html_doc)

# This will get the initial html - before javascript
#html1 = driver.page_source

# This will get the html after on-load javascript
html2 = driver.execute_script("return document.documentElement.innerHTML;")

soup = BeautifulSoup(html2, 'lxml')
type(soup)

divBonosUSD = soup.select('div#tabla-dolares-usd') #get tabla nombre BONO USD especifica
divBonosARS = soup.select('div#tabla-dolares-ars') #get tabla nombre BONO ARS especifica

#print(divBonosUSD)
#print(divBonosARS)
#print(type(divBonosUSD))

#strip tabla BONO USD
a = re.findall('<a((.|\s)+?)</a>',str(divBonosUSD))
b = re.findall('<b((.|\s)+?)</b>',str(a))


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

bonoUSDNom=[]
getBonosName(bonoUSDNom,b)
#i=0
#for child in b:
    #nom = child[0].replace(' data-v-1c9ddfd8="">','')#get BONO nombre
#    nom = child[0]
    #print(nom[20:])
#    bonoUSDNom.insert(i,nom[20:])
#    i+=1

a = re.findall('<span data-v-((.|\s)+?)</span>',str(divBonosUSD))
bonoUSDPre=[]
getBonosPre(bonoUSDPre,a)
#i=0
#for child in a:
#    precio = child[0]#.replace('="">','')
#    precio = precio[12:]
#    print(precio)
    #precio = precio.replace('.','')
    #precio = precio.replace(',','.')
#    if i%4==0:
#        bonoUSDPre.insert(i,precio[12:])#get BONO precio 0,4,8,12,16,20,24
#    i+=1

#print(bonoUSDNom)
#print(bonoUSDPre)

#strip tabla BONO ARS
a = re.findall('<a((.|\s)+?)</a>',str(divBonosARS))
b = re.findall('<b((.|\s)+?)</b>',str(a))

bonoARSNom=[]
getBonosName(bonoARSNom, b)
#i=0
#for child in b:
#    nom = child[0].replace(' data-v-1c9ddfd8="">','')#get BONO nombre
#    #print(nom)
#    bonoARSNom.insert(i,nom)
#    i+=1

a = re.findall('<span data-v-((.|\s)+?)</span>',str(divBonosARS))
bonoARSPre=[]
getBonosPre(bonoARSPre,a)
#i=0
#for child in a:
#    precio = child[0].replace('="">','')
#    precio = precio.replace('.','')
#    precio = precio.replace(',','.')
    #print(precio)
#    if i%4==0:
#        bonoARSPre.insert(i,precio)#get BONO precio 0,4,8,12,16,20,24
#    i+=1


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
bonosDF['momento'] = datetime.datetime.now()

print(bonosDF)
print(bonosDF[bonosDF['compraMEP']==bonosDF['compraMEP'].min()])
#print('current:-',datetime.datetime.now())
sys.exit()

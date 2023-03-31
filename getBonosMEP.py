html_doc = 'https://datos.rava.com/'

from selenium import webdriver

from bs4 import BeautifulSoup
import urllib.request
from IPython.display import HTML
import re
import pandas as pd
import numpy as np
import sys

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
#print(type(divBonosUSD))

#strip tabla BONO USD
a = re.findall('<a((.|\s)+?)</a>',str(divBonosUSD))
b = re.findall('<b((.|\s)+?)</b>',str(a))

bonoUSDNom=[]
i=0
for child in b:
    nom = child[0].replace(' data-v-0e629720="">','')#get BONO nombre
    #print(nom)
    bonoUSDNom.insert(i,nom)
    i+=1

a = re.findall('<span data-v-0e629720((.|\s)+?)</span>',str(divBonosUSD))
bonoUSDPre=[]
i=0
for child in a:
    precio = child[0].replace('="">','')
    precio = precio.replace('.','')
    precio = precio.replace(',','.')
    #print(precio)
    if i%4==0:
        bonoUSDPre.insert(i,precio)#get BONO precio 0,4,8,12,16,20,24
    i+=1

#print(bonoUSDNom)
#print(bonoUSDPre)

#strip tabla BONO ARS
a = re.findall('<a((.|\s)+?)</a>',str(divBonosARS))
b = re.findall('<b((.|\s)+?)</b>',str(a))

bonoARSNom=[]
i=0
for child in b:
    nom = child[0].replace(' data-v-0e629720="">','')#get BONO nombre
    #print(nom)
    bonoARSNom.insert(i,nom)
    i+=1

a = re.findall('<span data-v-0e629720((.|\s)+?)</span>',str(divBonosARS))
bonoARSPre=[]
i=0
for child in a:
    precio = child[0].replace('="">','')
    precio = precio.replace('.','')
    precio = precio.replace(',','.')
    #print(precio)
    if i%4==0:
        bonoARSPre.insert(i,precio)#get BONO precio 0,4,8,12,16,20,24
    i+=1


#print(bonoARSNom)
#print(bonoARSPre)

bonoUSDNom_D =  [s.strip('D') for s in bonoUSDNom]

if len(bonoARSNom)>len(bonoUSDNom_D):
    for i,tick in enumerate(bonoARSNom):
        if tick!=bonoUSDNom_D[i]:
            #print(i +' '+ tick)
            break
    bonoARSNom.remove(tick)
    bonoARSPre.pop(i)
elif len(bonoARSNom)<len(bonoUSDNom_D):
    for i,tick in enumerate(bonoUSDNom_D):
        if tick!=bonoARSNom[i]:
            #print(i +' '+ tick)
            break
    bonoUSDNom.pop(i)
    bonoUSDPre.pop(i)


pesos = np.array(bonoARSPre,dtype='f')
dolar = np.array(bonoUSDPre,dtype='f')

#if np.count_nonzero(dolar)<np.count_nonzero(pesos):
#    bonoARSNom.remove(bonoARSNom[-1])
#    bonoARSPre.remove(bonoARSPre[-1])
#    pesos = np.delete(pesos,-1)

#if np.count_nonzero(pesos)<np.count_nonzero(dolar):
#    bonoUSDNom.remove(bonoUSDNom[-1])
#    bonoUSDPre.remove(bonoUSDPre[-1])
#    dolar = np.delete(dolar,-1)

#print(pesos/dolar)
cotizaMEP=np.zeros(np.count_nonzero(pesos))
if np.count_nonzero(pesos)==np.count_nonzero(dolar):
    cotizaMEP = pesos/dolar

bonos = {
    "nombreUSD":bonoUSDNom,
    "precioUSD":bonoUSDPre,
    "nombreARS":bonoARSNom,
    "precioARS":bonoARSPre,
    "compraMEP":cotizaMEP.tolist()
}


bonosDF = pd.DataFrame(bonos)
print(bonosDF)
print(bonosDF[bonosDF['compraMEP']==bonosDF['compraMEP'].min()])
sys.exit()

#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Kütüphaneleri tanımladık
import requests
from bs4 import BeautifulSoup
import numpy as np
linkler = []
fiyatlistesi = []
deger = []
ozellikler = []

#Özelliklerin çekilmesi
for i in range(1,25):
        url = "https://www.trendyol.com/ayakkabi?pi=" + str(i)
        r = requests.get(url)
        sr1 = BeautifulSoup(r.content,"lxml") #İstek yapılan sayfanın içeriğinin çekilmesi
        
        fiyatlar = sr1.find_all("div",attrs={"class":"prc-box-sllng"})  
        for fiyat in fiyatlar:
            fiyatlistesi.append(fiyat.text)        
        ayakkabilar = sr1.find_all("div",attrs={"class":"p-card-chldrn-cntnr"})#Tüm verilerin bulunması
        for ayakkabi in ayakkabilar:
            ayakkabi_url = "https://www.trendyol.com/"+ayakkabi.a.get("href")#Verilerin linklerinin bulunması
            linkler.append(ayakkabi_url)#Linklerin kaydedilmesi           
            re_tel = requests.get(ayakkabi_url)#Bulunan linke tekrar istek atılması
            link_ayakkabi = BeautifulSoup(re_tel.content,"lxml")#Veri içeriğinin çekilmesi          
            ayakkabiozellikler = link_ayakkabi.find_all("div",attrs={"class":"item-key"})
            for ayakkabioz in ayakkabiozellikler:
                ozellikler.append(ayakkabioz.text)           
            ayakkabioz_deger = link_ayakkabi.find_all("div",attrs={"class":"item-value"})
            for ayakkabiozdeg in ayakkabioz_deger:
                deger.append(ayakkabiozdeg.text)
#veri setini doldurma
import pandas as pd
df = pd.DataFrame()
columns = np.array(ozellikler)
columns = np.unique(columns)
df = pd.DataFrame(columns = columns)
df["Fiyat"] = fiyat_liste
df["Link"] = links
for i in range(0,575):
    url = df['Link'].loc[i]
    r = requests.get(url)
    sr2 = BeautifulSoup(r.content,"lxml")
    ozellik = sr2.find_all("div",attrs={"class":"prop-item"})
    for ozel in ozellik:
        _isim = ozel.find("div",attrs={"class":"item-key"}).text
        _deger = ozel.find("div",attrs={"class":"item-value"}).text
        print(_isim+_deger)
        df[_isim].loc[i] = deger  

df.to_excel('verinin_ilk_hali.xlsx', engine='xlsxwriter')#veriyi excell dosyasına yazdırma

#veri ön işleme
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(
    missing_values=np.nan,
    strategy='most_frequent',
    fill_value=None,
    verbose=0,
    copy=True,add_indicator=False,)
imputer.fit(df.loc[:,:])
df.loc[:,:] = imputer.transform(df.loc[:,:])
       
df.to_excel('islenmis_hali.xlsx', engine='xlsxwriter')#verinin işlenmiş halini excell dosyasına yazdırma


# In[ ]:





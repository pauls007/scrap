#!/usr/bin/env python
# coding: utf-8

# In[9]:


import re
import pandas as pd
import requests
#import urllib.request
#import time
import json

import filefolders as ff

from bs4 import BeautifulSoup

r = requests.get('https://www.arduinothai.com/category/2/arduino-compatible-board')
s = BeautifulSoup(r.text, 'lxml')

productDetail = s.find_all('div',class_='productDetail')


ids=[]
Productname=[]
Productprice=[]
OldProductPrice=[]
CategoryProduct=[]
ListOfProduct =[]


for x in productDetail:
   #Scrape ProductID
    id1 = x.find('span','code').get_text(strip=True)
    pattren = r'[A-Z]{2}\d{5}|\d{5}|....\d{5}'
    regex = re.compile(pattren)
    result = regex.findall(id1)  
    ids.append(result)
    
   #Scrape ProductName
    ProName = x.find('div','product_name').get_text(strip=True)
    Productname.append(ProName)
    
   #Scrape ProductPriceCurrent
    ProPrice = x.find('div','product_price has_currency_unit').get_text(strip=True)
    Productprice.append(ProPrice)

   #Scrape OldProductPrice 
    OldProPrice = x.find('div','product_price_old has_currency_unit')
    OldProductPrice.append(OldProPrice)
   #print(type(OldProPrice))
    
   #Scrape CategoryProduct
    ProductDetail = x.find('a').get("gaeepd")
    ProductCategory_jsonData=json.loads(ProductDetail)["category"]
   # Data_Raw = ProductCategory_jsonData["category"]
   # print(ProName ,ProPrice,OldProPrice,Data_Raw)
    #print(ProductCategory_jsonData)
    CategoryProduct.append(ProductCategory_jsonData)

                
    ListOfProduct.append((result,ProName,ProPrice,OldProPrice,ProductCategory_jsonData))

data_df = pd.DataFrame({
    'ProductID': ids,
    'ProdcutName':Productname,
    'Productprice':Productprice,
    'OldProductPrice': OldProductPrice,
    'Category':CategoryProduct
})

df=pd.DataFrame(ListOfProduct, columns=['รหัสสินค้า', 'ชื่อสินค้า','ราคาขายปัจจุบัน','ราคาเดิมก่อนลด','ชนิด'])
pd.set_option('display.max_colwidth', 1)
df.to_csv('arduino.csv', index=False, encoding='utf-8')

arduino=pd.read_csv('arduino.csv')
arduino

df[0:]


# In[ ]:





# In[ ]:





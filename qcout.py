# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import re
import pandas as pd
import requests
import json
import time
import datetime
import numpy as np
import os
import filefolders as ff

from bs4 import BeautifulSoup
from requests import get
from time import sleep
from datetime import datetime

'''การกำหนดค่า URL ที่เราต้องการจะ Scraper ข้อมูล'''
URL = 'https://www.arduinothai.com/category/90/สินค้าราคาพิเศษ-หลุดqc'
Request = requests.get(URL)
soups = BeautifulSoup(Request.text, 'lxml')

''' เป็นการหาจำนวนหน้าของเพจ '''
Count_Next_Pages = soups.find_all('span','tsk-all')[-1].extract()
TotalProduct = float(str(Count_Next_Pages.text))

TotalProductPerPage = 40
TotalPages = (round(TotalProduct/TotalProductPerPage))

AllProduct = soups.find_all('div',class_='productDetail')
TypeProduct = soups.find('h2',class_='headerText').text

ProductIDAll=[]
Productname=[]
Productprice=[]
OldProductPrice=[]
CategoryProduct=[]
LinkProduct =[]
StockOfProduct=[]
ListOfProduct =[]

Total_Page = np.arange(1,TotalPages,1)  #เป็นการ Set การ Load จำนวนหน้าของแต่ละเพจที่เราดึง

'''for AllPage in Total_Page: #เป็นการวนลูปตามจำนวนหน้าที่เว็บมี'''
 #print(AllPage)

count = 0
for i in range(int(TotalPages)):
    count+=1
    i = 'https://www.arduinothai.com/category/90/สินค้าราคาพิเศษ-หลุดqc?tskp='+str(count)
    print(i)
    Request_Data = requests.get(i)
    Soups_Data = BeautifulSoup(Request_Data.text, 'lxml')
    AllProduct = Soups_Data.find_all('div',class_='productDetail')

for x in AllProduct:
    
     AllProductDeatil = x.find('a').get("gaeepd") #เป็นการดึงค่าของตัวแปรที่ชื่อว่า gaeepd ซึ่งอยู่ใน tag <a>
     IDProductLink = json.loads(AllProductDeatil)["id"]  #ดึงค่าที่เป็น id จาก gaeepd ซึ่งอยู่ใน tag <a> เพื่อใช้ในการดึงข้อมูลสินค้าแต่ละตัว
       
    #Scrape ProductID
     ProductID = x.find('span','code').get_text(strip=True)
     pattren = r'[A-Z]{2}\d{5}|\d{5}|....\d{5}'          #Regex สำหรับการจัดการรหัสสินค้า
     regex = re.compile(pattren)
     ProDuctIDResult = regex.findall(ProductID)  
     ProductIDStr = ff.ConvertListToStr(ProDuctIDResult)
     ProductIDAll.append(ProductIDStr)   

    #Scrape Link URL
     Link_URL = x.find('a').get("href")
     LinkProduct.append(Link_URL)
     #type(Link_URL)             
            
    #Scrape ProductName
     NameOfProduct = json.loads(AllProductDeatil)["name"]
     Productname.append(NameOfProduct)  
        
    #Scrape ProductPriceCurrent    
     PriceOfProduct = json.loads(AllProductDeatil)["price"]
     Productprice.append(PriceOfProduct) 

    #Scrape OldProductPrice         
     OldProPricesList = x.find('div','product_price_old has_currency_unit')
     OldProPricesEmp = ff.ConvertNoneToEmp(OldProPricesList)
     OldProPricesStr =  ff.ConvertListToStr(OldProPricesEmp)
     OldProductPrice.append(OldProPricesStr) 
        
   #Scrape CategoryProduct
     ProductCategory_jsonData=json.loads(AllProductDeatil)["category"]
     CategoryProduct.append(ProductCategory_jsonData) 
   
   #Scrape Stock    
     URL_Prefix =requests.get('https://www.arduinothai.com/product/'+str(IDProductLink))
     SoupStock = BeautifulSoup(URL_Prefix.text, 'lxml')   
     ChkStock = SoupStock.find('span', class_='num').text
     StockOfProduct.append(ChkStock)
   
     if((ProductCategory_jsonData==('สินค้าราคาพิเศษ หลุดQC'))):

         ListOfProduct.append((ProductIDStr, NameOfProduct, PriceOfProduct, OldProPricesStr, ChkStock, Link_URL, ProductCategory_jsonData))
        
         data_df = pd.DataFrame({
                'ProductID': ProductIDAll,
                'ProdcutName':Productname,
                'Productprice':Productprice,
                'OldProductPrice': OldProductPrice,
                'StockOfProduct': StockOfProduct,
                'Link': LinkProduct,
                'Category':CategoryProduct
         })
            
         df=pd.DataFrame(ListOfProduct, columns=['รหัสสินค้า', 'ชื่อสินค้า','ราคาขายปัจจุบัน','ราคาเดิมก่อนลด','สินค้าคงเหลือ','Link','ชนิด'])
         pd.set_option('display.max_rows', df.shape[0]+1)

df1 = df.copy()
        
names = "qcout_"        
ff.modify_folder(names,df1)
   
df
import re
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from requests import get
import numpy as np
from time import sleep
from random import randint
from datetime import datetime
import filefolders as ff
from urllib.request import urlopen 
from urllib.error import HTTPError 

'''การกำหนดค่า URL ที่เราต้องการจะ Scraper ข้อมูล'''
URL = 'https://www.arduinothai.com/category/157/microbit'
TotalPages = ff.geturl(URL)
print('Total: ',TotalPages)

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
 
count = 0
for i in range(int(TotalPages)):
    count+=1
    i = 'https://www.arduinothai.com/category/157/microbit?tskp='+str(count)
    url_name = urlopen(URL)
#            Request = requests.get(URL)
    soups = BeautifulSoup(url_name.read(), 'lxml')
    AllProduct = soups.find_all('div',class_='productDetail')

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
     URL_Prefix = urlopen('https://www.arduinothai.com/product/'+str(IDProductLink))
     SoupStock = BeautifulSoup(URL_Prefix.read(), 'lxml') 
     ChkStock = SoupStock.find('span', class_='num').text
     StockOfProduct.append(ChkStock)
   
     if((ProductCategory_jsonData==('บอร์ด')) or (ProductCategory_jsonData==('หุ่นยนต์')) or (ProductCategory_jsonData==('อุปกรณ์เสริม')) or (ProductCategory_jsonData==('Case')) ):

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
   
names = "Microbit"
ff.modify_folder(names,df1)    
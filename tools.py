#!/usr/bin/env python
# coding: utf-8

# In[31]:


import re
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import filefolders as ff
#from time import sleep
#from random import randint

'''--------------------------------------- เลือกรูปแบบในการแสดงข้อมูล--------------------------------------------------------'''
'''ข้อมูล 1 หน้า'''
#Request = requests.get('https://www.arduinothai.com/category/157/microbit')
#Request = requests.get('https://www.arduinothai.com/category/5/sensor-modules-shield')
'''ข้อมูล 2 หน้า'''
#Request = requests.get('https://www.arduinothai.com/category/2/arduino-compatible-board')
#Request = requests.get('https://www.arduinothai.com/category/32/%E0%B8%AD%E0%B8%B8%E0%B8%9B%E0%B8%81%E0%B8%A3%E0%B8%93%E0%B9%8C%E0%B8%AB%E0%B8%B8%E0%B9%88%E0%B8%99%E0%B8%A2%E0%B8%99%E0%B8%95%E0%B9%8C-robot-part')
'''ข้อมูล 6 หน้า'''
#Request = requests.get('https://www.arduinothai.com/category/54/%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A%E0%B9%84%E0%B8%9F%E0%B9%80%E0%B8%A5%E0%B8%B5%E0%B9%89%E0%B8%A2%E0%B8%87')
'''ข้อมูล 9 หน้า'''
#Request = requests.get('https://www.arduinothai.com/category/105/diy-%E0%B8%A1%E0%B8%B5%E0%B8%84%E0%B9%88%E0%B8%B2%E0%B8%88%E0%B8%B1%E0%B8%94%E0%B8%AA%E0%B9%88%E0%B8%87-%E0%B8%AA%E0%B8%B4%E0%B8%99%E0%B8%84%E0%B9%89%E0%B8%B2%E0%B8%A3%E0%B8%AB%E0%B8%B1%E0%B8%AAat30xxx')
'''------------------------------------------------------------------------------------------------------------------------'''


'''การกำหนดค่า URL ที่เราต้องการจะ Scraper ข้อมูล'''
URL_Page = 'https://www.arduinothai.com/category/12/tool-เครื่องมือ'
Request_Page = requests.get(URL_Page)
Soups_Page = BeautifulSoup(Request_Page.text, 'lxml')

''' เป็นการหาจำนวนหน้าของเพจ '''
Count_Next_Pages = Soups_Page.find_all('span','tsk-all')[-1].extract()
TotalProduct = float(str(Count_Next_Pages.text))
TotalProductPerPage = 40
TotalPages = round(TotalProduct/TotalProductPerPage)

Pages=[]
Counts = 1
while Counts <= TotalPages:
    Pages.append(Counts)
    Counts = Counts + 1

#AllProduct = soups.find_all('div',class_='productDetail')
#TypeProduct = soups.find('h2',class_='headerText').text

ProductIDAll=[]
Productname=[]
Productprice=[]
OldProductPrice=[]
CategoryProduct=[]
LinkProduct =[]
StockOfProduct=[]
ListOfProduct =[]


for i in Pages:
    
            URL = 'https://www.arduinothai.com/category/12/tool-เครื่องมือ?tskp='+str(i)
            Request = requests.get(URL)
            soups = BeautifulSoup(Request.text, 'lxml')
            AllProduct = soups.find_all('div',class_='productDetail')
    
            def ConvertNoneToEmp(ValueNone):
                if ValueNone is None:
                    return'-'
                else:
                    return ValueNone

            def ConvertListToStr(ValueList):
                ConvertValueStr =' '.join([str(elem) for elem in ValueList])
                return ConvertValueStr


            for x in AllProduct:


                 AllProductDeatil = x.find('a').get("gaeepd")
                 IDProductLink = json.loads(AllProductDeatil)["id"]        

                #Scrape ProductID
                 ProductID = x.find('span','code').get_text(strip=True)
                 pattren = r'[A-Z]{2}\d{5}|\d{5}|....\d{5}'
                 regex = re.compile(pattren)
                 ProDuctIDResult = regex.findall(ProductID)  
                 ProductIDStr = ConvertListToStr(ProDuctIDResult)
                 ProductIDAll.append(ProductIDStr)  

                #Scrape Link URL
                 Link_URL = x.find('a').get("href")
                 LinkProduct.append(Link_URL)
                 type(Link_URL)             

                #Scrape ProductName
                 NameOfProduct = json.loads(AllProductDeatil)["name"]
                 Productname.append(NameOfProduct)  


                #Scrape ProductPriceCurrent    
                 PriceOfProduct = json.loads(AllProductDeatil)["price"]
                 Productprice.append(PriceOfProduct) 

                #Scrape OldProductPrice         
                 OldProPricesList = x.find('div','product_price_old has_currency_unit')
                 OldProPricesEmp = ConvertNoneToEmp(OldProPricesList)   
                 OldProPricesStr = ConvertListToStr(OldProPricesEmp)
                 OldProductPrice.append(OldProPricesStr) 

               #Scrape CategoryProduct
                 ProductCategory_jsonData=json.loads(AllProductDeatil)["category"]
                 CategoryProduct.append(ProductCategory_jsonData) 

               #Scrape Stock    
                 URL_Prefix =requests.get('https://www.arduinothai.com/product/'+str(IDProductLink))
                 SoupStock = BeautifulSoup(URL_Prefix.text, 'lxml')           
                 Stocks = SoupStock.find('span', class_='num')
                 ChkStock = int(str(Stocks.text))
                 StockOfProduct.append(ChkStock)

                 if((ProductCategory_jsonData==('Tool/เครื่องมือ'))):

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
        
names = "Tool_"        
ff.modify_folder(names,df1)
   
print(df)
import re
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from requests import get
import filefolders as ff
from urllib.request import urlopen 
from urllib.error import HTTPError 
#from time import sleep
#from random import randint

'''การกำหนดค่า URL ที่เราต้องการจะ Scraper ข้อมูล'''
URL_Page = 'https://www.arduinothai.com/category/28/%E0%B9%80%E0%B8%8B%E0%B8%99%E0%B9%80%E0%B8%8B%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%AA%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B9%81%E0%B8%A7%E0%B8%94%E0%B8%A5%E0%B9%89%E0%B8%AD%E0%B8%A1'

TotalPages = ff.geturl(URL_Page)
print('Total: ',TotalPages)

Pages=[]
Counts = 1
while Counts <= TotalPages:
    Pages.append(Counts)
    Counts = Counts + 1

ProductIDAll=[]
Productname=[]
Productprice=[]
OldProductPrice=[]
CategoryProduct=[]
LinkProduct =[]
StockOfProduct=[]
ListOfProduct =[]


for i in Pages:
    
            URL = 'https://www.arduinothai.com/category/28/%E0%B9%80%E0%B8%8B%E0%B8%99%E0%B9%80%E0%B8%8B%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%AA%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B9%81%E0%B8%A7%E0%B8%94%E0%B8%A5%E0%B9%89%E0%B8%AD%E0%B8%A1?tskp='+str(i)
            url_name = urlopen(URL)
            soups = BeautifulSoup(url_name.read(), 'lxml')
            AllProduct = soups.find_all('div',class_='productDetail')
    
            for x in AllProduct:


                 AllProductDeatil = x.find('a').get("gaeepd")
                 IDProductLink = json.loads(AllProductDeatil)["id"]        

                #Scrape ProductID
                 ProductID = x.find('span','code').get_text(strip=True)
                 pattren = r'[A-Z]{2}\d{5}|\d{5}|....\d{5}'
                 regex = re.compile(pattren)
                 ProDuctIDResult = regex.findall(ProductID)  
                 ProductIDStr = ff.ConvertListToStr(ProDuctIDResult)
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

                 if((ProductCategory_jsonData==('วัดอุณหภูมิ / วัดความชื้น(Temp./Humi.)')) or (ProductCategory_jsonData==('วัดแสง / UV (Light / UV)')) 
                     or (ProductCategory_jsonData==('ตรวจจับเปลวไฟ')) or (ProductCategory_jsonData==('โมดูลแปลงสัญญาณ')) or (ProductCategory_jsonData==('วัดฝน/วัดความชื้นในดิน/วัดน้ำ (Rain / Soil / Water)')) 
                     or (ProductCategory_jsonData==('ความเคลื่อนไหว / ความสั่น / เสียง')) or (ProductCategory_jsonData==('วัดแรงดันอากาศ')) or (ProductCategory_jsonData==('Hall Magnetic')) 
                     or (ProductCategory_jsonData==('Ph / Ec / TDS / Oxygen Sensor')) or (ProductCategory_jsonData==('วัดสภาพอากาศ')) or (ProductCategory_jsonData==('Thermostat'))):

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
        
names = "เซนเซอร์วัดสภาพแวดล้อม_"        
ff.modify_folder(names,df1)
   
#print(df)
#print('sss')
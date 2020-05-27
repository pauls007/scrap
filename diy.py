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


'''การกำหนดค่า URL ที่เราต้องการจะ Scraper ข้อมูล'''
URL_Page = 'https://www.arduinothai.com/category/105/diy-มีค่าจัดส่ง-สินค้ารหัสat30xxx'
Request_Page = requests.get(URL_Page)
Soups_Page = BeautifulSoup(Request_Page.text, 'lxml')

''' เป็นการหาจำนวนหน้าของเพจ '''
Count_Next_Pages = Soups_Page.find_all('span','tsk-all')
TotalProduct = float(Count_Next_Pages[1].text)
TotalProductPerPage = 40
TotalPages = round(TotalProduct/TotalProductPerPage)
#print(TotalPages)
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
    
            URL = 'https://www.arduinothai.com/category/105/diy-มีค่าจัดส่ง-สินค้ารหัสat30xxx?tskp='+str(i)
            Request = requests.get(URL)
            soups = BeautifulSoup(Request.text, 'lxml')
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
                 OldProPricesStr = ff.ConvertListToStr(OldProPricesEmp)
                 OldProductPrice.append(OldProPricesStr) 

               #Scrape CategoryProduct
                 ProductCategory_jsonData=json.loads(AllProductDeatil)["category"]
                 CategoryProduct.append(ProductCategory_jsonData) 

               #Scrape Stock    
                 URL_Prefix =requests.get('https://www.arduinothai.com/product/'+str(IDProductLink))
                 SoupStock = BeautifulSoup(URL_Prefix.text, 'lxml')           
                 ChkStock = SoupStock.find('span', class_='num')
                 StockOfProduct.append(ChkStock)

                 if((ProductCategory_jsonData==('แหล่งจ่ายไฟ/Switching')) or (ProductCategory_jsonData==('อุปกรณ์ 3D Printer')) 
                     or (ProductCategory_jsonData==('Pulley/Belt/พูเล่ย์/สายพาน/โซ่')) or (ProductCategory_jsonData==('คัปปิ้ง/coupling')) 
                     or (ProductCategory_jsonData==('มัลติมิเตอร์')) or (ProductCategory_jsonData==('แม่เหล็กนีโอไดเมียม')) 
                     or (ProductCategory_jsonData==('อลูมิเนียมโปรไฟล์')) or (ProductCategory_jsonData==('อุปกรณ์นิวเมติกส์')) or (ProductCategory_jsonData==('ลูกปืนสไลด์/ตุ๊กตาแบริ่ง'))
                     or (ProductCategory_jsonData==('Nut / Bolt'))  or (ProductCategory_jsonData==('เครื่อง CNC และอุปกรณ์ CNC'))  or (ProductCategory_jsonData==('อุปกรณ์ RC'))
                     or (ProductCategory_jsonData==('เครื่อง 3D Printer')) or (ProductCategory_jsonData==('อุปกรณ์บัดกรี')) or (ProductCategory_jsonData==('เพลา'))
                     or (ProductCategory_jsonData==('ล้อ')) or (ProductCategory_jsonData==('Solar Cell ( โซล่า เซลล์ )'))  ):

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

names = "DIY"
ff.modify_folder(names,df1)

#print(df)
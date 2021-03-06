
import os, sys, stat
import socket

from bs4 import BeautifulSoup 
from urllib.request import urlopen 
from urllib.error import HTTPError 
from tkinter import messagebox
from datetime import datetime

def geturl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None

    try:
            Soups = BeautifulSoup(html.read(), 'lxml')
            Count_Next_Pages = Soups.find_all('span','tsk-all')
            TotalProduct = float(Count_Next_Pages[1].text)
            TotalProductPerPage = 40
            AllPages = round(TotalProduct/TotalProductPerPage)
            
            #title = soups.body.h3
    except AttributeError as e:
            return None
    return AllPages

def modify_folder(namesfolder,data):              
    todays = datetime.now()
    main_folder = todays.strftime('%d-%m-%Y')
    name_folder = namesfolder+'_'+todays.strftime('%d-%m-%Y')
    comname = socket.gethostname()

    if (comname == "DESKTOP-BK4KDMS"):
        parent_dir = "D:/Scrapy/" 
    else:
        parent_dir = "E:/Scrapy/"
    try:      
     #Set path
     pathmain = os.path.join(parent_dir,main_folder)
     path = os.path.join(pathmain,name_folder)
     os.mkdir(path)
     print(pathmain)

     datestring = datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M-%S')
     files = namesfolder+'_'
     filename = files.format(datestring)
     f = open(filename, 'w') 
     data.to_csv(path+'/'+filename+'.csv', 
                header=True, 
                index=True, 
                encoding='utf-8-sig') 

     msg = ("Directory '% s' created" % name_folder)
     messagebox.showinfo("สามารถสร้าง Folder ได้แล้ว;", msg)     
     
     print("Directory '% s' created" % name_folder)

    except OSError as error:
     
     msg = ("Directory " , name_folder ,  " already exists")
     messagebox.showinfo("ไม่สามารถสร้าง Folder ได้จร้าา", msg)   
     
     print("Directory " , name_folder ,  " already exists")  
 #    print(path)
     print(error)

    return

def ConvertNoneToEmp(ValueNone):
    if ValueNone is None:
        return'-'
    else:
        return ValueNone

    return

def ConvertListToStr(ValueList):
        ConvertValueStr =' '.join([str(elem) for elem in ValueList])
        return ConvertValueStr

#print('sss')
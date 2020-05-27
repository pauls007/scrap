
import os, sys, stat
import socket

from datetime import datetime

#def modify_folder(namesfolder,data):              
todays = datetime.now()
main_folder = todays.strftime('%d-%m-%Y')
#name_folder = namesfolder+'_'+todays.strftime('%d-%m-%Y')
comname = socket.gethostname()

if (comname == "DESKTOP-BK4KDMS"):
    parent_dir = "D:/Scrapy/" 
else:
    parent_dir = "E:/Scrapy/"
try:      
     #Set path
     path = os.path.join(parent_dir,main_folder)
     os.mkdir(path)
     print(path)
except OSError as error:
     print("Directory " , main_folder ,  " already exists")  
 #    print(path)
     print(error)

#    return
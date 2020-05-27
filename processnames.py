#!/usr/bin/env python
# coding: utf-8

# In[30]:


# Python program to explain os.mkdir() method 
	
# importing os module 
import os 
import datetime
from datetime import datetime
import socket
	
# Directory 

def process_data(name_file_folder,data):

    today = datetime.now()
    names = name_file_folder
    directory = names+today.strftime('%d-%m-%Y')


    # Parent Directory path 
    namehost = socket.gethostname()

    if (namehost == 'DESKTOP-M4LTLO4'):
        print("Acer")
        parent_dir = "E:/Scrapy/"
    else:
        print('HP')


    # Path 
    path = os.path.join(parent_dir, directory) 

    # Create the directory 
    # 'GeeksForGeeks' in 
    # '/home / User / Documents' 
    try:
            os.mkdir(path)                               
            print("Directory '% s' created" % directory) 
    except FileExistsError:
            print("Directory " , directory ,  " already exists")    

    # if directory / file that 
    # is to be created already 
    # exists then 'FileExistsError' 
    # will be raised by os.mkdir() method 

    # Similarly, if the specified path 
    # is invalid 'FileNotFoundError' Error 
    # will be raised 


# In[ ]:





# In[ ]:





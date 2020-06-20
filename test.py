#import re
#import pandas as pd
#import requests
#import json
#from bs4 import BeautifulSoup
#from requests import get
#from datetime import datetime
#import ssl

#URL_Page = 'https://www.psu.ac.th/th/index.php'
#Request_Page = requests.get(URL_Page)
#Soups_Page = BeautifulSoup(Request_Page.text, 'lxml')
#print(type(Soups_Page))

#URL_Page = 'https://www.arduinothai.com/category/54/ระบบไฟเลี้ยง'
#Request_Page = requests.get(URL_Page)
#Soups_Page = BeautifulSoup(Request_Page, 'lxml')
#print(type(Soups_Page))

#import urllib3.contrib.pyopenssl
from urllib.request import urlopen 
from urllib.error import HTTPError 
from bs4 import BeautifulSoup 
import json

def gettitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None

    try:
            soups = BeautifulSoup(html.read(), 'lxml')
            title = soups.body.h3
    except AttributeError as e:
            return None
    return title

title_name = 'https://www.arduinothai.com/category/54/%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A%E0%B9%84%E0%B8%9F%E0%B9%80%E0%B8%A5%E0%B8%B5%E0%B9%89%E0%B8%A2%E0%B8%87'

#title_name_encode = (urllib.parse.unquote(title_name))
#print(type(title_name))

title =  gettitle(title_name)
if title == None:
    print('Title could not be found')
else:
    print(title)
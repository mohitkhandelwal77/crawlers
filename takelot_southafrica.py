# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from datetime import date, datetime
import csv
import pandas as pd
import time
import json
import requests
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from tqdm.notebook import tqdm
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

headers = {
    'authority': 'api.takealot.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"k0Zm9FeDntu9R44BSnto/A"',
    'origin': 'https://www.takealot.com',
    'referer': 'https://www.takealot.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

params = {
    'platform': 'desktop',
    'display_credit': 'true',
}



#input file
inputlist = pd.read_excel(r"C:/Users/mohit/Documents/Rhythm Feature mapping/takealot_input.xlsx")
inputlist
inputlist.drop_duplicates(inplace=True)
inputlist.dropna(inplace = True)
asinlist = list(inputlist['Asin'].unique())
asinlist
urllist = list(inputlist['Url'].unique())

#creating empty dataframe
df = pd.DataFrame(columns=['Product URL','Product ID','Product Title','Brand','Asin','Image URL',
                           'No. of Image','Model Number','Description','Category','Average Rating','Review Count','Price','Availability'])



for val in tqdm(range(0,50)):
    
    i=asinlist[val]
    url = urllist[val]
    print(i)
    response = requests.get(f'https://api.takealot.com/rest/v-1-10-0/product-details/{i}', params=params, headers=headers)


    res_text=response.text
    
    productpage= json.loads(res_text)
    
    try:
        summary = productpage['enhanced_ecommerce_detail']['ecommerce']['detail']['products']
        # Fetch the desired information
        first_product = summary[0]  # Access the first dictionary in the list
        
        try:
            Asin = first_product.get('id', None)
        except KeyError:
            Asin = None
        
        try:
            category = first_product.get('category', None)
        except KeyError:
            category = None
        
        try:
            brand = first_product.get('brand', None)
        except KeyError:
            brand = None
        
        try:
            price = first_product.get('price', None)
        except KeyError:
            price = None
        
        try:
            product_title = first_product.get('name', None)
        except KeyError:
            product_title = None
    except:
        pass
    
    try:
        price = productpage['buybox'].get('pretty_price', None)
    except KeyError:
        price = None
    
    try:
        description = productpage['description'].get('html', None)
    except KeyError:
        description = None
    
    try:
        product_title = productpage['core'].get('title', None)
    except KeyError:
        product_title = None
    
    try:
        modelnumber = productpage['core'].get('subtitle', None)
        if modelnumber:
            parts = modelnumber.split(':')
            if len(parts) >= 2:
                modelnumber = parts[1].strip()
    except KeyError:
        modelnumber = None
    
    try:
        productid = productpage['buybox'].get('product_id', None)
    except KeyError:
        productid = None
    
    try:
        brand = productpage['core'].get('brand', None)
    except KeyError:
        brand = None
    
    try:
        Star_Rating = productpage['reviews'].get('star_rating', None)
    except KeyError:
        Star_Rating = None
    
    try:
        Reviewcount = productpage['reviews'].get('count', None)
    except KeyError:
        Reviewcount = None
    
    try:
        Availability = productpage['stock_availability'].get('status', None)
    except KeyError:
        Availability = None
    
    try:
        imageurl = productpage['gallery'].get('images', [])
        for z in range(len(imageurl)):
            imageurl[z] = imageurl[z].replace("{size}", "zoom")
        Numberofimages = len(imageurl)
    except KeyError:
        imageurl = []
        Numberofimages = 0
      # Append the extracted information as a new row to the DataFrame
    data = {'Product URL':url,'Product ID':productid,'Product Title':product_title,'Brand': brand,
            'Asin':Asin,'Image URL':imageurl,'No. of Image':Numberofimages,'Model Number':modelnumber,'Description': description,
            'Average Rating': Star_Rating ,'Review Count': Reviewcount,'Price':price,
            'Availability':Availability}
    df = df.append(data, ignore_index=True)   
    
print(df)
print(val)
df.to_excel(r'C:/Users/mohit/Documents/Rhythm Feature mapping/takealotoutput2.xlsx')
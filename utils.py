'''
That file contain all file that utility
function (basic used)

Created by Napas Vinitnantharat
'''


import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  


WEBDRIVER_PATH = './chromedriver'
# office MAA-Warin , home ASUS

############################################################

def createDir_if_not_exist(path):
    """_
    This function create a folder if not exists
    
    Argument : path
        
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print('create new Dir',path)
        
############################################################
def createDriver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
        
def get_texthtml(url,driver):

    driver.get(url)
    text_html = driver.page_source
    print('get text html from url =',url)
    return text_html

def driver_quit(driver):
    driver.quit()
    
############################################################

def filter_stock(filename):
    """
    This function filter stock in csv that is not in
    
    Equity Securities (Main Board) or Equity Securities (GEM) or Investment Companies
    
    Argument : filename
             
    Return : New filename that already filter
    """
    try:
        df = pd.read_csv(filename,converters={"StockCode": str})
        df = df.loc[(df['Sub-Category'] == 'Equity Securities (Main Board)') \
                    | (df['Sub-Category'] == 'Equity Securities (GEM)') \
                    | (df['Sub-Category'] == 'Investment Companies') \
                    | (df['Sub-Category'] == 'Depositary Receipts') \
                    | (df['Category'] == 'Real Estate Investment Trusts')]
        df.to_csv('filter-' + filename, index=False)
        df.to_json('filter-' + filename + '.json')
        
        return 'filter-' + filename
    except:
        print('No such file or directory:',filename)
    
############################################################

def stock_in_csv(stockcode,filename):
    """
    This function check is stockcode in filecsv or not
    
    Argument : stockcode 
             : filename
             
    Return : True or False
    """
    df = pd.read_csv(filename)
    
    return (int(stockcode) in list(df['StockCode']))
    
############################################################

def setupFolder():
    createDir_if_not_exist('data/y')
    createDir_if_not_exist('data/q')
    createDir_if_not_exist('data/h')
    createDir_if_not_exist('data/u/y')
    createDir_if_not_exist('data/u/q')
    createDir_if_not_exist('data/u/h')
    
############################################################


def inttostr(num):
    if num < 10:
        return '0000' + str(num)
    elif num < 100:
        return '000' + str(num)
    elif num < 1000:
        return '00' + str(num)
    elif num < 10000:
        return '0' + str(num)
    else:
        return str(num)

if __name__ == '__main__':


    filter_stock('HK-CODE2.csv')
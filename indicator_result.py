from utils import *
from bs4 import BeautifulSoup 

BASE_URL = 'http://www.aastocks.com/en/stocks/quote/detail-quote.aspx?symbol='

OUTPUT_FILE = 'aastock_indicator.csv'

df_all_stock = pd.read_csv('filter-HK-CODE2.csv')


def get_indicator_result(symbol,driver):
    print('get data symbol:',symbol)
    html = get_texthtml(BASE_URL+ symbol,driver)
    
    
if __name__ == '__main__':
    driver = createDriver()
    '''
    for i in range(len(df_all_stock)):
        stockCode = df_all_stock.loc[i, "StockCode"]
        get_indicator_result(stockCode,driver)
    '''
    get_indicator_result('01600',driver)
    driver_quit(driver)
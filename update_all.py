
from utils import *
from v1_Update_result import *


df_all_stock = pd.read_csv('filter-HK-CODE2.csv')


def updateStock_(period,url,stock_file,driver):
    
    flag,aa_PL_date,df_PL_aa_stock = get_aa_stock(url,driver)
    print('\nStatus Flag =',flag,'aa_PL_date=',aa_PL_date)
    
    # No information in aa stock
    if flag == 'N':
        print('No information')
    else:
        
        if os.path.exists(stock_file):
        
            df_stock_file = pd.read_csv(stock_file,header=None)
            #find latest date in file csv 
            date_csv_file = df_stock_file.iloc[-1,0]

            #the file in y,q,h is already update
            if aa_PL_date == date_csv_file:
                print('\nNo update')
            else:
                print('file in y q h is not update')
                if period=='Q':
                    df_PL_aa_stock.to_csv('data/u/q/' + stockcode + 'PL-Q.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
                elif period=='H':
                    df_PL_aa_stock.to_csv('data/u/h/' + stockcode + 'PL-H.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
                elif period=='Y':
                    df_PL_aa_stock.to_csv('data/u/y/' + stockcode + 'PL-Y.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
                else:
                    print('########## ERR something')
                
        else:
            print('file csv in q,y,h is not exist')
            #create new file (latest record in aa stock PL website)
            if period=='Q':
                df_PL_aa_stock.to_csv('data/q/' + stockcode + 'PL-Q.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
            elif period=='H':
                df_PL_aa_stock.to_csv('data/h/' + stockcode + 'PL-H.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
            elif period=='Y':
                df_PL_aa_stock.to_csv('data/y/' + stockcode + 'PL-Y.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
            else:
                print('########## ERR something')


if __name__ == '__main__':

    driver = createDriver()

    for i in range(len(df_all_stock)):
        
        stockCode = df_all_stock.loc[i, "StockCode"]
        # period Y
        url_y = BASE_PL_URL + stockCode 
        stock_file = 'data/y/'+stockCode+'PL-Y.csv'
        updateStock_('Y',url_y,stock_file,driver)
        # period Q
        url_q = BASE_PL_URL  + stockCode + '&period=0'
        stock_file = 'data/q/'+stockCode+'PL-Q.csv'
        updateStock_('Q',url_q,stock_file,driver)
        # period H
        url_h = BASE_PL_URL  + stockCode + '&period=2'
        stock_file = 'data/h/'+stockCode+'PL-H.csv'
        updateStock_('H',url_h,stock_file,driver)
        
        
    merge_file()
    
    driver_quit(driver)
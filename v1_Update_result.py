
'''


Update jun 10 2022

Created By Napas Vinitnantharat

'''
from utils import *
import sys


###########################################################################
# list of allstock in HKEX
df_code = pd.read_csv('HK-CODE2.csv',converters={"StockCode": str})
df_code.set_index('StockCode')

# parameter 
update_month="8"
update_year="2022"
data = sys.argv
print(data)

if len(data) > 2 :
    
    update_month = str(data[1])
    update_year = str(data[2])




BASE_PL_URL = 'http://www.aastocks.com/en/stocks/analysis/company-fundamental/profit-loss?symbol='
CALENDAR_DIR = 'data/cal/' + update_year + '/' + update_month 
ALL_HK_STOCK_FILE = 'filter-HK-CODE2.csv'


new_update = 0
not_update = 0
new_file = 0



###########################################################################

def get_aa_stock(url,driver):
    status = 'A'
    date = ''
    text_html = get_texthtml(url,driver)
    table_MN = pd.read_html(text_html)
    if len(table_MN) < 10:
        status = 'N'
        df_all = '' # temp dataframe 
    for i in range(len(table_MN)):
    
        df = table_MN[i]
        if df[0][0] == "No related information.":
            print('No related information.')
            status = 'N'
            df_all = '' # temp dataframe 
            
        if df[0][0] == "Closing Date":
            df_top = table_MN[i] #top p&L
            df_bottom = table_MN[i+1] #botoom p&L
            df_all = pd.concat([df_top,df_bottom])
            del df_all[6] # delete trend 
            
            # case where record is not full 6 record is going to be nan
            # http://www.aastocks.com/en/stocks/analysis/company-fundamental/profit-loss?symbol=03347&period=0
            if df_all[df_all.columns[-1]].isna().any():
                while df_all[df_all.columns[-1]].isna().any():
                    df_all = df_all.drop(df_all.columns[-1],axis=1)
                
            
            df_all = df_all.transpose()
            del df_all[2] # delete Created with Highcharts
            date = df_all.iloc[df_all.shape[0]-1,0] #date in aa stock website P&L
        
        
    return status,date,df_all;

###########################################################################



def getperiodCodeInfo(periodCode,StockCode):
    if periodCode.find("ANN RES")!=-1 :
        period_ = "Y"
        url = BASE_PL_URL  + StockCode
        stock_file = 'data/y/'+StockCode+'PL-Y.csv'

    elif periodCode.find("RES")!=-1 and (periodCode.find("QTR")!=-1 or periodCode.find("9-MTH")!=-1 or periodCode.find("3-MTH")!=-1):
        period_="Q"
        url = BASE_PL_URL  + StockCode + '&period=0'
        stock_file='data/q/'+StockCode+'PL-Q.csv'
        # print(StockCode, periodCode)
    elif periodCode.find("RES")!=-1 and (periodCode.find("INT")!=-1  or periodCode.find("6-MTH")!=-1) and periodCode.find("ANN")==-1:
        period_ = "H"
        url = BASE_PL_URL  + StockCode + '&period=2'
        stock_file = 'data/h/'+StockCode+'PL-H.csv'
        # print(StockCode, periodCode)
    elif periodCode.find("RES")!=-1 and (periodCode.find("ANN")!=-1 or periodCode.find("ANN RES")!=-1 or periodCode.find("FIN RES")!=-1):
        period_ = "Y"
        url = BASE_PL_URL  + StockCode
        stock_file = 'data/y/'+StockCode+'PL-Y.csv'
    elif periodCode.find("RES/FIN")!=-1 :
        period_ = "Y"
        url = BASE_PL_URL  + StockCode
        stock_file = 'data/y/'+StockCode+'PL-Y.csv'

    else:
        print("period not found",periodCode)
        period_ = "Not found"
        url = "Not found"
        stock_file = "Not found"
        
    return period_, url, stock_file;


###########################################################################


def updateStock(stockcode,period,df_cal,driver):
    
    global new_update
    global not_update 
    global new_file 
    
    status = True
    print('#########################################')
    print("กำลังทำงานกับหุ้น: ",stockcode)
    # check if the stockcode is in the file csv or not        
    if stock_in_csv(stockcode,ALL_HK_STOCK_FILE) == False:
        print(stockcode,'is not in ',ALL_HK_STOCK_FILE)
        df_cal.loc[df_cal['Code'] == stockcode + '.HK','updateStatus'] = 'Not in filter-HK-CODE2.csv'
        return False
    
    # check if the stock is already update or not
    print(df_cal[df_cal['Code'] == stockcode + '.HK']['updateStatus'].values[0])
    if df_cal[df_cal['Code'] == stockcode + '.HK']['updateStatus'].values[0] == 'U':
        print(stockcode,'Has already update')
        return False
    
    print(period)
    # case special dividend
    if period.count("/") <2:
        print('Not a report case',period)
        return False
        
    # period_ Y Q H 
    period_, url, stock_file = getperiodCodeInfo(period,stockcode)
    print('period_ is ',period_, 'URL is ',url, 'stock_file is ',stock_file)
    
    # case special diviend or other case
    if period_== "Not found":
        return False
    
    # d2 get PL data and date record from aa stock 
    flag,aa_PL_date,df_PL_aa_stock = get_aa_stock(url,driver)
    print('\nStatus Flag =',flag,'aa_PL_date=',aa_PL_date)
    
    # No information in aa stock
    if flag == 'N':
        print('No information')
        df_cal.loc[df_cal['Code'] == stockcode + '.HK','updateStatus'] = 'No information'
        return False
        
    # d3 calendar date on aa stock annonuement calendar file
    aa_calendar_date = "20"+str(period[-3:-1])+"/"+str(period[-6:-4])
    print('\n\naa stock calendar date=',aa_calendar_date)
    
    chk_file_exist=os.path.exists(stock_file)
        
    # if the stock_file in folder Y Q H is exist
    if chk_file_exist:
        print('*******************')
        print('file csv in q,y,h exist',stock_file)
        print('*******************')
        df_stock_file = pd.read_csv(stock_file,header=None)
        
        #find latest date in file csv 
        date_csv_file = df_stock_file.iloc[-1,0]
        
        print('latest date in file csv is',date_csv_file,'aa stock PL date is ',aa_PL_date)
        
        # ข้อมูลเดิม updated ไม่ต้องทำการ download ไฟล์
        # if the date in file csv is equal to aa stock date mean the stock is already update
        if date_csv_file == aa_PL_date:
            print('ข้อมูลเดิม updated ไม่ต้องทำการ download ไฟล์')
            df_cal.loc[df_cal['Code'] == stockcode + '.HK','updateStatus'] = 'U'
            print(f'set {stockcode} as update U')
            
        #พบไฟล์ข้อมูลยังไม่ update และฐานข้อมูลใน aastocks ได้ update ข้อมูลแล้ว
        elif aa_calendar_date == aa_PL_date:
            print('พบไฟล์ข้อมูลยังไม่ update และฐานข้อมูลใน aastocks ได้ update ข้อมูลแล้ว')
            
            if period_=='Q':
                df_PL_aa_stock.to_csv('data/u/q/' + stockcode + 'PL-Q.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
            elif period_=='H':
                df_PL_aa_stock.to_csv('data/u/h/' + stockcode + 'PL-H.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
            elif period_=='Y':
                df_PL_aa_stock.to_csv('data/u/y/' + stockcode + 'PL-Y.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
            else:
                print('########## ERR something')
            
            
            
            df_cal.loc[df_cal['Code'] == stockcode + '.HK','updateStatus'] = 'U'
            print(f'set {stockcode} as update U')
            new_update = new_update + 1
        else:
            print("aastock ยังไม่ update ฐานข้อมูล")
            df_cal.loc[df_cal['Code'] == stockcode + '.HK','updateStatus'] = 'N'
            
    # if the stock_file is not in folder Y Q H is exist
    else:
        print('file csv in q,y,h is not exist')
        #create new file (latest record in aa stock PL website)
        if period_=='Q':
            df_PL_aa_stock.to_csv('data/q/' + stockcode + 'PL-Q.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
        elif period_=='H':
            df_PL_aa_stock.to_csv('data/h/' + stockcode + 'PL-H.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
        elif period_=='Y':
            df_PL_aa_stock.to_csv('data/y/' + stockcode + 'PL-Y.csv', mode='w', encoding='utf-8-sig', header=None, index=False)
        else:
            print('########## ERR something')
    
        print('aa calendar = ',aa_calendar_date,'aa PL date = ',aa_PL_date)
        
        if aa_calendar_date == aa_PL_date:
            # if the aa stock PL date website is the same as the aa stock calendar date website
            # set update the data in specify stockcode in calendar file when PL web is the same as the data in calendar
            new_file = new_file + 1 
            df_cal.loc[df_cal['Code'] == stockcode + '.HK','updateStatus'] = 'I'
            print(f'set {stockcode} as updateStatus I')
    print('#########################################')
    return status


#######################################################################
def merge_file():
    print('merge file')
    # merge file in folder q,y,h
    for period in ['y','q','h']:
        for file in os.listdir('data/u/' + period):
            df_old = pd.read_csv('data/'+ period +'/' + file,header=None)
            df_new = pd.read_csv('data/u/'+ period +'/' + file,header=None)
            
            #print(pd.concat([df_old,df_new]).drop_duplicates().reset_index(drop=True))
            df_final = pd.concat([df_old,df_new]).drop_duplicates() \
            .reset_index(drop=True)
            #print(df_final)
            #df_final.sort_values(by=[df_final.columns[0]],inplace=True)
            df_final.to_csv('data/'+ period +'/' + file, mode='w', encoding='utf-8-sig', header=None, index=False)

#######################################################################

if __name__ == '__main__':

    # run This first
    # filter_stock('HK-CODE2.csv')

    setupFolder()

    driver = createDriver()

    createDir_if_not_exist(CALENDAR_DIR)

    all_file = os.listdir(CALENDAR_DIR)

    all_file.sort()

    
    # for loop in folder year months
    for file in all_file:
        print('looking on file :',file)
        df_cal = pd.read_csv(CALENDAR_DIR+ '/' + file,index_col= False) # df calendar
        
        # for loop in each stock in the file
        for i in range(len(df_cal)):
            
            stockcode = df_cal.loc[i,'Code'][0:5]
            print(df_cal.loc[i,'Code'])
            try:
                period = df_cal.loc[i,'Period'].upper() # period in cal file  example 3RD QTR RES/DIV (9-MTH-ENDED31/08/21)
                updateStock(stockcode,period,df_cal,driver)
            except:
                print('Error no period')
        df_cal.to_csv(CALENDAR_DIR+ '/' + file,index=False)
        

    print("new updated สะสม: ",new_update)
    print("new file สะสม: ", new_file)

    driver_quit(driver)
    
    merge_file()
    
    '''
    df_cal = pd.read_csv(CALENDAR_DIR+ '/'+'cal2022822.csv',index_col= False)
    stockcode = '04612'
    period = df_cal[df_cal['Code'] == stockcode + '.HK']['Period'].values[0]
    updateStock(stockcode,period,df_cal,driver)
    driver_quit(driver)
    '''
    
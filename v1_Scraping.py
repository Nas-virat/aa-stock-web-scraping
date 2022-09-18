from utils import *
import sys


data = sys.argv
print(data)

month = '8'
year = '2022'

if len(data) > 2 :
    
    month = data[1]
    year = data[2]


BASE_URL = 'http://www.aastocks.com/en/stocks/market/calendar-daily.aspx?date='


createDir_if_not_exist('data/cal/'+year+'/'+month)

driver = createDriver()


# URL='http://www.aastocks.com/en/stocks/market/calendar-daily.aspx'
for i in range(1,32):
    if len(str(i))==2:
        url = BASE_URL + year+ '-'+ month +'-' +str(i)# ใส่ช้อมูล 4 จุด ตรงนี้ 1 จุด
        month_str = 'cal' + year +month +str(i)# ใส่ช้อมูล 4 จุด ตรงนี้ 1 จุด
    else:
        url = BASE_URL + year+ '-'+ month +'-0' + str(i)# ใส่ช้อมูล 4 จุด ตรงนี้ 1 จุด
        month_str = 'cal' + year +month +'0'+ str(i)# ใส่ช้อมูล 4 จุด ตรงนี้ 1 จุด
    
    
    text_html = get_texthtml(url,driver)
    table_MN = pd.read_html(text_html)
    print(f'Total tables: {len(table_MN)}',"ข้อมูลของวันที่"+str(i))
   
    print('get df')
    df = table_MN[18]
    print(df)
    
    #create update status column
    df['updateStatus'] = 'None'

    if df.iat[0, 0]!="No Result Announcements":
        df.to_csv('data/cal/'+year + '/' + month + '/' + month_str + '.csv', mode='w', encoding='utf-8-sig', index=False)
        #time.sleep(1)

driver_quit(driver)

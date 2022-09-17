from tkinter import font
from utils import *
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

# y folder

df_stock = pd.read_csv('filter-HK-CODE2.csv')



def create_visual(filename,period):
    
    createDir_if_not_exist('out/'+ period +'/img')
    createDir_if_not_exist('out/'+ period +'/interactive')
    
    print('read file: ' ,filename)
    
    df = pd.read_csv('data/'+ period +'/'+ filename)
    
    if(period == 'h'):
        print(filename[0:7]+'-Y'+filename[9:13])
        try:
            df_y = pd.read_csv('data/y/'+ filename[0:7]+'-Y'+filename[9:13])
        except:
            print('No file in Y')
            return False
            
    
    df = pd.concat([df,df_y])
    df.sort_values(by=['Closing Date'], inplace=True)
    
    df.replace('-', '0', inplace=True)
    df['Total Turnover'] = pd.to_numeric(df['Total Turnover'])
    df['Net Profit'] = pd.to_numeric(df['Net Profit'])
    try:
        df['Gross Profit'] = pd.to_numeric(df['Gross Profit'])
    except:
        print('No GP')
    stockcode = filename[0:5]
 
    #print('stockcode: ', stockcode)

    #print(df['Total Turnover'])
    #print(df['Net Profit'])
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(name='Revenue', x=df['Closing Date'], y=df['Total Turnover'],base = 0,text=df['Total Turnover'],textposition="outside",),secondary_y=False)
    fig.add_trace(go.Bar(name='Net Profit', x=df['Closing Date'], y=df['Net Profit'],base = 0,text=df['Net Profit'],textposition="outside",),secondary_y=False)

    
    try:
        gpm = df['Gross Profit']*100/df['Total Turnover']
        gpm = gpm.apply(lambda x: round(x,2))
        fig.add_trace(go.Scatter(mode="lines+markers+text",x=df['Closing Date'], y=gpm, name="GPM%",
                                 text=gpm,
                                 textposition="bottom right",
                                 textfont=dict(
                                    family="sans serif",
                                    color="Green"
                                )),secondary_y=True)
    except:
        print('No GP')
        
    npm = df['Net Profit']*100/df['Total Turnover']
    npm = npm.apply(lambda x: round(x,2))
    fig.add_trace(go.Scatter(mode="lines+markers+text",x=df['Closing Date'], y=npm, name="NPM%",
                             text=npm,
                             textposition="bottom left",
                             textfont=dict(
                                    family="sans serif",
                                    color="crimson"
                                )),secondary_y=True)
    
    
    fig.update_layout(barmode='group',template="seaborn",
        title_text=str(df_stock[df_stock['StockCode'] == int(stockcode)]['Name of Securities'].values[0]) + '    ' + stockcode +'.HK',
        xaxis_title="date",
        title_font_color="red",
        yaxis_title=df['Unit'].values[0] +'    '+ df['Currency'].values[0],
        font=dict(
            size=18,
        ))
    #fig.show()
    pio.write_image(fig,'out/'+ period +'/img/'+str(stockcode)+'.png', width=1480, height=780,format ='png')
    #fig.write_html('out/'+period+'/interactive/'+str(stockcode)+'.html')
    
if __name__ == '__main__':
    
    count = 0 
    for file in os.listdir('data/y'):
        print('file No : ',count)
        create_visual(file,'y')
        count += 1 
    for file in os.listdir('data/h'):
        print('file No : ',count)
        create_visual(file,'h')
        count += 1 
        
    print('finish visual.py')
    '''
    create_visual('00001PL-Y.csv')
    '''
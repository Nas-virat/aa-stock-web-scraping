import sys
import os


from tkinter import *
class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Enter month',font=("Arial", 16))
        self.lbl2=Label(win, text='Enter year',font=("Arial", 16))
       
        self.t1=Entry(width=30,font=("Arial", 16))
        self.t2=Entry(width=30,font=("Arial", 16))
        self.t1.place(height=25)
        self.t2.place(height=25)
        
     
        self.lbl1.place(x=200, y=100)
        self.t1.place(x=400, y=100)
        self.lbl2.place(x=200, y=200)
        self.t2.place(x=400, y=200)
        
        self.b1=Button(win, text='set calander',font=("Arial", 16) ,command=self.set_calander)
        self.b2=Button(win, text='Update Result',font=("Arial", 16) ,command=self.update_result)
        self.b3=Button(win, text='create visual img',font=("Arial", 16) ,command=self.visual)
        
        
        self.b1.place(x=200, y=300)
        self.b2.place(x=400, y=300)
        self.b3.place(x=200, y=400)
    def set_calander(self):
        month=int(self.t1.get())
        year=int(self.t2.get())
        print('month',month,'year',year)
        os.system('python v1_Scraping.py '+str(month)+' '+str(year))
        
    def update_result(self):
        month=int(self.t1.get())
        year=int(self.t2.get())
        print('month',month,'year',year)
        os.system('python v1_Update_result.py '+str(month)+' '+str(year))
        
    def visual(self):
        os.system('python visual.py')

window=Tk()
mywin=MyWindow(window)
window.title('aa stock webscraping')
window.geometry("800x600+10+10")
window.mainloop()






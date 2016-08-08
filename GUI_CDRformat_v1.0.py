# simple GUI with class
import re, datetime,time,operator,xlsxwriter,sys
from operator import itemgetter
from Tkinter import *

class Application(Frame):
    """A GUI with three buttons"""
    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        #self.button_clicks=0 # count the number of clicks
        self.create_widgets()
    def create_widgets(self):
        """Create a button, text, and entry widgets"""
        self.firstrow=Label(self,text='Use this user interface to format the CDR data.\nThe program inputs a text file of CDR data and returns the formatted \nresult in an excel file. You can find the result at the current directory.',
        justify=LEFT)
        self.firstrow.grid(row=0,column=0,columnspan=4,sticky=W)
        self.emptyrow1=Label(self,text='')
        self.emptyrow1.grid(row=1)
        self.instruction=Label(self, text="Enter the complete name of the CDR text file:   ",anchor=W, justify=LEFT)
        self.instruction.grid(row=2,column=0,columnspan=2,sticky=W)# W means west (left side)
        self.emptyrow1=Label(self,text='')
        self.emptyrow1.grid(row=3)

        self.filename=Entry(self,text='')
        self.filename.grid(row=2,column=2,columnspan=2,sticky=W)

        self.submit_button=Button(self,text="Input validation:", command=self.reveal1)
        self.submit_button.grid(row=4)

        self.text1=Label(self) # wrap= WORD,CHAR,NONE
        self.text1.grid(row=4,column=2,columnspan=2, sticky=W)

        self.emptyrow2=Label(self,text='')
        self.emptyrow2.grid(row=5)

        self.Run_button=Button(self,text="Run",state=DISABLED, command=self.reveal2)
        self.Run_button.grid(row=6)

        self.text2=Label(self,text='')#,width=35,height=5,wrap=WORD) # wrap= WORD,CHAR,NONE
        self.text2.grid(row=6,column=2,columnspan=2, sticky=W)
    def reveal1(self):
        """Display a message based on the Entry"""
        self.text1['text']=" "
        self.text2['text']=''
        #self.text1.delete(0.0,END)
        content=self.filename.get()
        try:
            fhand= open(content) # handling the file
            message="File name is OK, press Run"
            #self.text1.insert(0.0,message) #0.0 means row 0 and column 0 as the last position is
            self.text1['text']=message
            fhand.close()
            self.Run_button.configure(state=NORMAL, takefocus='1')

        except:
            message="Invalid filename."
            self.text1['text']=message
            #self.text1.insert(0.0,message) #0.0 means row 0 and column 0 as the last position is
            #exit()
    def reveal2(self):
        """Display a message based on CDRformat results"""
        #self.text2.delete(0.0,END)
        self.text2['text']=''
        inp=self.filename.get()
        count=0
        with open(inp,'r') as fhand:
            for line in fhand:
              if line.startswith('CDR_'):
                 count=count+1
        try:
            self.CDRfunction(inp,count)
            message="Results are ready in the excel file."
            #self.text2.insert(0.0,message)
            self.text2['text']=message
        except:
            message="Operation is not successful because of error...",sys.exc_info()[0]
            #self.text2.insert(0.0,message)
            self.text2['text']=message
        self.Run_button.configure(state=DISABLED)
    def CDRfunction (self,inp,count):
        def month1(x):
                    return {
                       'Jan': 01,
                       'Feb': 02,
                       'Mar': 03,
                       'Apr': 04,
                       'May': 05,
                       'Jun': 06,
                       'Jul': 07,
                       'Aug': 8,
                       'Sep': 9,
                       'Oct': 10,
                       'Nov': 11,
                       'Dec': 12,
                    }[x]
        cdr = [dict() for x in range(count)] #list of dictionaries of CDRs
        fhand=open(inp,'r')
        c=0
        cdr_list=[]
        #print 'number of CDR reports',count,range(count)
        for line in fhand:
            line=line.rstrip()
            line=line.lstrip()
            #print datetime.datetime(int(line[20:24]),month1(line[4:7]),int(line[8:10]),int(line[11:13]), int(line[14:16]), int(line[17:19]))#re.search('[0-3]+',line[11])
            if len(line)>0:
                if re.search('[0-3]+',line[11]):
                    if c<=count:
                        cdr[c]={'id':c,'t':datetime.datetime(int(line[20:24]),month1(line[4:7]),int(line[8:10]),int(line[11:13]), int(line[14:16]), int(line[17:19])),
                        'd1':line[24:],'d2':'','CDRSID':'','mbox':'','ClassOfService':'','MsgID':'','CDRtype':'','reqMWI':'','MWIresult':'','Calling':''}
                        c=c+1

            if c<=count:
                if line.startswith('CDR_'):
                    cdr[c-1]['d2']=re.findall(' ----(.+)',line)
                    cdr[c-1]['CDRSID']=re.findall('CDRSID=(\S+)',line)
                    cdr[c-1]['ClassOfService']=re.findall('COS=(\S+)',line)
                    cdr[c-1]['MsgID']=re.findall('msg_id=(\S+)',line)
                    cdr[c-1]['CDRtype']=re.findall('(^CDR_\S+)',line)
                    if reduce(lambda x,y: x+str(y), cdr[c-1].get('CDRtype'))=='CDR_DATACOLLECTIONMWI':
                        MWI=re.findall('reqMWI=(\S+)',line)
                        if reduce(lambda x,y: x+str(y), MWI)=='0':
                            cdr[c-1]['reqMWI']='MWI Off'
                        if reduce(lambda x,y: x+str(y), MWI)=='1':
                            cdr[c-1]['reqMWI']='MWI On'
                        cdr[c-1]['MWIresult']=re.findall('result=(\S+)',line)
                    if reduce(lambda x,y: x+str(y), cdr[c-1].get('CDRtype'))=='CDR_INCOMINGCALLCONNECT':
                        cdr[c-1]['Calling']=re.findall('calling=(\S+)',line)
                    if reduce(lambda x,y: x+str(y), cdr[c-1].get('CDRtype'))=='CDR_MSGSENT':
                        cdr[c-1]['mbox']=re.findall('dest_mbox=(\S+)',line)
                        cdr[c-1]['Calling']=re.findall('orig_mbox=(\S+)',line)
                        #print cdr[c-1].get('mbox')
                    else:
                        cdr[c-1]['mbox']=re.findall(' mbox=(\S+)',line)
                        ############### sort by datetime#############################
        tmp={}
        i=0
        while i<=(len(cdr)-1):
            j=len(cdr)-1
            while j>=0 and j>=i+1:
                if cdr[j].get('t')<cdr[j-1].get('t'):
                    tmp=cdr[j]
                    cdr[j]=cdr[j-1]
                    cdr[j-1]=tmp
                j=j-1
            i=i+1
        fhand.close()
        ################### sort by type of CDR ###############################
        tmp={}
        i=0
        for i in range(len(cdr)):
            if i+1<=len(cdr)-1:
                if reduce(lambda x,y: x+str(y), cdr[i].get('CDRtype'))=='CDR_DATACOLLECTIONMWI' and cdr[i].get('reqMWI')=='MWI On':
                    if reduce(lambda x,y: x+str(y), cdr[i+1].get('CDRtype'))=='CDR_MSGRECEIVE':
                        if cdr[i].get('mbox')==cdr[i+1].get('mbox') and cdr[i].get('t')==cdr[i+1].get('t'):
                            tmp=cdr[i]
                            cdr[i]=cdr[i+1]
                            cdr[i+1]=tmp
                elif reduce(lambda x,y: x+str(y), cdr[i].get('CDRtype'))=='CDR_MSGCOUNT':
                    if reduce(lambda x,y: x+str(y), cdr[i+1].get('CDRtype'))=='CDR_MSGDELETED':
                        if cdr[i].get('mbox')==cdr[i+1].get('mbox') and cdr[i].get('t')==cdr[i+1].get('t'):
                            tmp=cdr[i]
                            cdr[i]=cdr[i+1]
                            cdr[i+1]=tmp
                elif reduce(lambda x,y: x+str(y), cdr[i].get('CDRtype'))=='CDR_MSGCOUNT':
                    if reduce(lambda x,y: x+str(y), cdr[i+1].get('CDRtype'))=='CDR_PASSWORDTEST':
                        if cdr[i].get('CDRSID')==cdr[i+1].get('CDRSID') and cdr[i].get('t')==cdr[i+1].get('t'):
                            tmp=cdr[i]
                            cdr[i]=cdr[i+1]
                            cdr[i+1]=tmp
        #########################write to excel################################
        def magic( aList, base=10 ):
            n= 0
            for d in aList:
               n = base*n + int(d)
               if n==0:
                   return ' '
            return n
        x=len(inp)
        name=inp[0:x-4]
        book = xlsxwriter.Workbook('%s.xlsx'%name)
        sheet1 = book.add_worksheet()
        bold = book.add_format({'bold': True})
        font=book.add_format({'font_size':10,'font_name':'Arial'})
        col=1
        sheet1.set_column(col,col, 6)
        sheet1.write(0, col, "Count",bold)
        col=col+1
        sheet1.set_column(col,col, 16)
        sheet1.write(0, col, "Date Time",bold)
        col=col+1
        sheet1.set_column(col,col, 23)
        sheet1.write(0, col, "CDR Type",bold)
        col=col+1
        sheet1.set_column(col,col, 28)
        sheet1.write(0, col, "CDRSID",bold)
        col=col+1
        sheet1.set_column(col,col, 11)
        sheet1.write(0, col, "mbox",bold)
        col=col+1
        sheet1.set_column(col,col, 11)
        sheet1.write(0, col, "Calling",bold)
        col=col+1
        sheet1.set_column(col,col, 10)
        sheet1.write(0, col, "message ID",bold)
        col=col+1
        sheet1.set_column(col,col, 7)
        sheet1.write(0, col, "reqMWI",bold)
        col=col+1
        sheet1.set_column(col,col, 8)
        sheet1.write(0, col, "MWI result",bold)
        col=col+1
        sheet1.set_column(col,col, 9)
        sheet1.write(0,col, "Class of Service",bold)
        col=col+1
        sheet1.set_column(col,col, 23)
        sheet1.write(0, col, "First Line",bold)
        col=col+1
        sheet1.set_column(col,col, 100)
        sheet1.write(0, col, "Description in Second Line",bold)
        i=0
        for n in range(len(cdr)):
            i = i+1
            col=1
            sheet1.write(i, col, i,font)
            col+=1
            dt=cdr[n].get('t')
            sheet1.write(i, col, dt.strftime('%x %X'),font)
            col+=1
            CDRTYPE=" ".join(str(x) for x in cdr[n].get('CDRtype'))
            sheet1.write(i, col,CDRTYPE[4:],font)#column width 30
            col+=1
            sheet1.write(i, col, " ".join(str(x) for x in cdr[n].get('CDRSID')),font)#column width 30
            col+=1
            sheet1.write(i, col, magic(" ".join(str(x) for x in cdr[n].get('mbox'))),font)#column width 11
            col+=1
            sheet1.write(i, col, magic(" ".join(str(x) for x in cdr[n].get('Calling'))),font)#column width 11
            col+=1
            sheet1.write(i, col, magic(" ".join(str(x) for x in cdr[n].get('MsgID'))),font)
            col+=1
            sheet1.write(i, col, cdr[n].get('reqMWI'),font)
            col+=1
            sheet1.write(i, col, reduce(lambda x,y: x+str(y), cdr[n].get('MWIresult'), '') ,font)
            col+=1
            sheet1.write(i, col, magic(" ".join(str(x) for x in cdr[n].get('ClassOfService'))),font)#column width 14
            col+=1
            sheet1.write(i, col, reduce(lambda x,y: x+str(y), cdr[n].get('d1'), ''),font)#column width 38
            col+=1
            sheet1.write(i, col, reduce(lambda x,y: x+str(y), cdr[n].get('d2'), ''),font)#column width 100
        book.close()
        return 'correct';


root=Tk()
root.title("CDR fomatting")
root.geometry("400x200")
app=Application(root)

root.mainloop()





        #self.button=Button(self,text="Total Clicks= 0")
        #self.button["command"]=self.update_count#binding the event handler
        #self.button.grid()

#import regular expression
import re, datetime,time,operator,xlwt
from operator import itemgetter

inp = raw_input("Enter file name ")# asks for a file name

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

count=0
with open(inp,'r') as fhand:
    for line in fhand:
      if line.startswith('CDR_'):
         count=count+1
cdr = [dict() for x in range(count)] #list of dictionaries of CDRs
fhand=open(inp,'r')
c=0
cdr_list=[]
print 'number of CDR reports',count,range(count)
for line in fhand:
    line=line.rstrip()
    line=line.lstrip()
    if len(line)>0:
        if re.search('[0-3]+',line[11]):
            if c<=count:
                cdr[c]={'id':c,'t':datetime.datetime(int(line[20:24]),month1(line[4:7]),int(line[8:10]),int(line[11:13]), int(line[14:16]), int(line[17:19])),
                    'd1':line[24:],'d2':'','CDRSID':'','mbox':'','ClassOfService':'','MsgID':'','CDRtype':'','reqMWI':'','MWIresult':''}
                c=c+1

    if c<=count:
        if line.startswith('CDR_'):
            cdr[c-1]['d2']=line
            cdr[c-1]['CDRSID']=re.findall('CDRSID=(\S+)',line)
            cdr[c-1]['mbox']=re.findall('mbox=(\S+)',line)
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
                print 'test'
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
x=len(inp)
name=inp[0:x-4]
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
sheet1.write(0, 1, "Count")
sheet1.write(0, 2, "Date Time")
sheet1.write(0, 3, "CDRSID")
sheet1.write(0, 4, "mbox")
sheet1.write(0, 5, "message ID")
sheet1.write(0, 6, "reqMWI")
sheet1.write(0, 7, "MWI result")
sheet1.write(0, 8, "Class of Service")
sheet1.write(0, 9, "First Line")
sheet1.write(0, 10, "Second Line")
i=0
for n in range(len(cdr)):
    i = i+1
    sheet1.write(i, 1, i)
    dt=cdr[n].get('t')
    sheet1.write(i, 2, dt.strftime('%x %X'))
    sheet1.write(i, 3, cdr[n].get('CDRSID'))
    sheet1.write(i, 4, cdr[n].get('mbox'))
    sheet1.write(i, 5, cdr[n].get('MsgID'))
    sheet1.write(i, 6, cdr[n].get('reqMWI'))
    sheet1.write(i, 7, cdr[n].get('MWIresult'))
    sheet1.write(i, 8, cdr[n].get('ClassOfService'))
    sheet1.write(i, 9, cdr[n].get('d1'))
    sheet1.write(i, 10, cdr[n].get('d2'))
book.save("%s.xls"%name)

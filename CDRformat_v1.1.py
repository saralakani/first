#import regular expression
import re, datetime,time,operator,xlsxwriter
from operator import itemgetter

inp = raw_input("Enter a text file name ")# asks for a file name
try:
    fhand= open(inp) # handling the file
except:
    print "Invalid filename"
    exit()
fhand.close()

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
                #print 'test'
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
sheet1.write(0, 1, "Count",bold)
sheet1.set_column(2,2, 16)
sheet1.write(0, 2, "Date Time",bold)
sheet1.set_column(3,3, 30)
sheet1.write(0, 3, "CDRSID",bold)
sheet1.set_column(4,4, 11)
sheet1.write(0, 4, "mbox",bold)
sheet1.set_column(5,5, 11)
sheet1.write(0, 5, "message ID",bold)
sheet1.set_column(6,6, 11)
sheet1.write(0, 6, "reqMWI",bold)
sheet1.set_column(7,7, 11)
sheet1.write(0, 7, "MWI result",bold)
sheet1.set_column(8,8, 14)
sheet1.write(0,8, "Class of Service",bold)
sheet1.set_column(9,9, 36)
sheet1.write(0, 9, "First Line",bold)
sheet1.set_column(10,10, 100)
sheet1.write(0, 10, "Second Line",bold)
i=0
for n in range(len(cdr)):
    i = i+1
    sheet1.write(i, 1, i,font)
    dt=cdr[n].get('t')
    sheet1.write(i, 2, dt.strftime('%x %X'),font)
    sheet1.write(i, 3, " ".join(str(x) for x in cdr[n].get('CDRSID')),font)#column width 30
    sheet1.write(i, 4, magic(" ".join(str(x) for x in cdr[n].get('mbox'))),font)#column width 11
    sheet1.write(i, 5, magic(" ".join(str(x) for x in cdr[n].get('MsgID'))),font)
    sheet1.write(i, 6, cdr[n].get('reqMWI'),font)
    sheet1.write(i, 7, reduce(lambda x,y: x+str(y), cdr[n].get('MWIresult'), '') ,font)
    sheet1.write(i, 8, magic(" ".join(str(x) for x in cdr[n].get('ClassOfService'))),font)#column width 14
    sheet1.write(i, 9, reduce(lambda x,y: x+str(y), cdr[n].get('d1'), ''),font)#column width 38
    sheet1.write(i, 10, reduce(lambda x,y: x+str(y), cdr[n].get('d2'), ''),font)#column width 100




book.close()

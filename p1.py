#import regular expression
import re, datetime,time,operator
from operator import itemgetter

inp = raw_input("Enter file name ")# asks for a file name
#try:
#    fhand= open(inp) # handling the file
#except:
#    print "Invalid filename"
#    exit()
def day1(x):
        return {
           'Mon': 1,
           'Tue': 2,
           'Wed': 3,
           'Thu': 4,
           'Fri': 5,
           'Sat': 6,
           'Sun':7,
        }[x]
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
#with open(inp,'r') as fhand:
#    for (i, line) in enumerate(fhand):
#        if 'CDR_' in line:
#            i
with open(inp,'r') as fhand:
    for line in fhand:
      if line.startswith('CDR_'):
         count=count+1
cdr = [dict() for x in range(count)] #list of dictionaries of CDRs
print range(count)
fhand=open(inp,'r')
c=0
cdr_list=[]
print 'Number of CDR reports:',count
for line in fhand:
    line=line.rstrip()
    line=line.lstrip()
    if len(line)>0:
        if re.search('[0-3]+',line[11]):
          c=c+1
          if c<=count:
            #cdr[c]['week']=day1(line[0:3])
            #cdr[c]['month']=month1(line[4:7])
            #cdr[c]['day']=int(line[8:10])
            #cdr[c]['hour']=int(line[11:13])
            #cdr[c]['minute']=int(line[14:16])
            #cdr[c]['second']=int(line[17:19])
            #cdr[c]['year']=int(line[20:24])
            #print c,line,'date',cdr[c]['year'],cdr[c]['month'],cdr[c]['week'],cdr[c]['day']
            #print 'time',cdr[c]['hour'],cdr[c]['minute'],cdr[c]['second']
            cdr[c]={'id':c,'t':datetime.datetime(int(line[20:24]),month1(line[4:7]),int(line[8:10]),int(line[11:13]), int(line[14:16]), int(line[17:19])),
                    'd1':line[24:],'d2':''}
            cdr_list.append(cdr[c].get('t'))
            print c,'',cdr[c].get('t')
    if c<=count:
        if line.startswith('CDR_'):
            cdr[c]['d2']=line
            #print cdr[c].get('d2')

#print cdr
#newlist = sorted(cdr, key=operator.itemgetter('t'))
#newlist=sorted(cdr, key=lambda k: k['t'])
#cdr.sort(key=operator.itemgetter('t'))
#def mykey(adict): return adict['t']
#sorted(cdr, key=mykey)

#sort_on = 't'
#decorated = [(dict_[sort_on], dict_) for dict_ in cdr]
#decorated.sort()
#newlist = [dict_ for (key, dict_) in decorated]
#print 'cdr len',len(cdr)
tmp={}
#a_list=[1,9,3,7,8,5,6,4,2]
#l=len(a_list)
i=1
while i<=(len(cdr)):
    #print 'i',i
    j=len(cdr)
    #for j, e in reversed(list(enumerate(cdr_list))):
    while j>=0 and j>=i+1:
        #print 'first j',j
        #print cdr[j].get('t'),cdr[j-1].get('t')
        #if j>=i+1:
        if cdr[j].get('t')<cdr[j-1].get('t'):
            #print 'switching, j',j
            #print cdr[j].get('t'),cdr[j-1].get('t')
            tmp=cdr[j]
            cdr[j]=cdr[j-1]
            cdr[j-1]=tmp
        j=j-1
    i=i+1

#print a_list

#cdr_list.sort()

for i in range(len(cdr_list)):
#    print cdr_list[i]
    print cdr[i].get('t')
    #print cdr[i].get('d1')
    #print cdr[i].get('d2')


#    cdr[line]['day']=line()


#class ClassCDR(object):
#    """docstring for """
#    def __init__(self, arg):
#        super(, self).__init__()
#        self.arg = arg









fhand.close()

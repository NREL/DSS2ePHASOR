#####################
####Transformers#####
#####################


q1=0
q2=0
q3=0
p=0

kf2mil=0.189394
km2mil=0.621371
Trans1={}

import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame
import collections


fd = open("Transformers.dss")
contents = fd.readlines()
fd.close()

new_contents = []
for line in contents:
    if not line.strip():
        continue
    else:
        new_contents.append(line)

f=open("Transformers.dss", "w")
f.write("".join(new_contents))
f.close()


with open("Transformers.dss") as f3:
    lines11=f3.readlines()
    count=len(lines11)

for i in range(0, count):
    lines11[i]=' '.join(lines11[i].split())
    if (lines11[i].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None]*q3
        s2= [None]*q3

count1=0        
for i in range(0, count):
    if (lines11[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines11.index(lines11[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines11[p].split()[0][0] == '~' or lines11[p].split()[0][0] == '!' or lines11[p].strip() == '':
          lines11[i]=lines11[i]+lines11[p]
          if p >= count-1:
              break
          p=p+1
              
s2= [None]* q3
for m in range(0, q3):
    s2[m]=lines11[s1[m]]
    
fr=len(s2)
hr=[None]*fr
qw1=[None]*fr
qw2=[None]*fr
tokens2=[None]*fr
for ty in range(0,fr):
    line=re.sub(' +',' ',s2[ty])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    for h in range(0,len(tokens1)):
        if tokens1[h][0]=='XHL':
            print 'klp'
            for h in range(0,len(tokens1)):
                yr1=tokens1[2][1].split('.')[0]
                yr2=tokens1[3][1]
                yr3=tokens1[4][1]
                yr4=tokens1[6][1].split('.')[0]
                if '.' in tokens1[6][1]:
                    yr41=tokens1[6][1].split('.')[1]
                else:
                    yr41='threephase'
                yr5=tokens1[7][1]
                yr6=tokens1[8][1]
                yr7=tokens1[9][1]
                yr8=tokens1[11][1]
                yr9='wye'
                yr10='wye'

        else:
            for h in range(0,len(tokens1)):
                if tokens1[h][0] =='buses':
                    sd1=tokens1[h][1]
                    yr1=sd1.split(",")[0].split("(")[1].split(".")[0]
                    yr4=sd1.split(",")[1].split(")")[0].split(".")[0]
                    yr41='threephase'
                if tokens1[h][0] =='kvs' or tokens1[h][0] =='kVs':
                    sd2=tokens1[h][1]
                    yr2=sd2.split(",")[0].split("(")[1]
                    yr5=sd2.split(",")[1].split(")")[0]
                if tokens1[h][0] =='kvas' or tokens1[h][0] =='kVAs':
                    sd3=tokens1[h][1]
                    yr3=sd3.split(",")[0].split("(")[1]
                    yr6=sd3.split(",")[1].split(")")[0]
                if tokens1[h][0] =='%r' or tokens1[h][0] =='%loadloss':
                    yr7=tokens1[h][1]
                if tokens1[h][0] =='xhl' or tokens1[h][0] =='XHL':
                    yr8=tokens1[h][1]
                if tokens1[h][0] =='conns':
                    sd3=tokens1[h][1]
                    yr9=sd3.split(",")[0].split("(")[1]
                    yr10=sd3.split(",")[1].split(")")[0]

    hr[ty]='FromBus='+str(yr1)+' '+'FromBuskV='+str(yr2)+' '+'FromBuskVA='+str(yr3)+' '+'ToBus='+str(yr4)+' '+'BusPhase='+yr41+' '+'ToBuskV='+str(yr5)+' '+'ToBuskVA='+str(yr6)+' '+'%r='+str(yr7)+' '+'%x='+str(yr8)+' '+'FromBuswdg='+str(yr9)+' '+'ToBuswdg='+str(yr10)
    
print hr

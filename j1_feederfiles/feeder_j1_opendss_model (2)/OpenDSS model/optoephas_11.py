# Initialization
q1=0
q2=0
p=0
LineCodesd={}
kf2mil=0.189394
km2mil=0.621371
f2mil=0.000189394
mil2mil=1
m2mil=0.000621371

# Import of differnt operations 
import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame

# Open the .dss/.dss file and read each line
f=open("LineCodes.dss", "r")
fileString = f.read()
f.close()

# After reading the files, blank lines are removed and rewritten to the same file
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("LineCodes.dss", "w")
f.write(processedString)
f.close()

# Count the number of lines
with open("LineCodes.dss") as f1:
    lines1=f1.readlines()
    count=len(lines1)

# Scan each line to find the number of unique "New"s for the number of different line configurations
for m in range(0, count):
    if (lines1[m].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None] * q3
        s2= [None]* q3

# Scan each line and then concatenate/append all the lines following a "New" (which might begin with '~', '!' or ' ') to a single line until another "New" is encountered 
count1=0        
for i in range(0, count):
    if (lines1[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines1.index(lines1[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines1[p].split()[0][0] == '~' or lines1[p].split()[0][0] == '!' or lines1[p].strip() == '':
          lines1[i]=lines1[i]+lines1[p]
          if p >= count-1:
              break
          p=p+1

# As q3 is the number of unique "New"s, set s2 is created in order to populate all the lines that begin with "New"        
for k in range(0, q3):
    s2[k]=lines1[s1[k]]

for l in range(0,len(s2)):
    #Any escess whitespace is replaced by a single space
    line=re.sub(' +',' ',s2[l])

    ## tokens1 is created to read all the linecode information that is represented in the form "name=a" ( All the overhead and underground line configuartion information)
    # get line conficuration IDs
    names1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    names1=names1[0].split(".")[1]
    tokens1 = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[\w\.\_]+', line)
    # Read tokens1 and create a set with the same name tokens1
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    # Process to convert RHS string values into integer and float values
    nu=len(tokens1)
    for j  in range(0,nu):
        if tokens1[j][0] == 'nphases' or tokens1[j][0] == 'Nphases':
            tokens1[j][1]=int(tokens1[j][1])
               
    for j  in range(0,nu):
            if tokens1[j][0]== 'R1' or tokens1[j][0] == 'r1':
                tokens1[j][1]=float(tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='X1' or tokens1[j][0] == 'x1':
                tokens1[j][1]=float(tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='R0' or tokens1[j][0] == 'r0':
                tokens1[j][1]=float(tokens1[j][1])
                  
    for j  in range(0,nu):
            if tokens1[j][0]=='X0' or tokens1[j][0] == 'x0':
                tokens1[j][1]=float(tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='C1' or tokens1[j][0] == 'c1':
                tokens1[j][1]=float (tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='C0' or tokens1[j][0] == 'c0':
                tokens1[j][1]=float (tokens1[j][1])                                              

    for j  in range(0,nu):
            if tokens1[j][0]=='BaseFreq' or tokens1[j][0]=='basefreq' or tokens1[j][0]== 'baseFreq' or tokens1[j][0]=='Basefreq':
                tokens1[j][1]=float(tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='Normamps' or tokens1[j][0] == 'normamps' or tokens1[j][0] == 'NormAmps':
                tokens1[j][1]= float (tokens1[j][1])

    for j in range(0,nu):
            if tokens1[j][0]=='Emergamps'or tokens1[j][0]=='emergamps':
                tokens1[j][1]=float(tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='Faultrate' or tokens1[j][0]=='faultrate':
                tokens1[j][1]=float(tokens1[j][1])
                  
    for j  in range(0,nu):
            if tokens1[j][0]=='Pctperm' or tokens1[j][0]=='pctperm':
                tokens1[j][1]=float(tokens1[j][1])
                  
    for j  in range(0,nu):
            if tokens1[j][0]=='Rg' or tokens1[j][0]=='rg':
                tokens1[j][1]=float(tokens1[j][1])

    for j  in range(0,nu):
            if tokens1[j][0]=='Xg' or tokens1[j][0]=='xg':
                tokens1[j][1]=float (tokens1[j][1])
                  
    for j  in range(0,nu):
            if tokens1[j][0]=='Rho' or tokens1[j][0]=='rho':
                tokens1[j][1]=float (tokens1[j][1])

    # Create a dictionary with the Services line configuration information and add the service line configuration name (converting sets to dictionary)
    tokens1 = { x:y for x,y in tokens1}
    tokens1['name'] = names1

    
    ## tokens2 is created to read the 3X3 matrices in the form "name=[ a b c | d e f | g h i]" ( All the service line configuartion information)
    tokens2 = re.findall(r'[\s]?\w+[\s]?\=[\s]?[[(]?[\s]?\d*[+-]?\.?\d*[\s]\d*[+-]?\.?\d*[\s]?\d*[+-]?\.?\d*[\s]?\|[\s]?\d*[+-]?\.?\d*[\s]\d*[+-]?\.?\d*[\s]?\d*[+-]?\.?\d*[\s]?\|[\s]?\d*[+-]?\.?\d*[\s]\d*[+-]?\.?\d*[\s]?\d*[+-]?\.?\d*[\s]?[])]?', line)
    hu=len(tokens2)
    # Line configuartion IDs set
    s3 = [None] * hu
    # Line configuration information set
    s4 = [None] * hu
    str0 = [None] * hu
    str1 = [None] * hu
    str2 = [None] * hu
    str3 = [None] * hu
    str4 = [None] * hu
    str5 = [None] * hu
    y = [None] * hu
    A1 = [None] * hu
    for ih in range (0,hu):
        str0[ih]=(tokens2[ih].split("="))[1]
        s3[ih]=(tokens2[ih].split("="))[0]
        s3[ih]=s3[ih].replace(" ", "")
        #Read rmatrix, xmatrix and cmatrix text data and then remove the braces (,[,),] and vertical bars (|)
        str1[ih]=" ".join(str0[ih].split())
        if str1[ih][0] == '(':
            str2[ih]=str1[ih].replace("(", " ")
        if str1[ih][0] == '[':
            str2[ih]=str1[ih].replace("[", " ")
        if str2[ih][-1] == ')':
            str3[ih]=str2[ih].replace(")", " ")
        if str2[ih][-1] == ']':
            str3[ih]=str2[ih].replace("]", " ")
        str4[ih]=str3[ih].replace("|", " ")
        str5[ih]=" ".join(str4[ih].split())
        y[ih] = str5[ih].split(" ")
        # Line impedance matrix information is read and created as an array based on the way a matrix is represented, either in a lower triangle form or full matrix form 
        if len(y[ih]) == 6:
            A1[ih] = np.array([float ((y[ih])[0]),float ((y[ih])[1]),float ((y[ih])[2]),float ((y[ih])[3]),float ((y[ih])[4]),float ((y[ih])[5])]).reshape(1,6)
        if len(y[ih]) == 9:
            A1[ih] = np.array([float ((y[ih])[0]),float ((y[ih])[1]),float ((y[ih])[4]),float ((y[ih])[6]),float ((y[ih])[7]),float ((y[ih])[8])]).reshape(1,6)
        s4[ih]=A1[ih]
    # Create a dictionary with the Overhead and underground lineconfiguration information
    tokens2= dict(zip(s3,s4))


    ## Append Overhead, underground and service line configuration dictionaries
    LineCodesd[l]=dict(chain.from_iterable(d.iteritems() for d in (tokens1, tokens2)))


#####################################
### Lines spreadsheet creation ######
#####################################

# Initialization
q1=0
q2=0
p=0
Linesd={}

# Open the .dss/.dss file and read each line
f=open("Lines.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Lines.dss", "w")
f.write(processedString)
f.close()

# Scan lines of both "Lines.dss" and "Services.dss"
with open("Lines.dss") as f1:
    lines1_1=f1.readlines()
    count4=len(lines1_1)
with open("Services.dss") as f2:
    lines1_2=f2.readlines()
    lines1=lines1_1+lines1_2
    count=len(lines1)

# Count lines of "Lines.dss" and "Services.dss" q3
for k in range(0, count):
    if (lines1[k].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2

s1 = [None] * q3
s2= [None]* q3

# Scan each line and then concatenate/append all the lines following a "New" (which might begin with '~', '!' or ' ') to a single line until another "New" is encountered 
count1=0        
for i in range(0, count):
    if (lines1[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines1.index(lines1[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines1[p].split()[0][0] == '~' or lines1[p].split()[0][0] == '!' or lines1[p].strip() == '':
          lines1[i]=lines1[i]+lines1[p]
          if p >= count-1:
              break
          p=p+1
          
# As q3 is the number of unique "New"s, set s2 is created in order to populate all the lines that begin with "New"    
for l in range(0, q3):
    s2[l]=lines1[s1[l]]

for n in range(0,len(s2)):
    line=re.sub(' +',' ',s2[n])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[A-Za-z0-9.\/_-]+', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    nu=len(tokens1)
    for j  in range(0,nu):
        if tokens1[j][0] == 'length' or tokens1[j][0] == 'Length':
            tokens1[j][1]=float(tokens1[j][1])
               
    for j  in range(0,nu):
            if tokens1[j][0]== 'phases' or tokens1[j][0] == 'Phases':
                tokens1[j][1]=int(tokens1[j][1])

    for j  in range(0,nu):
        if tokens1[j][0]== 'bus1' or tokens1[j][0] == 'Bus1':
            tokens1[j][1]=(tokens1[j][1]).split(".")[0]

    for j  in range(0,nu):
        if tokens1[j][0]== 'bus2' or tokens1[j][0] == 'Bus2':
            tokens1[j][1]=(tokens1[j][1]).split(".")[0] 

    tokens1 = { x:y for x,y in tokens1}
    tokens1['linenames'] = linenames1
    # create dictionary of lines with length, phases, from bus and to bus information
    Linesd[n]=dict(tokens1)

print Linesd


## For OH and UG line data parsing making sure to exclude switch information
bus1_a = [] 
bus1_b = [] 
bus1_c = []
count4_1=0
for y in range(0,count4):
    if 'switch' not in Linesd[y].keys() and Linesd[y].get('enabled')=='True':
        bus1_a.append((Linesd[y].get('bus1')+"_a").lower())
        bus1_b.append((Linesd[y].get('bus1')+"_b").lower())
        bus1_c.append((Linesd[y].get('bus1')+"_c").lower())
        count4_1=count4_1+1

bus2_a = [] 
bus2_b = [] 
bus2_c = [] 


for y in range(0,count4):
    if 'switch' not in Linesd[y].keys() and Linesd[y].get('enabled')=='True':
        bus2_a.append((Linesd[y].get('bus2')+"_a").lower())
        bus2_b.append((Linesd[y].get('bus2')+"_b").lower())
        bus2_c.append((Linesd[y].get('bus2')+"_c").lower())
        
linename = [] 
for y in range(0,count4):
    if 'switch' not in Linesd[y].keys() and Linesd[y].get('enabled')=='True':
        linename.append('line_'+(Linesd[y].get('linenames')).lower())
        
linelength = []
for y in range(0,count4):
    if 'switch' not in Linesd[y].keys() and Linesd[y].get('enabled')=='True':
        units=Linesd[y].get('units')
        if units == "kft":
            convf = kf2mil
        elif units == "ft":
            convf = f2mil
        elif units == "m":
            convf = m2mil
        elif units == "mi":
            convf = mil2mil
        elif units == "km":
            convf = km2mil

        linelength.append((Linesd[y].get('length'))*convf)

#Using linecode values the Symmetrical line parameter data are extracted from line configuration information
        
r_0 = []
for y in range(0,len(lines1_1)):
    if Linesd[y].get('enabled')=='True':
        R_0=Linesd[y].get('linecode')
        for y1 in range(0,len(LineCodesd)):
            if R_0 in LineCodesd[y1].values():
                temp=(LineCodesd[y1].get('r0'))/km2mil
        r_0.append(temp)

x_0 = [] 
for y in range(0,len(lines1_1)):
    if Linesd[y].get('enabled')=='True':                      
        X_0=Linesd[y].get('linecode')
        for y1 in range(0,len(LineCodesd)):
            if X_0 in LineCodesd[y1].values():
                temp=(LineCodesd[y1].get('x0'))/km2mil
        x_0.append(temp)

r_1 = [] 
for y in range(0,len(lines1_1)):
    if Linesd[y].get('enabled')=='True':                            
        R_1=Linesd[y].get('linecode')
        for y1 in range(0,len(LineCodesd)):
            if R_1 in LineCodesd[y1].values():
                temp=(LineCodesd[y1].get('r1'))/km2mil
        r_1.append(temp)

print r_1
print 'kl'
x_1 = []
for y in range(0,len(lines1_1)):
    if Linesd[y].get('enabled')=='True':                       
        X_1=Linesd[y].get('linecode')
        for y1 in range(0,len(LineCodesd)):
            if X_1 in LineCodesd[y1].values():
                temp=(LineCodesd[y1].get('x1'))/km2mil
        x_1.append(temp)

c_0 = [] 
for y in range(0,len(lines1_1)):
    if Linesd[y].get('enabled')=='True':  
        C_0=Linesd[y].get('linecode')
        for y1 in range(0,len(LineCodesd)):
            if C_0 in LineCodesd[y1].values():
                temp=(LineCodesd[y1].get('c0'))*(2*3.14*60/(1000*km2mil))
        c_0.append(temp)

c_1 = [] 
for y in range(0,len(lines1_1)):
    if Linesd[y].get('enabled')=='True': 
        C_1=Linesd[y].get('linecode')
        for y1 in range(0,len(LineCodesd)):
            if C_1 in LineCodesd[y1].values():
                temp=(LineCodesd[y1].get('c1'))*(2*3.14*60/(1000*km2mil))
        c_1.append(temp)

count4=len(linelength)
print count4
print 'mano'
## End

## Service Lines
# Make sure to initialize all redundant variables again
q1=0
q2=0
p=0
with open("Services.dss") as f3:
    lines11=f3.readlines()
    count=len(lines11)
for iy in range(0, count):
    if (lines11[iy].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None] * q3
        s2= [None]* q3

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
    while lines1[p].split()[0][0] == '~' or lines1[p].split()[0][0] == '!' or lines1[p].strip() == '':
          lines1[i]=lines1[i]+lines1[p]
          if p >= count-1:
              break
          p=p+1

for m in range(0, q3):
    s2[m]=lines11[s1[m]]
    
fr=len(s2)
hr=[None]*fr
for n in range(0,fr):
    line=re.sub(' +',' ',s2[n])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[A-Za-z0-9.\/_-]+', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    # assuming switch is in position 3 (could be modified)
    if tokens1[3][0] !='switch':
        tr1=tokens1[1][1]
        yr1=tr1.split('.')[0]
        tr2=tokens1[2][1]
        yr2=tr2.split('.')[0]
        yr3=tokens1[3][1]
        yr4=tokens1[4][1] 
        hr[n]=yr1+' '+yr2+' '+yr3+' '+yr4
        
    if tokens1[3][0] =='switch':
        hr[n]=''

# '' is removed from hr, as switch information was replaced with '' previously      
while '' in hr:
    hr.remove('')

import collections
[item for item, count in collections.Counter(hr).items() if count > 1]

# countining only unique information as there are reduncies
#cleanlist1 is all the OH,UG and service line information excluding the switches
cleanlist1 = []
[cleanlist1.append(x) for x in hr if x not in cleanlist1]

# create service line list
services_list=[None]*len(cleanlist1)
for n in range(0,len(cleanlist1)):
    services_list[n]=cleanlist1[n].split()

print services_list
print cleanlist1
print len(services_list)
print len(cleanlist1)
#y+count4 makes sure the service line data are added after the OH and UG line information
for y in range(0,len(cleanlist1)):
    bus1_a.append((services_list[y][0]+"_a").lower())
    bus1_b.append((services_list[y][0]+"_b").lower())
    bus1_c.append((services_list[y][0]+"_c").lower())

for y in range(0,len(cleanlist1)):
    bus2_a.append((services_list[y][1]+"_a").lower())
    bus2_b.append((services_list[y][1]+"_b").lower())
    bus2_c.append((services_list[y][1]+"_c").lower())
    
for y in range(0,len(cleanlist1)):
    linename.append('line_'+services_list[y][1].lower())

for y in range(0,len(services_list)):
    linelength.append(float(services_list[y][2])*kf2mil)

# Using linecode values the matrix line data are extracted from line configuration information 
R_11=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    R_11temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if R_11temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['rmatrix'][0,0])/kf2mil
    R_11[y+count4]=temp

X_11=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    X_11temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if X_11temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['xmatrix'][0,0])/kf2mil
    X_11[y+count4]=temp

C_11=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    C_11temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if C_11temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['cmatrix'][0,0])/(kf2mil*2.65)
    C_11[y+count4]=temp

R_21=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    R_21temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if R_21temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['rmatrix'][0,1])/kf2mil
    R_21[y+count4]=temp

X_21=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    X_21temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if X_21temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['xmatrix'][0,1])/kf2mil
    X_21[y+count4]=temp

C_21=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    C_21temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if C_21temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['cmatrix'][0,1])/(kf2mil*2.65)
    C_21[y+count4]=temp

R_22=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    R_22temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if R_22temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['rmatrix'][0,2])/kf2mil
    R_22[y+count4]=temp

X_22=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    X_22temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if X_22temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['xmatrix'][0,2])/kf2mil
    X_22[y+count4]=temp        

C_22=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    C_22temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if C_22temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['cmatrix'][0,2])/(kf2mil*2.65)
    C_22[y+count4]=temp

R_31=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    R_31temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if R_31temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['rmatrix'][0,3])/kf2mil
    R_31[y+count4]=temp

X_31=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    X_31temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if X_31temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['xmatrix'][0,3])/kf2mil
    X_31[y+count4]=temp        

C_31=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    C_31temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if C_31temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['cmatrix'][0,3])/(kf2mil*2.65)
    C_31[y+count4]=temp

R_32=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    R_32temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if R_32temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['rmatrix'][0,4])/kf2mil
    R_32[y+count4]=temp

X_32=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    X_32temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if X_32temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['xmatrix'][0,4])/kf2mil
    X_32[y+count4]=temp

C_32=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    C_32temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if C_32temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['cmatrix'][0,4])/(kf2mil*2.65)
    C_32[y+count4]=temp

R_33=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    R_33temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if R_33temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['rmatrix'][0,5])/kf2mil
    R_33[y+count4]=temp

X_33=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    X_33temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if X_33temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['xmatrix'][0,5])/kf2mil
    X_33[y+count4]=temp

C_33=[None]*(len(cleanlist1)+count4)
for y in range(0,len(cleanlist1)):
    C_33temp=services_list[y][3]
    for y1 in range(0,len(LineCodesd)):
        if C_33temp in LineCodesd[y1].values():
            temp=(LineCodesd[y1]['cmatrix'][0,5])/(kf2mil*2.65)
    C_33[y+count4]=temp


for y in range(0,len(cleanlist1)):
    r_0.append('')
for y in range(0,len(cleanlist1)):
    r_1.append('')
for y in range(0,len(cleanlist1)):
    x_1.append('')
for y in range(0,len(cleanlist1)):
    x_0.append('')
for y in range(0,len(cleanlist1)):
    c_1.append('')
for y in range(0,len(cleanlist1)):
    c_0.append('')

print len(bus1_a)
print len(r_1)
print len(C_33)
print len(R_33)
print (count4)
## End

## Create 3phase Line data frame
df1 =DataFrame({'From bus A': bus1_a, 'From bus B': bus1_b, 'From bus C': bus1_c,  'To bus A': bus2_a, 'To bus B': bus2_b, 'To bus C': bus2_c, 'ID': linename, 'R_1 (ohm/mile)': r_1, 'X_1 (ohm/mile)': x_1, 'R_0 (ohm/mile)': r_0, 'X_0 (ohm/mile)': x_0, 'B_1 (uS/mile)': c_1, 'B_0 (uS/mile)': c_0, 'Length (mile)': linelength, 'R_11 (ohm/mile)': R_11, 'X_11 (ohm/mile)': X_11, 'R_21 (ohm/mile)': R_21, 'X_21 (ohm/mile)': X_21, 'R_22 (ohm/mile)': R_22, 'X_22 (ohm/mile)': X_22, 'R_31 (ohm/mile)': R_31, 'X_31 (ohm/mile)': X_31, 'R_32 (ohm/mile)': R_32, 'X_32 (ohm/mile)': X_32, 'R_33 (ohm/mile)': R_33, 'X_33 (ohm/mile)': X_33, 'B_11 (uS/mile)': C_11, 'B_21 (uS/mile)': C_21, 'B_22 (uS/mile)': C_22, 'B_31 (uS/mile)': C_31, 'B_32 (uS/mile)': C_32, 'B_33 (uS/mile)': C_33 })
df1 = df1[['From bus A','From bus B','From bus C','To bus A','To bus B','To bus C','ID','Length (mile)','R_0 (ohm/mile)','X_0 (ohm/mile)', 'R_1 (ohm/mile)','X_1 (ohm/mile)','B_0 (uS/mile)','B_1 (uS/mile)','R_11 (ohm/mile)','X_11 (ohm/mile)', 'R_21 (ohm/mile)', 'X_21 (ohm/mile)', 'R_22 (ohm/mile)', 'X_22 (ohm/mile)', 'R_31 (ohm/mile)', 'X_31 (ohm/mile)', 'R_32 (ohm/mile)', 'X_32 (ohm/mile)', 'R_33 (ohm/mile)', 'X_33 (ohm/mile)', 'B_11 (uS/mile)', 'B_21 (uS/mile)', 'B_22 (uS/mile)', 'B_31 (uS/mile)', 'B_32 (uS/mile)', 'B_33 (uS/mile)' ]]
## End


#####################################
### Switch spreadsheet creation #####
#####################################

## Begin

# count number of switches in Lines
counts=0
for y in range(0,len(Linesd)):
    if 'switch' in Linesd[y].keys():
        counts=counts+1

q1=0
q2=0
p=0
kf2mil=0.189394
km2mil=0.621371
import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame

# A switch exists in Substation.dss file
f=open("Substation.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Substation.dss", "w")
f.write(processedString)
f.close()

with open("Substation.dss") as f1:
    lines11=f1.readlines()
    count=len(lines11)

for l in range(0, count):
    lines11[l]=' '.join(lines11[l].split())
    if (lines11[l].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None] * q3
        s2= [None]* q3
        
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
    linenames1=linenames1[0].split(".")[0]   
    if linenames1 == "line":
        linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
        linenames15=linenames1[0].split(".")[1]
        tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
        tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
        for ey in range(0,len(tokens1)):
            if "switch" in tokens1[ey][0]:
                counts=counts+1

# Creating switch information as a dictionary
tokens4 = { x:y for x,y in tokens1}


# Creating 3 phase switch information in 3 separate lines 
bus1_s = [None] * counts *3
yst=0
for y in range(0,len(Linesd)):
    if 'switch' in Linesd[y].keys():
        bus1_s[0+3*yst]=Linesd[y].get('bus1')
        bus1_s[0+3*yst]=bus1_s[0+3*yst]+'_a'
        bus1_s[0+3*yst]=(bus1_s[0+3*yst]).lower()
        
        bus1_s[1+3*yst]=Linesd[y].get('bus1')
        bus1_s[1+3*yst]=bus1_s[1+3*yst]+'_b'
        bus1_s[1+3*yst]=(bus1_s[1+3*yst]).lower()

        bus1_s[2+3*yst]=Linesd[y].get('bus1')
        bus1_s[2+3*yst]=bus1_s[2+3*yst]+'_c'
        bus1_s[2+3*yst]=(bus1_s[2+3*yst]).lower()

        yst=yst+1
if 'switch' in tokens4.keys():
    bus1_s[0+3*yst]=tokens4.get('bus1')
    bus1_s[0+3*yst]=bus1_s[0+3*yst]+'_a'
    bus1_s[0+3*yst]=(bus1_s[0+3*yst]).lower()
    
    bus1_s[1+3*yst]=tokens4.get('bus1')
    bus1_s[1+3*yst]=bus1_s[1+3*yst]+'_b'
    bus1_s[1+3*yst]=(bus1_s[1+3*yst]).lower()

    bus1_s[2+3*yst]=tokens4.get('bus1')
    bus1_s[2+3*yst]=bus1_s[2+3*yst]+'_c'
    bus1_s[2+3*yst]=(bus1_s[2+3*yst]).lower()

    yst=yst+1

bus2_s = [None] * counts *3
yst=0
for y in range(0,len(Linesd)):
    if 'switch' in Linesd[y].keys():
        bus2_s[0+3*yst]=Linesd[y].get('bus2')
        bus2_s[0+3*yst]=bus2_s[0+3*yst]+'_a'
        bus2_s[0+3*yst]=(bus2_s[0+3*yst]).lower()
        
        bus2_s[1+3*yst]=Linesd[y].get('bus2')
        bus2_s[1+3*yst]=bus2_s[1+3*yst]+'_b'
        bus2_s[1+3*yst]=(bus2_s[1+3*yst]).lower()
        
        bus2_s[2+3*yst]=Linesd[y].get('bus2')
        bus2_s[2+3*yst]=bus2_s[2+3*yst]+'_c'
        bus2_s[2+3*yst]=(bus2_s[2+3*yst]).lower()
        
        yst=yst+1
if 'switch' in tokens4.keys():
    bus2_s[0+3*yst]=tokens4.get('bus2')
    bus2_s[0+3*yst]=bus2_s[0+3*yst]+'_a'
    bus2_s[0+3*yst]=(bus2_s[0+3*yst]).lower()
    
    bus2_s[1+3*yst]=tokens4.get('bus2')
    bus2_s[1+3*yst]=bus2_s[1+3*yst]+'_b'
    bus2_s[1+3*yst]=(bus2_s[1+3*yst]).lower()
    
    bus2_s[2+3*yst]=tokens4.get('bus2')
    bus2_s[2+3*yst]=bus2_s[2+3*yst]+'_c'
    bus2_s[2+3*yst]=(bus2_s[2+3*yst]).lower()
    
    yst=yst+1

line_sw = [None] * counts *3
yst=0
for y in range(0,len(Linesd)):
    if 'switch' in Linesd[y].keys():
        line_sw[0+3*yst]=Linesd[y].get('linenames')
        line_sw[0+3*yst]=line_sw[0+3*yst]+'_a'
        line_sw[0+3*yst]=(line_sw[0+3*yst]).lower()
        
        line_sw[1+3*yst]=Linesd[y].get('linenames')
        line_sw[1+3*yst]=line_sw[1+3*yst]+'_b'
        line_sw[1+3*yst]=(line_sw[1+3*yst]).lower()
        
        line_sw[2+3*yst]=Linesd[y].get('linenames')
        line_sw[2+3*yst]=line_sw[2+3*yst]+'_c'
        line_sw[2+3*yst]=(line_sw[2+3*yst]).lower()        
        yst=yst+1
if 'switch' in tokens4.keys():
    line_sw[0+3*yst]=linenames15+'_a'
    line_sw[0+3*yst]=(line_sw[0+3*yst]).lower()
    
    line_sw[1+3*yst]=linenames15+'_b'
    line_sw[1+3*yst]=(line_sw[1+3*yst]).lower()
    
    line_sw[2+3*yst]=linenames15+'_c'
    line_sw[2+3*yst]=(line_sw[2+3*yst]).lower()

    yst=yst+1 


#check for the status of swith on(1)/off(0)
status_sw = [None] * counts *3
yst=0
for y in range(0,len(Linesd)):
    if 'switch' in Linesd[y].keys():
        status_sw[0+3*yst]=Linesd[y].get('enabled')
        if status_sw[0+3*yst] == 'Yes' or status_sw[0+3*yst] =='yes':
            status_sw[0+3*yst]=1
        elif status_sw[0+3*yst] == 'No' or status_sw[0+3*yst] =='no':
            status_sw[0+3*yst]=0
        
        status_sw[1+3*yst]=Linesd[y].get('enabled')
        if status_sw[1+3*yst] == 'Yes' or status_sw[1+3*yst] =='yes':
            status_sw[1+3*yst]=1
        elif status_sw[1+3*yst] == 'No' or status_sw[1+3*yst] =='no':
            status_sw[1+3*yst]=0
        
        status_sw[2+3*yst]=Linesd[y].get('enabled')
        if status_sw[2+3*yst] == 'Yes' or status_sw[2+3*yst] =='yes':
            status_sw[2+3*yst]=1
        elif status_sw[2+3*yst] == 'No' or status_sw[2+3*yst] =='no':
            status_sw[2+3*yst]=0
        yst=yst+1
if 'switch' in tokens4.keys():
    status_sw[0+3*yst]=tokens4.get('enabled')
    if status_sw[0+3*yst] == 'Yes' or status_sw[0+3*yst] =='yes':
        status_sw[0+3*yst]=1
    elif status_sw[0+3*yst] == 'No' or status_sw[0+3*yst] =='no':
        status_sw[0+3*yst]=0
        
    status_sw[1+3*yst]=tokens4.get('enabled')
    if status_sw[1+3*yst] == 'Yes' or status_sw[1+3*yst] =='yes':
        status_sw[1+3*yst]=1
    elif status_sw[1+3*yst] == 'No' or status_sw[1+3*yst] =='no':
        status_sw[1+3*yst]=0
        
    status_sw[2+3*yst]=tokens4.get('enabled')
    if status_sw[2+3*yst] == 'Yes' or status_sw[2+3*yst] =='yes':
        status_sw[2+3*yst]=1
    elif status_sw[2+3*yst] == 'No' or status_sw[2+3*yst] =='no':
        status_sw[2+3*yst]=0
    yst=yst+1

## Create 3phase switched data frame
df2 =DataFrame({'From bus': bus1_s, 'To bus': bus2_s, 'ID': line_sw, 'Status':status_sw})
df2 = df2[['From bus','To bus','ID','Status']]
## End



###################################
### Load spreadsheet creation #####
###################################

q1=0
q2=0
q3=0
p=0
Load1={}

fd = open("LoadsInd.dss")
contents = fd.readlines()
fd.close()

new_contents = []
for line in contents:
    if not line.strip():
        continue
    else:
        new_contents.append(line)

f=open("LoadsInd.dss", "w")
f.write("".join(new_contents))
f.close()


with open("LoadsInd.dss") as f3:
    lines11=f3.readlines()
    count=len(lines11)

for l in range(0, count):
    lines11[l]=' '.join(lines11[l].split())
    if (lines11[l].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None]* q3
        s2= [None]* q3

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
qw=[None]*fr
tokens2=[None]*fr
for j in range(0,fr):
    line=re.sub(' +',' ',s2[j])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[A-Za-z0-9.\/_-]+', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    # Find the 'item' phases's location that is used to find the number of phases later by getting the 'value'
    name ='phases'
    list = tokens1

    new_list=[]
    for item in list:
        new_list.append(item[0])
    loc= new_list.index(name)
    for h in range(0,len(tokens1)):
        if tokens1[loc][1] =='1':
            if tokens1[h][0] =='bus':
                yr1=tokens1[h][1].split('.')[0]
                yr2=tokens1[h][1].split('.')[1]
#                yr1=tokens1[h][1].split('-')[0]
#                yr2=tokens1[h][1].split('-')[1]
            if tokens1[h][0] =='kV':
                yr3=float (tokens1[h][1])
            if tokens1[h][0] =='kW':
                yr4=float (tokens1[h][1])
            if tokens1[h][0] =='kvar' or 'pf':
                if tokens1[h][0]=='kvar':
                    yr5=float (tokens1[h][1])
                if tokens1[h][0]=='pf':
                    yr5=((yr4/float (tokens1[h][1]))**2 - (yr4)**2)**0.5

        else:
            if tokens1[h][0] =='bus':
                yr1=tokens1[h][1].split('.')[0]
#                yr1=tokens1[h][1]
                yr2='threephase'
            if tokens1[h][0] =='kV':
                yr3=float (tokens1[h][1])
            if tokens1[h][0] =='kW':
                yr4=float (tokens1[h][1])
            if tokens1[h][0] =='kvar' or 'pf':
                if tokens1[h][0]=='kvar':
                    yr5=float (tokens1[h][1])
                if tokens1[h][0]=='pf':
                    yr5=((yr4/float (tokens1[h][1]))**2 - (yr4)**2)**0.5

    hr[j]='Bus='+yr1+' '+'Phase='+yr2+' '+'kv='+str(yr3)+' '+'kw='+str(yr4)+' '+'kvar='+str(yr5)
    qw[j]=yr1
    tokens2[j] = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[\w\.\_\-\c]+', hr[j])
    tokens2[j] = [x.replace(" ", "").split('=') for x in tokens2[j]]
    tokens2[j][2][1] = float (tokens2[j][2][1])
    tokens2[j][3][1] = float (tokens2[j][3][1])
    tokens2[j][4][1] = float (tokens2[j][4][1])
    tokens2[j] = { x:y for x,y in tokens2[j]}
    Load1[j]=dict(tokens2[j])




Loads_list=[None]*len(hr)
for j in range(0,len(hr)):
    Loads_list[j]=hr[j].split()
   
[item for item, count in collections.Counter(qw).items() if count > 1]
cleanlist1 = []
[cleanlist1.append(x) for x in qw if x not in cleanlist1]

Busn=[None]*len(cleanlist1)
PA=[None]*len(cleanlist1)
PB=[None]*len(cleanlist1)
PC=[None]*len(cleanlist1)
toke2=[None]*len(cleanlist1)
Load2={}
for k in range(0,len(cleanlist1)):
    temp1='Busn='+cleanlist1[k]
    temp2='PA='+'0'
    temp3='PB='+'0'
    temp4='PC='+'0'
    temp5='QA='+'0'
    temp6='QB='+'0'
    temp7='QC='+'0'
    temp8='kv='+'0'
    Busn[k]=temp1+' '+temp2+' '+temp3+' '+temp4+' '+temp5+' '+temp6+' '+temp7+' '+temp8
    toke2[k] = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[\w\.\_\-\c]+', Busn[k])
    toke2[k] = [x.replace(" ", "").split('=') for x in toke2[k]]
    toke2[k][1][1] = float (toke2[k][1][1])
    toke2[k][2][1] = float (toke2[k][2][1])
    toke2[k][3][1] = float (toke2[k][3][1])
    toke2[k][4][1] = float (toke2[k][4][1])
    toke2[k][5][1] = float (toke2[k][5][1])
    toke2[k][6][1] = float (toke2[k][6][1])
    toke2[k][7][1] = float (toke2[k][7][1])
    toke2[k] = { x:y for x,y in toke2[k]}
    Load2[k]=dict(toke2[k])

for i in range(0,len(Load2)):
    for j in range(0,len(Load1)):
        if Load2[i].get('Busn')==Load1[j].get('Bus'):
            Load2[i]['kv'] = Load1[j]['kv']
            if Load1[j]['Phase'] == '1' or Load1[j]['Phase'] == 'A.1' or Load1[j]['Phase'] ==  'a.1':
                Load2[i]['PA'] = Load1[j]['kw']
                Load2[i]['QA'] = Load1[j]['kvar']
            if Load1[j]['Phase'] == '2' or Load1[j]['Phase'] == 'B.2' or Load1[j]['Phase'] == 'b.2':
                Load2[i]['PB'] = Load1[j]['kw']
                Load2[i]['QB'] = Load1[j]['kvar']
            if Load1[j]['Phase'] == '3' or Load1[j]['Phase'] == 'C.3' or Load1[j]['Phase'] == 'c.3':
                Load2[i]['PC'] = Load1[j]['kw']
                Load2[i]['QC'] = Load1[j]['kvar']
            if Load1[j]['Phase'] == 'threephase':
                Load2[i]['PA'] = Load1[j]['kw']/3
                Load2[i]['PB'] = Load1[j]['kw']/3
                Load2[i]['PC'] = Load1[j]['kw']/3
                Load2[i]['QA'] = Load1[j]['kvar']/3
                Load2[i]['QB'] = Load1[j]['kvar']/3
                Load2[i]['QC'] = Load1[j]['kvar']/3
                Load2[i]['kv'] = Load1[j]['kv']/1.732

## Creating individual lists
ID = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp='Load_'+(Load2[k].get('Busn'))
    ID[k]=temp
    ID[k]=(ID[k]).lower()    

BusA = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('Busn'))
    BusA[k]=temp+'_a'
    BusA[k]=(BusA[k]).lower()
    
BusB = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('Busn'))
    BusB[k]=temp+'_b'
    BusB[k]=(BusB[k]).lower()
    
BusC = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('Busn'))
    BusC[k]=temp+'_c'
    BusC[k]=(BusC[k]).lower()
    
Type = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp='ZIP'
    Type[k]=temp

P_a = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('PA'))
    P_a[k]=temp

Q_a = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('QA'))
    Q_a[k]=temp

P_b = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('PB'))
    P_b[k]=temp

Q_b = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('QB'))
    Q_b[k]=temp

P_c = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('PC'))
    P_c[k]=temp

Q_c = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('QC'))
    Q_c[k]=temp

V = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=(Load2[k].get('kv'))*1.732
    V[k]=temp

Band = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=0.2
    Band[k]=temp

Conn = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp='wye'
    Conn[k]=temp

K_z = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=0
    K_z[k]=temp

K_i = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=0
    K_i[k]=temp

K_p = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=1
    K_p[k]=temp

Status = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=1
    Status[k]=temp

Initial = [None] * len(Load2)
for k in range(0,len(Load2)):
    temp=1
    Initial[k]=temp

##

## Data frame for 3-phase load
df3 =DataFrame({'Bus A': BusA, 'Bus B': BusB, 'Bus C': BusC, 'ID':ID,'Type': Type, 'P_a (kW)': P_a, 'Q_a (kVAr)': Q_a, 'P_b (kW)': P_b, 'Q_b (kVAr)': Q_b,'P_c (kW)': P_c, 'Q_c (kVAr)': Q_c, 'V (kV)': V,'Bandwidth (pu)': Band, 'Conn. type': Conn, 'K_z': K_z,'K_i': K_i, 'K_p': K_p, 'Status': Status, 'Use initial voltage?': Initial })
df3 = df3[['Bus A', 'Bus B', 'Bus C', 'ID','Type', 'P_a (kW)', 'Q_a (kVAr)', 'P_b (kW)', 'Q_b (kVAr)','P_c (kW)', 'Q_c (kVAr)', 'V (kV)','Bandwidth (pu)', 'Conn. type', 'K_z','K_i', 'K_p', 'Status', 'Use initial voltage?']]
##



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
    # basis issue to use wdg, bus, kv, kVA as 'items' to find its values is that there are two sets with the same names (for primary and secondary windings)
    # Therefore data parsing in this case relies on the fact that 'items' always retain their index positions
    if tokens1[0][1] == "1" or tokens1[0][1] == "3" and tokens1[1][1] == "1":
        yr1=tokens1[2][1].split('.')[0]
        yr2=tokens1[3][1]
        yr3=tokens1[4][1]
#        yr4=tokens1[6][1].split('-')[0]
        yr4=tokens1[6][1].split('.')[0]
#        if '-' in tokens1[6][1]:
        if '.' in tokens1[6][1]:
#            yr41=tokens1[6][1].split('-')[1]            
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
            if tokens1[h][0] =='xhl':
                sd1=tokens1[2][1]
                sd2=tokens1[4][1]
                sd3=tokens1[5][1]
                sd4=tokens1[3][1]

                yr1=sd1.split(",")[0].split("(")[1]
                if '.' in yr1:          
                    yr1=(sd1.split(",")[0].split("(")[1]).split('.')[0]
                else:
                    yr1=(sd1.split(",")[0].split("(")[1])

                print yr1
                yr2=sd2.split(",")[0].split("(")[1]
                yr3=sd3.split(",")[0].split("(")[1]
                yr4=sd1.split(",")[1].split(")")[0]
                if '.' in yr4:          
                    yr4=(sd1.split(",")[1].split(")")[0]).split('.')[0]
                else:
                    yr4=(sd1.split(",")[1].split(")")[0])
                    
                yr41='threephase'
                yr5=sd2.split(",")[1].split(")")[0]
                yr6=sd3.split(",")[1].split(")")[0]
                yr7=tokens1[7][1]
                yr8=tokens1[6][1]
                yr9=sd4.split(",")[0].split("(")[1]
                yr10=sd4.split(",")[1].split(")")[0]
            if tokens1[h][0] == '%loadloss':
                sd1=tokens1[2][1]
                sd2=tokens1[4][1]
                sd3=tokens1[5][1]
                sd4=tokens1[3][1]
                
                yr1=sd1.split(",")[0].split("(")[1]
                if '.' in yr1:          
                    yr1=(sd1.split(",")[0].split("(")[1]).split('.')[0]
                else:
                    yr1=(sd1.split(",")[0].split("(")[1])

                print yr1
                yr2=sd2.split(",")[0].split("(")[1]
                yr3=sd3.split(",")[0].split("(")[1]
                yr4=sd1.split(",")[1].split(")")[0]
                if '.' in yr4:          
                    yr4=(sd1.split(",")[1].split(")")[0]).split('.')[0]
                else:
                    yr4=(sd1.split(",")[1].split(")")[0])
                
                yr41='threephase'
                yr5=sd2.split(",")[1].split(")")[0]
                yr6=sd3.split(",")[1].split(")")[0]
                yr7=tokens1[6][1]
                yr8=tokens1[8][1]
                yr9=sd4.split(",")[0].split("(")[1]
                yr10=sd4.split(",")[1].split(")")[0]

    hr[ty]='FromBus='+yr1+' '+'FromBuskV='+yr2+' '+'FromBuskVA='+yr3+' '+'ToBus='+yr4+' '+'BusPhase='+yr41+' '+'ToBuskV='+yr5+' '+'ToBuskVA='+yr6+' '+'%r='+yr7+' '+'%x='+yr8+' '+'FromBuswdg='+yr9+' '+'ToBuswdg='+yr10
    qw1[ty]=yr1+'*'+yr4   
    tokens2[ty] = re.findall(r'[\?%\w\.\_\-]+[\ ]*=[\ ]*[\w\.\_\-]+', hr[ty])
    tokens2[ty] = [x.replace(" ", "").split('=') for x in tokens2[ty]]
    tokens2[ty][1][1] = float (tokens2[ty][1][1])
    tokens2[ty][2][1] = float (tokens2[ty][2][1])
    tokens2[ty][5][1] = float (tokens2[ty][5][1])
    tokens2[ty][6][1] = float (tokens2[ty][6][1])
    tokens2[ty][7][1] = float (tokens2[ty][7][1])
    tokens2[ty][8][1] = float (tokens2[ty][8][1])
    tokens2[ty] = { x:y for x,y in tokens2[ty]}
    Trans1[ty]=dict(tokens2[ty])

print Trans1
print "lopp"

[item for item, count in collections.Counter(qw1).items() if count > 1]
cleanlist1 = []
[cleanlist1.append(x) for x in qw1 if x not in cleanlist1]


Busl=[None]*len(cleanlist1)
PA=[None]*len(cleanlist1)
PB=[None]*len(cleanlist1)
PC=[None]*len(cleanlist1)
toke2=[None]*len(cleanlist1)
Trans2={}
for k in range(0,len(cleanlist1)):
    temp1='Busl='+cleanlist1[k]
    temp2='FrombuskV='+'0'
    temp3='TobuskV='+'0'
    temp4='FrombuskVA='+'0'
    temp5='TobuskVA='+'0'
    temp6='%r='+'0'
    temp7='%x='+'0'
    temp8='Bus2='+cleanlist1[k].split("*")[1]
    Busl[k]=temp1+' '+temp2+' '+temp3+' '+temp4+' '+temp5+' '+temp6+' '+temp7+' '+temp8
    toke2[k] = re.findall(r'[\?%\w\.\_\-]+[\ ]*=[\ ]*[\w\.\_\-\*]+', Busl[k])
    toke2[k] = [x.replace(" ", "").split('=') for x in toke2[k]]
    toke2[k][1][1] = float (toke2[k][1][1])
    toke2[k][2][1] = float (toke2[k][2][1])
    toke2[k][3][1] = float (toke2[k][3][1])
    toke2[k][4][1] = float (toke2[k][4][1])
    toke2[k][5][1] = float (toke2[k][5][1])
    toke2[k][6][1] = float (toke2[k][6][1])
    toke2[k] = { x:y for x,y in toke2[k]}
    Trans2[k]=dict(toke2[k])

print Trans2

for i in range(0,len(Trans2)):
    for j in range(0,len(Trans1)):
        if Trans2[i].get('Bus2')==Trans1[j].get('ToBus'):
#            if Trans1[j]['BusPhase'] == 'A.1':
            if Trans1[j]['BusPhase'] == '1':
                Trans2[i]['FrombuskV'] = Trans1[j]['FromBuskV']
                Trans2[i]['TobuskV'] = Trans1[j]['ToBuskV']
                Trans2[i]['FrombuskVA'] = Trans1[j]['FromBuskVA']*3
                Trans2[i]['TobuskVA'] = Trans1[j]['ToBuskVA']*3
                Trans2[i]['%r'] = Trans1[j]['%r']
                Trans2[i]['%x'] = Trans1[j]['%x']        
#           if Trans1[j]['BusPhase'] == 'B.2':
            if Trans1[j]['BusPhase'] == '2':                
                Trans2[i]['FrombuskV'] = Trans1[j]['FromBuskV']
                Trans2[i]['TobuskV'] = Trans1[j]['ToBuskV']
                Trans2[i]['FrombuskVA'] = Trans1[j]['FromBuskVA']*3
                Trans2[i]['TobuskVA'] = Trans1[j]['ToBuskVA']*3
                Trans2[i]['%r'] = Trans1[j]['%r']
                Trans2[i]['%x'] = Trans1[j]['%x']
#            if Trans1[j]['BusPhase'] == 'C.3':
            if Trans1[j]['BusPhase'] == '3':
                Trans2[i]['FrombuskV'] = Trans1[j]['FromBuskV']
                Trans2[i]['TobuskV'] = Trans1[j]['ToBuskV']
                Trans2[i]['FrombuskVA'] = Trans1[j]['FromBuskVA']*3
                Trans2[i]['TobuskVA'] = Trans1[j]['ToBuskVA']*3
                Trans2[i]['%r'] = Trans1[j]['%r']
                Trans2[i]['%x'] = Trans1[j]['%x']
            if Trans1[j]['BusPhase'] == 'threephase':
                Trans2[i]['FrombuskV'] = Trans1[j]['FromBuskV']/1.732
                Trans2[i]['TobuskV'] = Trans1[j]['ToBuskV']/1.732
                Trans2[i]['FrombuskVA'] = Trans1[j]['FromBuskVA']
                Trans2[i]['TobuskVA'] = Trans1[j]['ToBuskVA']
                Trans2[i]['%r'] = Trans1[j]['%r']
                Trans2[i]['%x'] = Trans1[j]['%x']

# Transformed information from "Transformers.txt"
ID = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    temp2=temp.split("*")[1]
    ID[i]="VR_"+temp1+"_"+temp2
    ID[i]=(ID[i]).lower()
    
W1BusA = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    W1BusA[i]=temp1+'_a'
    W1BusA[i]=(W1BusA[i]).lower()
    
W1BusB = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    W1BusB[i]=temp1+'_b'
    W1BusB[i]=(W1BusB[i]).lower()

W1BusC = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    W1BusC[i]=temp1+'_c'
    W1BusC[i]=(W1BusC[i]).lower()

W1V = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('FrombuskV'))*1.732
    W1V[i]=temp

W1kVA = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('FrombuskVA'))
    W1kVA[i]=temp

W1R = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('%r'))/2
    W1R[i]=temp/100

W1conn = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp='wye'
    W1conn[i]=temp

W2BusA = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[1]
    W2BusA[i]=temp1+'_a'
    W2BusA[i]=(W2BusA[i]).lower()

W2BusB = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[1]
    W2BusB[i]=temp1+'_b'
    W2BusB[i]=(W2BusB[i]).lower()    

W2BusC = [None] * (len(Trans2)+1) 
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[1]
    W2BusC[i]=temp1+'_c'
    W2BusC[i]=(W2BusC[i]).lower()    

W2V = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('TobuskV'))*1.732
    W2V[i]=temp

W2kVA = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('TobuskVA'))
    W2kVA[i]=temp

W2R = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('%r'))/2
    W2R[i]=temp/100

W2conn = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp='wye'
    W2conn[i]=temp

WX = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('%x'))
    WX[i]=temp/100

TapA = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    TapA[i]=0

TapB = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    TapB[i]=0

TapC = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    TapC[i]=0

LowestTap = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    LowestTap[i]=-16

HighestTap = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    HighestTap[i]=16

MinRange = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    MinRange[i]=10

MaxRange = [None] * (len(Trans2)+1)
for i in range(0,len(Trans2)):
    MaxRange[i]=10



# There is a transformer at the substation
q1=0
q2=0
p=0
q3=0
kf2mil=0.189394
km2mil=0.621371
f=open("Substation.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Substation.dss", "w")
f.write(processedString)
f.close()

with open("Substation.dss") as f1:
    lines11=f1.readlines()
    count=len(lines11)

for i in range(0, count):
    lines11[i]=' '.join(lines11[i].split())
    if (lines11[i].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None] *q3
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
tokens2=[None]*fr
Trans3=[None]*fr
for ty in range(0,fr):
    line=re.sub(' +',' ',s2[ty])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[0]   
    # To find the transformer information in the substation file lines
    if linenames1 == "Transformer":
        tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
        tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
        sd1=tokens1[2][1]
        sd2=tokens1[4][1]
        sd3=tokens1[5][1]
        yr1=sd1.split(",")[0].split("(")[1]
        yr2=sd2.split(",")[0].split("(")[1]
        yr3=sd3.split(",")[0].split("(")[1]
        yr4=sd1.split(",")[1].split(")")[0]
        yr5=sd2.split(",")[1].split(")")[0]
        yr6=sd3.split(",")[1].split(")")[0]
        yr7=tokens1[7][1]
        yr8=tokens1[9][1]
        qw2=yr1+'*'+yr4
        hr='Busl='+qw2+' '+'FrombuskV='+yr2+' '+'FrombuskVA='+yr3+' '+'Bus2='+yr4+' '+'TobuskV='+yr5+' '+'TobuskVA='+yr6+' '+'%r='+yr8+' '+'%x='+yr7
        tokens2 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\ ]*[\w\.\_\*]+', hr)
        tokens2 = [x.replace(" ", "").split('=') for x in tokens2]
        tokens2[1][1] = float (tokens2[1][1])
        tokens2[2][1] = float (tokens2[2][1])
        tokens2[4][1] = float (tokens2[4][1])
        tokens2[5][1] = float (tokens2[5][1])
        tokens2[6][1] = float (tokens2[6][1])
        tokens2[7][1] = float (tokens2[7][1])        
        Trans3={ x:y for x,y in tokens2}

# Transformed information from "Substation.dss"
for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[0]
    temp2=temp.split("*")[1]
    ID[i]="VR_"+temp1+"_"+temp2
    ID[i]=(ID[i]).lower()
    
for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[0]
    W1BusA[i]=temp1+'_a'
    W1BusA[i]=(W1BusA[i]).lower()

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[0]
    W1BusB[i]=temp1+'_b'
    W1BusB[i]=(W1BusB[i]).lower()
    
for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[0]
    W1BusC[i]=temp1+'_c'
    W1BusC[i]=(W1BusC[i]).lower()
    
for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('FrombuskV'))
    W1V[i]=temp

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('FrombuskVA'))
    W1kVA[i]=temp

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('%r'))
    W1R[i]=temp/100

for i in range(len(Trans2),len(Trans2)+1):
    temp='wye'
    W1conn[i]=temp

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[1]
    W2BusA[i]=temp1+'_a'
    W2BusA[i]=(W2BusA[i]).lower()

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[1]
    W2BusB[i]=temp1+'_b'
    W2BusB[i]=(W2BusB[i]).lower()

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('Busl'))
    temp1=temp.split("*")[1]
    W2BusC[i]=temp1+'_c'
    W2BusC[i]=(W2BusC[i]).lower()
    
for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('TobuskV'))
    W2V[i]=temp

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('TobuskVA'))
    W2kVA[i]=temp

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('%r'))
    W2R[i]=temp/100

for i in range(len(Trans2),len(Trans2)+1):
    temp='wye'
    W2conn[i]=temp

for i in range(len(Trans2),len(Trans2)+1):
    temp=(Trans3.get('%x'))
    WX[i]=temp/100

for i in range(len(Trans2),len(Trans2)+1):
    TapA[i]=0

for i in range(len(Trans2),len(Trans2)+1):
    TapB[i]=0

for i in range(len(Trans2),len(Trans2)+1):
    TapC[i]=0

for i in range(len(Trans2),len(Trans2)+1):
    LowestTap[i]=-16

for i in range(len(Trans2),len(Trans2)+1):
    HighestTap[i]=16

for i in range(len(Trans2),len(Trans2)+1):
    MinRange[i]=10

for i in range(len(Trans2),len(Trans2)+1):
    MaxRange[i]=10


## Regulator transformer

q1=0
q2=0
p=0
LineCodesd={}
kf2mil=0.189394
km2mil=0.621371
f2mil=0.000189394
mil2mil=1
m2mil=0.000621371

# Import of differnt operations 
import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame
Linesd={}

# Open the .dss/.dss file and read each line
f=open("Regulators_mod.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Regulators_mod.dss", "w")
f.write(processedString)
f.close()

# Scan lines of both "Lines.dss" and "Services.dss"
with open("Regulators_mod.dss") as f2:
    lines1=f2.readlines()
    count=len(lines1)

# Count lines of "Lines.dss" and "Services.dss" q3
for k in range(0, count):
    if (lines1[k].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2

s1 = [None] * q3
s2= [None]* q3

# Scan each line and then concatenate/append all the lines following a "New" (which might begin with '~', '!' or ' ') to a single line until another "New" is encountered 
count1=0        
for i in range(0, count):
    if (lines1[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines1.index(lines1[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines1[p].split()[0][0] == '~' or lines1[p].split()[0][0] == '!' or lines1[p].strip() == '':
          lines1[i]=lines1[i]+lines1[p]
          if p >= count-1:
              break
          p=p+1
          
# As q3 is the number of unique "New"s, set s2 is created in order to populate all the lines that begin with "New"    
for l in range(0, q3):
    s2[l]=lines1[s1[l]]

fr=len(s2)
hr=[None]*fr
qw1=[None]*fr
tokens2=[None]*fr
Trans3={}
tokens4=[]
tokens3={}
print fr
sd=0
for ty in range(0,fr):
    line=re.sub(' +',' ',s2[ty])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[0]

    if linenames1 == "Transformer":
        
        tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\d]?[.]?\d*[A-Za-z0-9.\/_,-]+?', line)
        tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
           
        tokens2 = re.findall(r'[\?%\w\.\_]+[\ ]*=[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[\,][\s]?\d*[A-Za-z0-9.\/_,-]+[\s]??[])]?', line)
        tokens2 = [x.replace(" ", "").split('=') for x in tokens2]


        tokens1=(tokens2+tokens1)
            
        for h in range(0,len(tokens1)):
            if tokens1[h][0] =='xhl':
                for h in range(0,len(tokens1)):
                    if tokens1[h][0] =='buses':
                        sd1=tokens1[h][1]
                        yr1=sd1.split(",")[0].split("(")[1].split(".")[0]
                        yr4=sd1.split(",")[1].split(")")[0].split(".")[0]
                        if "." in sd1.split(",")[1].split(")")[0]:
                            yr41=sd1.split(",")[1].split(")")[0].split(".")[1]
                        else:
                            yr41='threephase'

                    if tokens1[h][0] =='conns':
                        sd12=tokens1[h][1]
                        yr12=sd12.split(",")[0].split("(")[1]
                        yr42=sd12.split(",")[1].split(")")[0]

                    if tokens1[h][0] =='kvs':
                        sd13=tokens1[h][1]
                        yr13=sd13.split(",")[0].split("(")[1]
                        yr43=sd13.split(",")[1].split(")")[0]

                    if tokens1[h][0] =='kvas':
                        sd14=tokens1[h][1]
                        yr14=sd14.split(",")[0].split("(")[1]
                        yr44=sd14.split(",")[1].split(")")[0]                        
                            
                    if tokens1[h][0] =='xhl':
                        yr55=tokens1[h][1]

                    if tokens1[h][0] =='%r':
                        yr66=tokens1[h][1]

            if tokens1[h][0] == '%loadloss':
                for h in range(0,len(tokens1)):
                    if tokens1[h][0] =='buses':
                        sd1=tokens1[h][1]
                        yr1=sd1.split(",")[0].split("(")[1].split(".")[0]
                        yr4=sd1.split(",")[1].split(")")[0].split(".")[0]
                        if "." in sd1.split(",")[1].split(")")[0]:
                            yr41=sd1.split(",")[1].split(")")[0].split(".")[1]
                        else:
                            yr41='threephase'


        qw2=yr1+'*'+yr4
        hr='Busl='+qw2+' '+'Bus2='+yr4+' '+'phase='+yr41+' '+'connp='+yr12+' '+'conns='+yr42+' '+'kvsp='+yr13+' '+'kvss='+yr43+' '+'kvasp='+yr14+' '+'kvass='+yr44+' '+'xhl='+yr55+' '+'rhl='+yr66
        print hr
        tokens2 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\ ]*[\w\.\_\*]+', hr)
        tokens2 = [x.replace(" ", "").split('=') for x in tokens2]
        tokens3[sd]={ x:y for x,y in tokens2}
        print tokens3[sd]
        Trans3[sd]=dict(tokens3[sd])
        sd=sd+1

print Trans3

sa=[None]*len(Trans3)
for i in range(0,len(Trans3)):
    sa[i]=Trans3[i].get('Busl')
    
import collections
[item for item, count in collections.Counter(sa).items() if count > 1]
cleanlist1 = []
[cleanlist1.append(x) for x in sa if x not in cleanlist1]

print cleanlist1

Busl=[None]*len(cleanlist1)
PA=[None]*len(cleanlist1)
PB=[None]*len(cleanlist1)
PC=[None]*len(cleanlist1)
toke2=[None]*len(cleanlist1)
Trans2={}
for k in range(0,len(cleanlist1)):
    temp1='Busl='+cleanlist1[k]
    temp2='FrombuskV='+'0'
    temp3='TobuskV='+'0'
    temp4='FrombuskVA='+'0'
    temp5='TobuskVA='+'0'
    temp6='%r='+'0'
    temp7='%x='+'0'
    temp8='Bus2='+cleanlist1[k].split("*")[1]
    Busl[k]=temp1+' '+temp2+' '+temp3+' '+temp4+' '+temp5+' '+temp6+' '+temp7+' '+temp8
    toke2[k] = re.findall(r'[\?%\w\.\_\-]+[\ ]*=[\ ]*[\w\.\_\-\*]+', Busl[k])
    toke2[k] = [x.replace(" ", "").split('=') for x in toke2[k]]
    toke2[k][1][1] = float (toke2[k][1][1])
    toke2[k][2][1] = float (toke2[k][2][1])
    toke2[k][3][1] = float (toke2[k][3][1])
    toke2[k][4][1] = float (toke2[k][4][1])
    toke2[k][5][1] = float (toke2[k][5][1])
    toke2[k][6][1] = float (toke2[k][6][1])
    toke2[k] = { x:y for x,y in toke2[k]}
    Trans2[k]=dict(toke2[k])

print Trans2


for i in range(0,len(Trans2)):
    for j in range(0,len(Trans3)):
        if Trans2[i].get('Bus2')==Trans3[j].get('Bus2'):
#            if Trans1[j]['BusPhase'] == 'A.1':
            if Trans3[j]['phase'] == '1':
                Trans2[i]['FrombuskV'] = float(Trans3[j]['kvsp'])
                Trans2[i]['TobuskV'] = float(Trans3[j]['kvss'])
                Trans2[i]['FrombuskVA'] = float(Trans3[j]['kvasp'])*3
                Trans2[i]['TobuskVA'] = float(Trans3[j]['kvass'])*3
                Trans2[i]['%r'] = float(Trans3[j]['rhl'])
                Trans2[i]['%x'] = float(Trans3[j]['xhl'])        
#           if Trans1[j]['BusPhase'] == 'B.2':
            if Trans3[j]['phase'] == '2':
                Trans2[i]['FrombuskV'] = float(Trans3[j]['kvsp'])
                Trans2[i]['TobuskV'] = float(Trans3[j]['kvss'])
                Trans2[i]['FrombuskVA'] = float(Trans3[j]['kvasp'])*3
                Trans2[i]['TobuskVA'] = float(Trans3[j]['kvass'])*3
                Trans2[i]['%r'] = float(Trans3[j]['rhl'])
                Trans2[i]['%x'] = float(Trans3[j]['xhl']) 
#            if Trans1[j]['BusPhase'] == 'C.3':
            if Trans3[j]['phase'] == '3':
                Trans2[i]['FrombuskV'] = float(Trans3[j]['kvsp'])
                Trans2[i]['TobuskV'] = float(Trans3[j]['kvss'])
                Trans2[i]['FrombuskVA'] = float(Trans3[j]['kvasp'])*3
                Trans2[i]['TobuskVA'] = float(Trans3[j]['kvass'])*3
                Trans2[i]['%r'] = float(Trans3[j]['rhl'])
                Trans2[i]['%x'] = float(Trans3[j]['xhl']) 
            if Trans3[j]['phase'] == 'threephase':
                Trans2[i]['FrombuskV'] = float(Trans3[j]['kvsp'])/1.732
                Trans2[i]['TobuskV'] = float(Trans3[j]['kvss'])/1.732
                Trans2[i]['FrombuskVA'] = float(Trans3[j]['kvasp'])
                Trans2[i]['TobuskVA'] = float(Trans3[j]['kvass'])
                Trans2[i]['%r'] = float(Trans3[j]['rhl'])
                Trans2[i]['%x'] = float(Trans3[j]['xhl'])

print Trans2
                
# Transformed information from "regulator_mod.dss"
ID_reg = [None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    print temp
    temp1=temp.split("*")[0]
    temp2=temp.split("*")[1]
    ID_reg[i]="VR_"+temp1+"_"+temp2
    ID_reg[i]=(ID_reg[i]).lower()

W1BusA_reg= [None] * (len(Trans2))    
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    W1BusA_reg[i]=temp1+'_a'
    W1BusA_reg[i]=(W1BusA_reg[i]).lower()

W1BusB_reg= [None] * (len(Trans2)) 
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    W1BusB_reg[i]=temp1+'_b'
    W1BusB_reg[i]=(W1BusB_reg[i]).lower()

W1BusC_reg= [None] * (len(Trans2))    
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[0]
    W1BusC_reg[i]=temp1+'_c'
    W1BusC_reg[i]=(W1BusC_reg[i]).lower()

W1V_reg =[None] * (len(Trans2))    
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('FrombuskV'))*1.732
    W1V_reg[i]=temp

W1kVA_reg=[None] * (len(Trans2))  
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('FrombuskVA'))
    W1kVA_reg[i]=temp

W1R_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('%r'))
    W1R_reg[i]=temp/100

W1conn_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp='wye'
    W1conn_reg[i]=temp

W2BusA_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[1]
    W2BusA_reg[i]=temp1+'_a'
    W2BusA_reg[i]=(W2BusA_reg[i]).lower()

W2BusB_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[1]
    W2BusB_reg[i]=temp1+'_b'
    W2BusB_reg[i]=(W2BusB_reg[i]).lower()

W2BusC_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('Busl'))
    temp1=temp.split("*")[1]
    W2BusC_reg[i]=temp1+'_c'
    W2BusC_reg[i]=(W2BusC_reg[i]).lower()

W2V_reg=[None] * (len(Trans2))    
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('TobuskV'))*1.732
    W2V_reg[i]=temp

W2kVA_reg=[None] * (len(Trans2))  
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('TobuskVA'))
    W2kVA_reg[i]=temp

W2R_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('%r'))
    W2R_reg[i]=temp/100

W2conn_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp='wye'
    W2conn_reg[i]=temp

WX_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    temp=(Trans2[i].get('%x'))
    WX_reg[i]=temp/100

TapA_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    TapA_reg[i]=0

TapB_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    TapB_reg[i]=0

TapC_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    TapC_reg[i]=0

LowestTap_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    LowestTap_reg[i]=-16

HighestTap_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    HighestTap_reg[i]=16

MinRange_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    MinRange_reg[i]=10

MaxRange_reg=[None] * (len(Trans2))
for i in range(0,len(Trans2)):
    MaxRange_reg[i]=10


ID=ID+ID_reg
W1BusA=W1BusA+W1BusA_reg
W1BusB=W1BusB+W1BusB_reg
W1BusC=W1BusC+W1BusC_reg
W1V=W1V+W1V_reg
W1kVA=W1kVA+W1kVA_reg
W1R=W1R+W1R_reg
W1conn=W1conn+W1conn_reg

W2BusA=W2BusA+W2BusA_reg
W2BusB=W2BusB+W2BusB_reg
W2BusC=W2BusC+W2BusC_reg
W2V=W2V+W2V_reg
W2kVA=W2kVA+W2kVA_reg
W2R=W2R+W2R_reg
W2conn=W2conn+W2conn_reg
WX=WX+WX_reg

TapA=TapA+TapA_reg
TapB=TapB+TapB_reg
TapC=TapC+TapC_reg

LowestTap=LowestTap+LowestTap_reg
HighestTap=HighestTap+HighestTap_reg

MinRange=MinRange+MinRange_reg
MaxRange=MaxRange+MaxRange_reg

## Data frame for transfromer, needs modification in the excel spreadheet by moving one line manually
df4 =DataFrame({'ID':ID ,'W1Bus A':W1BusA,'W1Bus B':W1BusB,'W1Bus C':W1BusC,'W1V (kV)':W1V,'W1S_base (kVA)':W1kVA,'W1R (pu)':W1R,'W1Conn. type':W1conn,'W2Bus A':W2BusA,'W2Bus B':W2BusB,'W2Bus C':W2BusC,'W2V (kV)':W2V,'W2S_base (kVA)':W2kVA,'W2R (pu)':W2R,'W2Conn. type':W2conn,'X (pu)':WX,'Tap A':TapA,'Tap B':TapB,'Tap C':TapC,'Lowest Tap':LowestTap,'Highest Tap':HighestTap,'Min Range (%)':MinRange,'Max Range (%)':MaxRange })
df4 = df4[['ID' ,'W1Bus A','W1Bus B','W1Bus C','W1V (kV)','W1S_base (kVA)','W1R (pu)','W1Conn. type','W2Bus A','W2Bus B','W2Bus C','W2V (kV)','W2S_base (kVA)','W2R (pu)','W2Conn. type','X (pu)','Tap A','Tap B','Tap C','Lowest Tap','Highest Tap','Min Range (%)','Max Range (%)']]
##

################
###Capacitor####
################

q1=0
q2=0
p=0
q3=0
kf2mil=0.189394
km2mil=0.621371
cap1={}

import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame
import collections

with open("Capacitors.dss") as f3:
    lines11=f3.readlines()
    count=len(lines11)

for i in range(0, count):
    lines11[i]=' '.join(lines11[i].split())
    if (lines11[i].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None] * q3
        s2= [None]* q3

count1=0        
for i in range(0, count):
    if (lines11[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines11.index(lines11[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
       
s2= [None]* q3
for m in range(0, q3):
    s2[m]=lines11[s1[m]]
    
fr=len(s2)
hr=[None]*fr
we=[None]*fr
qw1=[None]*fr
qw2=[None]*fr
toke1=[None]*fr
for k in range(0,fr):
    line=re.sub(' +',' ',s2[k])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[0]
    if linenames1 == "Capacitor":
        tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
        tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
        yr1=tokens1[0][1]
        yr2=tokens1[1][1]
        yr3=tokens1[2][1]
        yr4=tokens1[3][1]
        # Integrating Bus, kV, kVAr and connection type into a single line
        hr[k]='Bus='+yr1+' '+'kV='+yr2+' '+'kVAr='+yr3+' '+'conn='+yr4  
        toke1[k] = re.findall(r'[\?%\w\.\_]+[\ ]*=[\ ]*[\w\.\_]+', hr[k])
        toke1[k] = [x.replace(" ", "").split('=') for x in toke1[k]]
        toke1[k][1][1] = float (toke1[k][1][1])
        toke1[k][2][1] = float (toke1[k][2][1])
        
        toke1[k] = { x:y for x,y in toke1[k]}
        cap1[k]=dict(toke1[k])
   
# Bus connections of Cap. units
BusA = [None] * len(cap1)
BusB = [None] * len(cap1)
BusC = [None] * len(cap1)
ID = [None] * len(cap1)
for n in range(0,len(cap1)):
    temp=(cap1[n].get('Bus'))
    BusA[n]=temp+'_a'
    BusA[n]=(BusA[n]).lower()
    
    BusB[n]=temp+'_b'
    BusB[n]=(BusB[n]).lower()
    
    BusC[n]=temp+'_c'
    BusC[n]=(BusC[n]).lower()
    
    ID[n]='CAP_'+temp
    ID[n]=(ID[n]).lower()

# Power Values of Cap. units.. No active power injection
P_a = [None] * len(cap1)
Q_a = [None] * len(cap1)
P_b = [None] * len(cap1)
Q_b = [None] * len(cap1)
P_c = [None] * len(cap1)
Q_c = [None] * len(cap1)
for y in range(0,len(cap1)):
    temp=(cap1[y].get('kVAr'))/3
    P_a[y]=0
    Q_a[y]=-1*temp
    P_b[y]=0
    Q_b[y]=-1*temp
    P_c[y]=0
    Q_c[y]=-1*temp

# Voltage at Cap. banks
V = [None] * len(cap1)
for y in range(0,len(cap1)):
    temp=(cap1[y].get('kV'))/1.732
    V[y]=temp

# Status of cap. bank switch: on(1)/off(0)
StatusA = [None] * len(cap1)
StatusB = [None] * len(cap1)
StatusC = [None] * len(cap1)
for y in range(0,len(cap1)):
    StatusA[y]=1
    StatusB[y]=1
    StatusC[y]=1    

## Data fram for 3 phase shunt
df5 =DataFrame({ 'Bus A': BusA ,'Bus B':BusB,'Bus C': BusC,'ID':ID ,'P_a (kW)': P_a,'Q_a (kVAr)': Q_a,'P_b (kW)': P_b,'Q_b (kVAr)': Q_b,'P_c (kW)': P_c,'Q_c (kVAr)': Q_c,'V (kV)':V,'Status A':StatusA,'Status B':StatusB,'Status C':StatusC})
df5 =df5[['Bus A','Bus B','Bus C','ID','P_a (kW)','Q_a (kVAr)','P_b (kW)','Q_b (kVAr)','P_c (kW)','Q_c (kVAr)','V (kV)','Status A','Status B','Status C']]
##



########################################
### Faultbuses spreadsheet creation ####
########################################

df=pd.read_csv("J1_EXP_VOLTAGES.CSV")
df.shape

Count_Row=df.shape[0]
count=0
busn=[]
Magn=[]
Angn=[]
Noden=[]

Fault_bus = [None] * (Count_Row)
BusA = [None] * (Count_Row)
BusB = [None] * (Count_Row)
BusC = [None] * (Count_Row)
Type = [None] * (Count_Row)
R_f = [None] * (Count_Row)
X_f = [None] * (Count_Row)
R_g = [None] * (Count_Row)
X_g = [None] * (Count_Row)
Status = [None] * (Count_Row)
# Count4 ended with the number of OH and UG lines in the previous section, therfore count4 is added below to begin from the end of OH nad UG end of line buses
for j in range(0,(Count_Row)):
    Fault_bus[j]='Fault_'+df['Bus'][j]
    Fault_bus[j]=(Fault_bus[j]).lower()
    
    BusA[j]=df['Bus'][j]
    BusA[j]=BusA[j]+'_a'
    BusA[j]=(BusA[j]).lower()   

    BusB[j]=df['Bus'][j]
    BusB[j]=BusB[j]+'_b'
    BusB[j]=(BusB[j]).lower()  

    BusC[j]=df['Bus'][j]
    BusC[j]=BusC[j]+'_c'
    BusC[j]=(BusC[j]).lower()  

    Type[j]='abcg'    
    R_f[j]=0.000001
    X_f[j]=0
    R_g[j]=0.000001
    X_g[j]=0
    Status[j]=0

# Statuses are all initially 0
# In case fault analysis on bus is required put a 1 for status on the fault buses
## Data frame for Fault bus information
df6 =DataFrame({'ID': Fault_bus,'Bus A': BusA,'Bus B': BusB,'Bus C': BusC,'Type': Type,'R_f':R_f,'X_f':X_f,'R_g':R_g,'X_g':X_g,'Status':Status  })
df6 = df6[['ID','Bus A','Bus B','Bus C','Type','R_f','X_f','R_g','X_g','Status' ]]
##


####################################
### Source spreadsheet creation ####
####################################

q1=0
q2=0
p=0

f=open("Substation.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Substation.dss", "w")
f.write(processedString)
f.close()

with open("Substation.dss") as f1:
    lines11=f1.readlines()
    count=len(lines11)

for iy in range(0, count):
    lines11[iy]=' '.join(lines11[iy].split())
    if (lines11[iy].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None] * q3
        s2= [None]* q3
        
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
we=[None]*fr
qw1=[None]*fr
qw2=[None]*fr
toke1=[None]*fr
counts=3
for ty in range(0,fr):
    line=re.sub(' +',' ',s2[ty])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[0]   
    we[ty]= linenames1.split("-")[0]
    if linenames1 == "Circuit":
        tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
        tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
        for ey in range(0,len(tokens1)):
            if "switch" in tokens1[ey][0]:
                counts=counts+1

tokens4 = { x:y for x,y in tokens1}

BusA=[None]*1
BusB=[None]*1
BusC=[None]*1
ID=[None]*1
V=[None]*1
Angle=[None]*1
SCL_1=[None]*1
SCL_3=[None]*1
R_pos=[None]*1
X_pos=[None]*1
R_zero=[None]*1
X_zero=[None]*1


BusA[0]=tokens4.get('bus1')
BusA[0]=BusA[0]+'_a'
BusA[0]=(BusA[0]).lower()

BusB[0]=tokens4.get('bus1')
BusB[0]=BusB[0]+'_b'
BusB[0]=(BusB[0]).lower()

BusC[0]=tokens4.get('bus1')
BusC[0]=BusC[0]+'_c'
BusC[0]=(BusC[0]).lower()

ID[0]='SOURCE_A'
ID[0]=(ID[0]).lower()

V[0]=float (tokens4.get('basekv'))

Angle[0]=0

SCL_1[0]=1000000
SCL_3[0]=1000000
R_pos[0]=0
X_pos[0]=0
R_zero[0]=0
X_zero[0]=0

## Source information  dataframe creation
df7 =DataFrame({'Bus A': BusA ,'Bus B':BusB,'Bus C':BusC,'ID':ID,'V (kV)':V,'Angle (deg)':Angle,'SCL_1 (MVA)':SCL_1,'SCL_3 (MVA)':SCL_3,'R_pos (ohm)':R_pos,'X_pos (ohm)':X_pos,'R_zero (ohm)':R_zero,'X_zero (ohm)':X_zero})
df7 = df7[['Bus A','Bus B','Bus C','ID','V (kV)','Angle (deg)','SCL_1 (MVA)','SCL_3 (MVA)','R_pos (ohm)','X_pos (ohm)','R_zero (ohm)','X_zero (ohm)'  ]]
##

###############################################
### Current Injection spreadsheet creation ####
###############################################

q1=0
q2=0
p=0
counts3=0
tokens1={}
expv={}
distgen={}
kf2mil=0.189394
km2mil=0.621371
import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame

# Existing PV
f=open("ExistingPV.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("ExistingPV.dss", "w")
f.write(processedString)
f.close()

with open("ExistingPV.dss") as f1:
    lines22=f1.readlines()
    count=len(lines22)

for iy in range(0, count):
    lines22[iy]=' '.join(lines22[iy].split())
    if (lines22[iy].split(' ')[0].split(".")[0]) == 'new' or (lines22[iy].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1= [None]*q3
        s2= [None]*q3
        
count1=0
for i in range(0, count):
    if (lines22[i].split(" ")[0].split(".")[0]) == 'new' or (lines22[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines22.index(lines22[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines22[p].split()[0][0] == '~' or lines22[p].split()[0][0] == '!' or lines22[p].strip() == '':
          lines22[i]=lines22[i]+lines22[p]
          if p >= count-1:
              break
          p=p+1
       
s2= [None]* q3
for m in range(0, q3):
    s2[m]=lines22[s1[m]]
    
fr=len(s2)
hr=[None]*fr
we=[None]*fr
qw1=[None]*fr
qw2=[None]*fr
toke1=[None]*fr
qq=0
for ty in range(0,fr):
    line=re.sub(' +',' ',s2[ty])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)    
    linenames1=linenames1[0].split(".")[1]  
    we[ty]= linenames1
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames15=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    tokens4 = { x:y for x,y in tokens1}
    tokens4['DGname'] = we[ty]
    qq=qq+int (tokens4.get('phases'))
    expv[ty] = dict(tokens4)

# Distributed Generation
q1=0
q2=0
p=0
f=open("distributedgen.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("distributedgen.dss", "w")
f.write(processedString)
f.close()

with open("distributedgen.dss") as f1:
    lines22=f1.readlines()
    count=len(lines22)

for iy in range(0, count):
    lines22[iy]=' '.join(lines22[iy].split())
    if (lines22[iy].split(' ')[0].split(".")[0]) == 'new':
        q2=q2+1
        q3=q2
        s1 = [None]* q3
        s2= [None]* q3
        
count1=0
for i in range(0, count):
    if (lines22[i].split(" ")[0].split(".")[0]) == 'new':
        yy=lines22.index(lines22[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines22[p].split()[0][0] == '~' or lines22[p].split()[0][0] == '!' or lines22[p].strip() == '':
          lines22[i]=lines22[i]+lines22[p]
          if p >= count-1:
              break
          p=p+1
       
s2= [None]* q3
for i in range(0, q3):
    s2[i]=lines22[s1[i]]
    
fr=len(s2)
hr=[None]*fr
we=[None]*fr
qw1=[None]*fr
qw2=[None]*fr
toke1=[None]*fr
qq2=0
for j in range(0,fr):
    line=re.sub(' +',' ',s2[j])
    linenames1 = re.findall(r'new[\t ]+([A-Za-z0-9.\/_-]+)', line)    
    linenames1=linenames1[0].split(".")[1]  
    linenames1 = re.findall(r'new[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames15=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    tokens4 = { x:y for x,y in tokens1}
    tokens4['DGname'] = we[j]
    qq2=qq2+int (tokens4.get('phases'))

n=0
bus1_s = [None] * (qq+qq2)
DGID_s = [None] * (qq+qq2)
for k in range(0,len(expv)):
    if int (expv[k].get('phases')) == 3:
        if ".1.2.3" in expv[k].get('bus1'):
            wes=expv[k].get('bus1').split(".")[0]
        else:
            wes=expv[k].get('bus1')

        bus1_s[0+3*n]=wes
        bus1_s[0+3*n]=bus1_s[0+3*n]+'_a'
        bus1_s[0+3*n]=(bus1_s[0+3*n]).lower()         
        
        bus1_s[1+3*n]=wes
        bus1_s[1+3*n]=bus1_s[1+3*n]+'_b'
        bus1_s[1+3*n]=(bus1_s[1+3*n]).lower()        
        
        bus1_s[2+3*n]=wes
        bus1_s[2+3*n]=bus1_s[2+3*n]+'_c'
        bus1_s[2+3*n]=(bus1_s[2+3*n]).lower()         

        DGID_s[0+3*n]=expv[k].get('DGname')
        DGID_s[0+3*n]=DGID_s[0+3*n]+'_a'
        DGID_s[0+3*n]=(DGID_s[0+3*n]).lower()           
        
        DGID_s[1+3*n]=expv[k].get('DGname')
        DGID_s[1+3*n]=DGID_s[1+3*n]+'_b'
        DGID_s[1+3*n]=(DGID_s[1+3*n]).lower()        
        
        DGID_s[2+3*n]=expv[k].get('DGname')
        DGID_s[2+3*n]=DGID_s[2+3*n]+'_c'
        DGID_s[2+3*n]=(DGID_s[2+3*n]).lower()
        
        n=n+1

n=n*3
for k in range(0,len(expv)):
    if int (expv[k].get('phases')) == 1:
        bus1_s[n]=expv[k].get('bus1').split("-")[0]+"_"+expv[k].get('bus1').split("-")[1].split(".")[0]
        bus1_s[n]=(bus1_s[n]).lower()

        DGID_s[n]=expv[k].get('DGname')+"_"+expv[k].get('bus1').split("-")[1].split(".")[0]
        DGID_s[n]=(DGID_s[n]).lower()
        n=n+1

# Distributed Generators
q1=0
q2=0
p=0
f=open("distributedgen.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("distributedgen.dss", "w")
f.write(processedString)
f.close()

with open("distributedgen.dss") as f1:
    lines22=f1.readlines()
    count=len(lines22)

for i in range(0, count):
    lines22[i]=' '.join(lines22[i].split())
    if (lines22[i].split(' ')[0].split(".")[0]) == 'new':
        q2=q2+1
        q3=q2
        s1 = [None] * q3
        s2= [None]* q3
        
count1=0
for i in range(0, count):
    if (lines22[i].split(" ")[0].split(".")[0]) == 'new':
        yy=lines22.index(lines22[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines22[p].split()[0][0] == '~' or lines22[p].split()[0][0] == '!' or lines22[p].strip() == '':
          lines22[i]=lines22[i]+lines22[p]
          if p >= count-1:
              break
          p=p+1
       
s2= [None]* q3
for m in range(0, q3):
    s2[m]=lines22[s1[m]]
    
fr=len(s2)
hr=[None]*fr
we=[None]*fr
qw1=[None]*fr
qw2=[None]*fr
toke1=[None]*fr
qq=0
for k in range(0,fr):
    line=re.sub(' +',' ',s2[k])
    linenames1 = re.findall(r'new[\t ]+([A-Za-z0-9.\/_-]+)', line)    
    linenames1=linenames1[0].split(".")[1]  
    we[k]= linenames1
    linenames1 = re.findall(r'new[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames15=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\s]?[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[])]?', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    tokens4 = { x:y for x,y in tokens1}
    tokens4['DGname'] = we[k]
    qq=qq+int (tokens4.get('phases'))
    distgen[k] = dict(tokens4)

for k in range(0,len(distgen)):
    if int (distgen[k].get('phases')) == 1:
        bus1_s[n]=distgen[k].get('bus1').split("-")[0]+"_"+distgen[k].get('bus1').split("-")[1].split(".")[0]
        bus1_s[n]=(bus1_s[n]).lower()

        DGID_s[n]=distgen[k].get('DGname')+"_"+distgen[k].get('bus1').split("-")[1].split(".")[0]
        DGID_s[n]=(DGID_s[n]).lower()
        n=n+1

for k in range(0,len(distgen)):
    if int (distgen[k].get('phases')) == 3:
        if ".1.2.3" in distgen[k].get('bus1'):
            wes=distgen[k].get('bus1').split(".")[0]
        else:
            wes=distgen[k].get('bus1')
        bus1_s[n]=wes+'_a'
        bus1_s[n]=(bus1_s[n]).lower()         
        DGID_s[n]=distgen[k].get('DGname')
        DGID_s[n]=DGID_s[n]+'_a'
        DGID_s[n]=(DGID_s[n]).lower()
        n=n+1
        bus1_s[n]=wes+'_b'
        bus1_s[n]=(bus1_s[n]).lower()        
        DGID_s[n]=distgen[k].get('DGname')
        DGID_s[n]=DGID_s[n]+'_b'
        DGID_s[n]=(DGID_s[n]).lower()
        n=n+1
        bus1_s[n]=wes+'_c'
        bus1_s[n]=(bus1_s[n]).lower()         
        DGID_s[n]=distgen[k].get('DGname')
        DGID_s[n]=DGID_s[n]+'_c'
        DGID_s[n]=(DGID_s[n]).lower()
        n=n+1

## Current injector dataframe creation
df8 =DataFrame({'Bus': bus1_s ,'ID':DGID_s})
df8 = df8[['Bus' ,'ID'  ]]
##

df=pd.read_csv("J1_EXP_VOLTAGES.CSV")
df.shape
Count_Row=df.shape[0]
count=0
busn=[]
Magn=[]
Angn=[]
Noden=[]
for k in range(0,Count_Row):
    tempbus=df['Bus'][k].lower()
    tempmag=df[' Magnitude1'][k]
    tempang=df[' Angle1'][k]
    tempnode=df[' Node1'][k]
    tempnode2=df[' Node2'][k]

    if df[' Node1'][k] == 1:
        busn.append((df['Bus'][k]+"_a").lower())
        Magn.append(df[' Magnitude1'][k])
        Angn.append(df[' Angle1'][k])
        Noden.append(df[' Node1'][k])
    if df[' Node1'][k] == 2:
        busn.append((df['Bus'][k]+"_b").lower())
        Magn.append(df[' Magnitude1'][k])
        Angn.append(df[' Angle1'][k])
        Noden.append(df[' Node1'][k])
    if df[' Node1'][k] == 3:
        busn.append((df['Bus'][k]+"_c").lower())
        Magn.append(df[' Magnitude1'][k])
        Angn.append(df[' Angle1'][k])
        Noden.append(df[' Node1'][k])

    if df[' Node2'][k] == 1:
        busn.append((df['Bus'][k]+"_a").lower())
        Magn.append(df[' Magnitude2'][k])
        Angn.append(df[' Angle2'][k])  
    if df[' Node2'][k] == 2:
        busn.append((df['Bus'][k]+"_b").lower())
        Magn.append(df[' Magnitude2'][k])
        Angn.append(df[' Angle2'][k])       
    if df[' Node2'][k] == 3:
        busn.append((df['Bus'][k]+"_c").lower())
        Magn.append(df[' Magnitude2'][k])
        Angn.append(df[' Angle2'][k])
    if df[' Node2'][k] == 0:
        if tempnode == 1:
            busn.append((tempbus+"_b").lower())
            Magn.append(tempmag)
            Angn.append(tempang-120)
        if tempnode == 2:
            busn.append((tempbus+"_a").lower())
            Magn.append(tempmag)
            Angn.append(tempang+120)
        if tempnode == 3:
            busn.append((tempbus+"_a").lower())
            Magn.append(tempmag)
            Angn.append(tempang-120)

    if df[' Node3'][k] == 1:
        busn.append((df['Bus'][k]+"_a").lower())
        Magn.append(df[' Magnitude3'][k])
        Angn.append(df[' Angle3'][k])
    if df[' Node3'][k] == 2:
        busn.append((df['Bus'][k]+"_b").lower())
        Magn.append(df[' Magnitude3'][k])
        Angn.append(df[' Angle3'][k])
    if df[' Node3'][k] == 3:
        busn.append((df['Bus'][k]+"_c").lower())
        Magn.append(df[' Magnitude3'][k])
        Angn.append(df[' Angle3'][k])
    if df[' Node3'][k] == 0:
        if tempnode == 1 and tempnode2 == 0:
            busn.append((tempbus+"_c").lower())
            Magn.append(tempmag)
            Angn.append(tempang+120)
        if tempnode == 2 and tempnode2 == 0:
            busn.append((tempbus+"_c").lower())
            Magn.append(tempmag)
            Angn.append(tempang+240)
        if tempnode == 3 and tempnode2 == 0:
            busn.append((tempbus+"_b").lower())
            Magn.append(tempmag)
            Angn.append(tempang-240)
        if tempnode == 1 and tempnode2 == 2:
            busn.append((tempbus+"_c").lower())
            Magn.append(tempmag)
            Angn.append(tempang+120)
        if tempnode == 1 and tempnode2 == 3:
            busn.append((tempbus+"_b").lower())
            Magn.append(tempmag)
            Angn.append(tempang-120)
        if tempnode == 2 and tempnode2 == 1:
            busn.append((tempbus+"_c").lower())
            Magn.append(tempmag)
            Angn.append(tempang+120)
        if tempnode == 2 and tempnode2 == 3:
            busn.append((tempbus+"_a").lower())
            Magn.append(tempmag)
            Angn.append(tempang+120)
        if tempnode == 3 and tempnode2 == 1:
            busn.append((tempbus+"_b").lower())
            Magn.append(tempmag)
            Angn.append(tempang-240)
        if tempnode == 3 and tempnode2 == 2:
            busn.append((tempbus+"_a").lower())
            Magn.append(tempmag)
            Angn.append(tempang-120)

## Source information  dataframe creation
df9 =DataFrame({'Bus': busn ,'Voltage (V)':Magn,'Angle (deg)':Angn})
df9 = df9[['Bus' ,'Voltage (V)','Angle (deg)' ]]
##


########################################
### Pins spreadsheet creation ####
########################################

### Node Voltages row creation #####
df=pd.read_csv("J1_EXP_VOLTAGES.CSV")
df.shape
Count_Row=df.shape[0]
count=0

Vmag = []
Vang = [] 

for k in range(0,Count_Row):
    tempbus=df['Bus'][k].lower()

    if df[' Node1'][k] == 1:
        Vmag.append((df['Bus'][k].lower()+"_a/Vmag"))
    if df[' Node1'][k] == 2:
        Vmag.append((df['Bus'][k].lower()+"_b/Vmag"))
    if df[' Node1'][k] == 3:
        Vmag.append((df['Bus'][k].lower()+"_c/Vmag"))

    if df[' Node2'][k] == 1:
        Vmag.append((df['Bus'][k].lower()+"_a/Vmag"))
    if df[' Node2'][k] == 2:
        Vmag.append((df['Bus'][k].lower()+"_b/Vmag"))       
    if df[' Node2'][k] == 3:
        Vmag.append((df['Bus'][k].lower()+"_c/Vmag"))

    if df[' Node3'][k] == 1:
        Vmag.append((df['Bus'][k].lower()+"_a/Vmag"))
    if df[' Node3'][k] == 2:
        Vmag.append((df['Bus'][k].lower()+"_b/Vmag"))
    if df[' Node3'][k] == 3:
        Vmag.append((df['Bus'][k].lower()+"_c/Vmag"))


    if df[' Node1'][k] == 1:
        Vang.append((df['Bus'][k].lower()+"_a/Vang"))
    if df[' Node1'][k] == 2:
        Vang.append((df['Bus'][k].lower()+"_b/Vang"))
    if df[' Node1'][k] == 3:
        Vang.append((df['Bus'][k].lower()+"_c/Vang"))

    if df[' Node2'][k] == 1:
        Vang.append((df['Bus'][k].lower()+"_a/Vang"))
    if df[' Node2'][k] == 2:
        Vang.append((df['Bus'][k].lower()+"_b/Vang"))       
    if df[' Node2'][k] == 3:
        Vang.append((df['Bus'][k].lower()+"_c/Vang"))

    if df[' Node3'][k] == 1:
        Vang.append((df['Bus'][k].lower()+"_a/Vang"))
    if df[' Node3'][k] == 2:
        Vang.append((df['Bus'][k].lower()+"_b/Vang"))
    if df[' Node3'][k] == 3:
        Vang.append((df['Bus'][k].lower()+"_c/Vang"))


# Phase Sequence

Vmagnam_a = []
Vmagnam_b = []
Vmagnam_c = []

Vangnam_a = []
Vangnam_b = []
Vangnam_c = []

for k in range(0,Count_Row):
    if df[' Node1'][k] == 1:
        Vmagnam_a.append((df['Bus'][k].lower()+"_a/Vmag"))
    if df[' Node2'][k] == 1:
        Vmagnam_a.append((df['Bus'][k].lower()+"_a/Vmag"))
    if df[' Node3'][k] == 1:
        Vmagnam_a.append((df['Bus'][k].lower()+"_a/Vmag"))

    if df[' Node1'][k] == 2:
        Vmagnam_b.append((df['Bus'][k].lower()+"_b/Vmag"))
    if df[' Node2'][k] == 2:
        Vmagnam_b.append((df['Bus'][k].lower()+"_b/Vmag"))       
    if df[' Node3'][k] == 2:
        Vmagnam_b.append((df['Bus'][k].lower()+"_b/Vmag"))

    if df[' Node1'][k] == 3:
        Vmagnam_c.append((df['Bus'][k].lower()+"_c/Vmag"))
    if df[' Node2'][k] == 3:
        Vmagnam_c.append((df['Bus'][k].lower()+"_c/Vmag"))
    if df[' Node3'][k] == 3:
        Vmagnam_c.append((df['Bus'][k].lower()+"_c/Vmag"))

    if df[' Node1'][k] == 1:
        Vangnam_a.append((df['Bus'][k].lower()+"_a/Vang"))
    if df[' Node2'][k] == 1:
        Vangnam_a.append((df['Bus'][k].lower()+"_a/Vang"))
    if df[' Node3'][k] == 1:
        Vangnam_a.append((df['Bus'][k].lower()+"_a/Vang"))

    if df[' Node1'][k] == 2:
        Vangnam_b.append((df['Bus'][k].lower()+"_b/Vang"))
    if df[' Node2'][k] == 2:
        Vangnam_b.append((df['Bus'][k].lower()+"_b/Vang"))       
    if df[' Node3'][k] == 2:
        Vangnam_b.append((df['Bus'][k].lower()+"_b/Vang"))

    if df[' Node1'][k] == 3:
        Vangnam_c.append((df['Bus'][k].lower()+"_c/Vang"))
    if df[' Node2'][k] == 3:
        Vangnam_c.append((df['Bus'][k].lower()+"_c/Vang"))
    if df[' Node3'][k] == 3:
        Vangnam_c.append((df['Bus'][k].lower()+"_c/Vang"))

frames1 = Vmagnam_a+Vmagnam_b+Vmagnam_c
frames2 = Vangnam_a+Vangnam_b+Vangnam_c


### Line currents row creation #####

# Initialization
q1=0
p=0
Linesd={}

# Open the .dss/.txt file and read each line
f=open("Lines.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Lines.dss", "w")
f.write(processedString)
f.close()

f=open("Services.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Services.dss", "w")
f.write(processedString)
f.close()


# Scan lines of both "Lines.txt" and "Services.txt"
with open("Lines.dss") as f1:
    lines1_1=f1.readlines()
    count4=len(lines1_1)
with open("Services.dss") as f2:
    lines1_2=f2.readlines()
    count5=len(lines1_2)
    lines1=lines1_1+lines1_2
    count6=len(lines1)


q2=0
# Count lines of "Lines.txt" and "Services.txt" q3
for k in range(0, count4):
    if (lines1_1[k].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3_1=q2


q2=0
for k in range(0, count5):
    if (lines1_2[k].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3_2=q2


count=q3_1+q3_2
q3=q3_1+q3_2

s1 = [None] * q3
s2= [None]* q3

# Scan each line and then concatenate/append all the lines following a "New" (which might begin with '~', '!' or ' ') to a single line until another "New" is encountered
# yy is the index
count1=0        
for i in range(0, count6):
    if (lines1[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines1.index(lines1[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count6-1:
        break
    while lines1[p].split()[0][0] == '~' or lines1[p].split()[0][0] == '!' or lines1[p].strip() == '':
          lines1[i]=lines1[i]+lines1[p]
          if p >= count6-1:
              break
          p=p+1


# As q3 is the number of unique "New"s, set s2 is created in order to populate all the lines that begin with "New"    s1[l] is the index where New exists
for l in range(0, q3):
    if "!" in lines1[s1[l]]:
        s2[l]=lines1[s1[l]].split("!")[0]
    else:
        s2[l]=lines1[s1[l]]


for n in range(0,len(s2)):
    line=re.sub(' +',' ',s2[n])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[A-Za-z0-9.\/_-]+', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    nu=len(tokens1)
 
    tokens1 = { x:y for x,y in tokens1}
    tokens1['linenames'] = linenames1
    # create dictionary of lines with length, phases, from bus and to bus information
    Linesd[n]=dict(tokens1)

linename_mag = [None] * len(Linesd)*3
linename_ang = [None] * len(Linesd)*3
for y in range(0,q3_1):
    if 'switch' not in Linesd[y].keys():
        linename_mag[y*3]='line_'+Linesd[y].get('linenames')
        linename_mag[y*3]=(linename_mag[y*3]).lower()
        linename_mag[y*3]=linename_mag[y*3]+'/Imag_0_a'

        linename_mag[y*3+1]='line_'+Linesd[y].get('linenames')
        linename_mag[y*3+1]=(linename_mag[y*3+1]).lower()  
        linename_mag[y*3+1]=linename_mag[y*3+1]+'/Imag_0_b'

        linename_mag[y*3+2]='line_'+Linesd[y].get('linenames')
        linename_mag[y*3+2]=(linename_mag[y*3+2]).lower()  
        linename_mag[y*3+2]=linename_mag[y*3+2]+'/Imag_0_c'

        linename_ang[y*3]='line_'+Linesd[y].get('linenames')
        linename_ang[y*3]=(linename_ang[y*3]).lower()
        linename_ang[y*3]=linename_ang[y*3]+'/Iang_0_a'

        linename_ang[y*3+1]='line_'+Linesd[y].get('linenames')
        linename_ang[y*3+1]=(linename_ang[y*3+1]).lower()  
        linename_ang[y*3+1]=linename_ang[y*3+1]+'/Iang_0_b'

        linename_ang[y*3+2]='line_'+Linesd[y].get('linenames')
        linename_ang[y*3+2]=(linename_ang[y*3+2]).lower()  
        linename_ang[y*3+2]=linename_ang[y*3+2]+'/Iang_0_c'
        
for y in range(0,q3_2):
    linename_mag[y*3+q3_1*3]='line_'+Linesd[y+q3_1].get('bus2').split('.')[0]
    linename_mag[y*3+q3_1*3]=(linename_mag[y*3+q3_1*3]).lower()
    linename_mag[y*3+q3_1*3]=linename_mag[y*3+q3_1*3]+'/Imag_0_a'

    linename_mag[y*3+1+q3_1*3]='line_'+Linesd[y+q3_1].get('bus2').split('.')[0]
    linename_mag[y*3+1+q3_1*3]=(linename_mag[y*3+1+q3_1*3]).lower()  
    linename_mag[y*3+1+q3_1*3]=linename_mag[y*3+1+q3_1*3]+'/Imag_0_b'

    linename_mag[y*3+2+q3_1*3]='line_'+Linesd[y+q3_1].get('bus2').split('.')[0]
    linename_mag[y*3+2+q3_1*3]=(linename_mag[y*3+2+q3_1*3]).lower()  
    linename_mag[y*3+2+q3_1*3]=linename_mag[y*3+2+q3_1*3]+'/Imag_0_c'

    linename_ang[y*3+q3_1*3]='line_'+Linesd[y+q3_1].get('bus2').split('.')[0]
    linename_ang[y*3+q3_1*3]=(linename_ang[y*3+q3_1*3]).lower()
    linename_ang[y*3+q3_1*3]=linename_ang[y*3+q3_1*3]+'/Iang_0_a'

    linename_ang[y*3+1+q3_1*3]='line_'+Linesd[y+q3_1].get('bus2').split('.')[0]
    linename_ang[y*3+1+q3_1*3]=(linename_ang[y*3+1+q3_1*3]).lower()  
    linename_ang[y*3+1+q3_1*3]=linename_ang[y*3+1+q3_1*3]+'/Iang_0_b'

    linename_ang[y*3+2+q3_1*3]='line_'+Linesd[y+q3_1].get('bus2').split('.')[0]
    linename_ang[y*3+2+q3_1*3]=(linename_ang[y*3+2+q3_1*3]).lower()  
    linename_ang[y*3+2+q3_1*3]=linename_ang[y*3+2+q3_1*3]+'/Iang_0_c'

### Loads row creation #####

q1=0
q2=0
q3=0
p=0
Load1={}

fd = open("LoadsInd.dss")
contents = fd.readlines()
fd.close()

new_contents = []
for line in contents:
    if not line.strip():
        continue
    else:
        new_contents.append(line)

f=open("LoadsInd.dss", "w")
f.write("".join(new_contents))
f.close()


with open("LoadsInd.dss") as f3:
    lines11=f3.readlines()
    count=len(lines11)

for l in range(0, count):
    lines11[l]=' '.join(lines11[l].split())
    if (lines11[l].split(' ')[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2
        s1 = [None]* q3
        s2= [None]* q3

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
qw=[None]*fr
tokens2=[None]*fr
for j in range(0,fr):
    line=re.sub(' +',' ',s2[j])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[1]
    tokens1 = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[A-Za-z0-9.\/_-]+', line)
    tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
    # Find the 'item' phases's location that is used to find the number of phases later by getting the 'value'
    name ='phases'
    list = tokens1

    new_list=[]
    for item in list:
        new_list.append(item[0])
    loc= new_list.index(name)
    for h in range(0,len(tokens1)):
        if tokens1[loc][1] =='1':
            if tokens1[h][0] =='bus':
                yr1=tokens1[h][1].split('.')[0]
                yr2=tokens1[h][1].split('.')[1]
#                yr1=tokens1[h][1].split('-')[0]
#                yr2=tokens1[h][1].split('-')[1]
            if tokens1[h][0] =='kV':
                yr3=float (tokens1[h][1])
            if tokens1[h][0] =='kW':
                yr4=float (tokens1[h][1])
            if tokens1[h][0] =='kvar' or 'pf':
                if tokens1[h][0]=='kvar':
                    yr5=float (tokens1[h][1])
                if tokens1[h][0]=='pf':
                    yr5=((yr4/float (tokens1[h][1]))**2 - (yr4)**2)**0.5

        else:
            if tokens1[h][0] =='bus':
                yr1=tokens1[h][1].split('.')[0]
#                yr1=tokens1[h][1]
                yr2='threephase'
            if tokens1[h][0] =='kV':
                yr3=float (tokens1[h][1])
            if tokens1[h][0] =='kW':
                yr4=float (tokens1[h][1])
            if tokens1[h][0] =='kvar' or 'pf':
                if tokens1[h][0]=='kvar':
                    yr5=float (tokens1[h][1])
                if tokens1[h][0]=='pf':
                    yr5=((yr4/float (tokens1[h][1]))**2 - (yr4)**2)**0.5

    hr[j]='Bus='+yr1+' '+'Phase='+yr2+' '+'kv='+str(yr3)+' '+'kw='+str(yr4)+' '+'kvar='+str(yr5)
    qw[j]=yr1
    tokens2[j] = re.findall(r'[\w\.\_]+[\ ]*=[\ ]*[\w\.\_\-\c]+', hr[j])
    tokens2[j] = [x.replace(" ", "").split('=') for x in tokens2[j]]
    tokens2[j][2][1] = float (tokens2[j][2][1])
    tokens2[j][3][1] = float (tokens2[j][3][1])
    tokens2[j][4][1] = float (tokens2[j][4][1])
    tokens2[j] = { x:y for x,y in tokens2[j]}
    Load1[j]=dict(tokens2[j])


ID_load=[]
for i in range(0,len(Load1)):
    if (Load1[i].get('Phase')) == 'threephase':
        temp=(Load1[i].get('Bus'))
        temp3="load_"+temp
        ID_load.append((temp3.lower()+'/P_a'))
        ID_load.append((temp3.lower()+'/Q_a'))
        ID_load.append((temp3.lower()+'/P_b'))   
        ID_load.append((temp3.lower()+'/Q_b'))
        ID_load.append((temp3.lower()+'/P_c'))   
        ID_load.append((temp3.lower()+'/Q_c'))
        
    elif (Load1[i].get('Phase')) == '1':
        temp=(Load1[i].get('Bus'))
        temp3="load_"+temp
        ID_load.append((temp3.lower()+'/P_a'))
        ID_load.append((temp3.lower()+'/Q_a'))

    elif (Load1[i].get('Phase')) == '2':
        temp=(Load1[i].get('Bus'))
        temp3="load_"+temp
        ID_load.append((temp3.lower()+'/P_b'))   
        ID_load.append((temp3.lower()+'/Q_b'))

    elif (Load1[i].get('Phase')) == '3':
        temp=(Load1[i].get('Bus'))
        temp3="load_"+temp
        ID_load.append((temp3.lower()+'/P_c'))   
        ID_load.append((temp3.lower()+'/Q_c'))
 

import pandas

original = pandas.DataFrame({
    'Vmag':Vmag, 
    'Vang':Vang
    })
original = original[['Vmag','Vang' ]]


original1 = pandas.DataFrame({
    'linemag':linename_mag, 
    'lineang':linename_ang
    })
original1 = original1[['linemag','lineang' ]]

original2 = pandas.DataFrame({
    'loadid':ID_load
    })
original2 = original2[['loadid' ]]


### Regulating Transformers row creation #####
# Initialization
q1=0
q2=0
p=0
LineCodesd={}
kf2mil=0.189394
km2mil=0.621371
f2mil=0.000189394
mil2mil=1
m2mil=0.000621371

# Import of differnt operations 
import re
import numpy as np
import pandas as pd
from itertools import chain
from pandas import DataFrame
Linesd={}

# Open the .dss/.dss file and read each line
f=open("Substation.dss", "r")
fileString = f.read()
f.close()
processedString = re.sub("\n\s*\n*", "\n", fileString)
f=open("Substation.dss", "w")
f.write(processedString)
f.close()

# Scan lines of both "Lines.dss" and "Services.dss"
with open("Substation.dss") as f1:
    lines1_1=f1.readlines()
    count4=len(lines1_1)
with open("Regulators_mod.dss") as f2:
    lines1_2=f2.readlines()
    lines1=lines1_1+lines1_2
    count=len(lines1)

# Count lines of "Lines.dss" and "Services.dss" q3
for k in range(0, count):
    if (lines1[k].split(" ")[0].split(".")[0]) == 'New':
        q2=q2+1
        q3=q2

s1 = [None] * q3
s2= [None]* q3

# Scan each line and then concatenate/append all the lines following a "New" (which might begin with '~', '!' or ' ') to a single line until another "New" is encountered 
count1=0        
for i in range(0, count):
    if (lines1[i].split(" ")[0].split(".")[0]) == 'New':
        yy=lines1.index(lines1[i])
        p=i+1
        q1=q1+1
        s1[count1]=yy
        count1+=1
    if i >= count-1:
        break
    while lines1[p].split()[0][0] == '~' or lines1[p].split()[0][0] == '!' or lines1[p].strip() == '':
          lines1[i]=lines1[i]+lines1[p]
          if p >= count-1:
              break
          p=p+1
          
# As q3 is the number of unique "New"s, set s2 is created in order to populate all the lines that begin with "New"    
for l in range(0, q3):
    s2[l]=lines1[s1[l]]

fr=len(s2)
hr=[None]*fr
qw1=[None]*fr
tokens2=[None]*fr
Trans3={}
tokens4=[]
tokens3={}
print fr
sd=0
for ty in range(0,fr):
    line=re.sub(' +',' ',s2[ty])
    linenames1 = re.findall(r'New[\t ]+([A-Za-z0-9.\/_-]+)', line)
    linenames1=linenames1[0].split(".")[0]

    if linenames1 == "Transformer":
        
        tokens1 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\d]?[.]?\d*[A-Za-z0-9.\/_,-]+?', line)
        tokens1 = [x.replace(" ", "").split('=') for x in tokens1]
           
        tokens2 = re.findall(r'[\?%\w\.\_]+[\ ]*=[[(]?[\s]?\d*[A-Za-z0-9.\/_,-]+[\s]?[\,][\s]?\d*[A-Za-z0-9.\/_,-]+[\s]??[])]?', line)
        tokens2 = [x.replace(" ", "").split('=') for x in tokens2]


        tokens1=(tokens2+tokens1)
            
        for h in range(0,len(tokens1)):
            if tokens1[h][0] =='xhl':
                for h in range(0,len(tokens1)):
                    if tokens1[h][0] =='buses':
                        sd1=tokens1[h][1]
                        yr1=sd1.split(",")[0].split("(")[1].split(".")[0]
                        yr4=sd1.split(",")[1].split(")")[0].split(".")[0]
                        if "." in sd1.split(",")[1].split(")")[0]:
                            yr41=sd1.split(",")[1].split(")")[0].split(".")[1]
                        else:
                            yr41='threephase'

            if tokens1[h][0] == '%loadloss':
                for h in range(0,len(tokens1)):
                    if tokens1[h][0] =='buses':
                        sd1=tokens1[h][1]
                        yr1=sd1.split(",")[0].split("(")[1].split(".")[0]
                        yr4=sd1.split(",")[1].split(")")[0].split(".")[0]
                        if "." in sd1.split(",")[1].split(")")[0]:
                            yr41=sd1.split(",")[1].split(")")[0].split(".")[1]
                        else:
                            yr41='threephase'


        qw2=yr1+'*'+yr4
        hr='Busl='+qw2+' '+'Bus2='+yr4+' '+'phase='+yr41
        print hr
        tokens2 = re.findall(r'[\?%\w\.\_]+[\ ]*=[\ ]*[\w\.\_\*]+', hr)
        tokens2 = [x.replace(" ", "").split('=') for x in tokens2]
        tokens3[sd]={ x:y for x,y in tokens2}
        print tokens3[sd]
        Trans3[sd]=dict(tokens3[sd])
        sd=sd+1

print Trans3


ID_tf=[]
for i in range(0,len(Trans3)):
    if (Trans3[i].get('phase')) == 'threephase':
        temp=(Trans3[i].get('Busl'))
        temp1=temp.split("*")[0]
        temp2=temp.split("*")[1]
        temp3="VR_"+temp1+"_"+temp2
        ID_tf.append((temp3.lower()+'/tap_a'))
        ID_tf.append((temp3.lower()+'/tap_b'))   
        ID_tf.append((temp3.lower()+'/tap_c'))
        
    elif (Trans3[i].get('phase')) == '1':
        temp=(Trans3[i].get('Busl'))
        temp1=temp.split("*")[0]
        temp2=temp.split("*")[1]
        temp3="VR_"+temp1+"_"+temp2
        ID_tf.append((temp3.lower()+'/tap_a'))

    elif (Trans3[i].get('phase')) == '2':
        temp=(Trans3[i].get('Busl'))
        temp1=temp.split("*")[0]
        temp2=temp.split("*")[1]
        temp3="VR_"+temp1+"_"+temp2
        ID_tf.append((temp3.lower()+'/tap_b'))

    elif (Trans3[i].get('phase')) == '3':
        temp=(Trans3[i].get('Busl'))
        temp1=temp.split("*")[0]
        temp2=temp.split("*")[1]
        temp3="VR_"+temp1+"_"+temp2
        ID_tf.append((temp3.lower()+'/tap_c'))        


original3 = pandas.DataFrame({
    'tfid':ID_tf
    })
original3 = original3[['tfid' ]]

original4 = pandas.DataFrame({
    'loadid':ID_load
    })
original4 = original4[['loadid' ]]


original5 = pandas.DataFrame({
    'frames1':frames1
    })
original5 = original5[['frames1' ]]
print original5

original6 = pandas.DataFrame({
    'frames2':frames2
    })
original6 = original6[['frames2' ]]

new = pandas.concat([original, original1, original2,original3,original4,original5,original6], ignore_index=False, axis=1)

## End

## Data frame for Pins information
df10 = new.T
##############

#############################################
### Voltage results spreadsheet creation ####
#############################################

### Node Voltages row creation #####


df=pd.read_csv("J1_EXP_VOLTAGES.CSV")
df.shape
Count_Row=df.shape[0]
count=0

Vmag = []
Vang = []
Vbase= []

for k in range(0,Count_Row):
    tempbus=df['Bus'][k].lower()

    if df[' Node1'][k] == 1:
        Vmag.append(df[' pu1'][k])
    if df[' Node1'][k] == 2:
        Vmag.append(df[' pu1'][k])
    if df[' Node1'][k] == 3:
        Vmag.append(df[' pu1'][k])

    if df[' Node2'][k] == 1:
        Vmag.append(df[' pu2'][k])
    if df[' Node2'][k] == 2:
        Vmag.append(df[' pu2'][k])       
    if df[' Node2'][k] == 3:
        Vmag.append(df[' pu2'][k])

    if df[' Node3'][k] == 1:
        Vmag.append(df[' pu3'][k])
    if df[' Node3'][k] == 2:
        Vmag.append(df[' pu3'][k])
    if df[' Node3'][k] == 3:
        Vmag.append(df[' pu3'][k])


    if df[' Node1'][k] == 1:
        Vang.append(df[' Angle1'][k])
    if df[' Node1'][k] == 2:
        Vang.append(df[' Angle1'][k])
    if df[' Node1'][k] == 3:
        Vang.append(df[' Angle1'][k])

    if df[' Node2'][k] == 1:
        Vang.append(df[' Angle2'][k])
    if df[' Node2'][k] == 2:
        Vang.append(df[' Angle2'][k])       
    if df[' Node2'][k] == 3:
        Vang.append(df[' Angle2'][k])

    if df[' Node3'][k] == 1:
        Vang.append(df[' Angle3'][k])
    if df[' Node3'][k] == 2:
        Vang.append(df[' Angle3'][k])
    if df[' Node3'][k] == 3:
        Vang.append(df[' Angle3'][k])

    if df[' Node1'][k] == 1:
        Vbase.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node1'][k] == 2:
        Vbase.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node1'][k] == 3:
        Vbase.append(df[' BasekV'][k]*1000/1.732)

    if df[' Node2'][k] == 1:
        Vbase.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node2'][k] == 2:
        Vbase.append(df[' BasekV'][k]*1000/1.732)       
    if df[' Node2'][k] == 3:
        Vbase.append(df[' BasekV'][k]*1000/1.732)

    if df[' Node3'][k] == 1:
        Vbase.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node3'][k] == 2:
        Vbase.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node3'][k] == 3:
        Vbase.append(df[' BasekV'][k]*1000/1.732)        


# Phase sequence

Vmag_a = []
Vmag_b = []
Vmag_c = []

Vang_a = []
Vang_b = []
Vang_c = []

Vbase_a = []
Vbase_b = []
Vbase_c = []

for k in range(0,Count_Row):
    if df[' Node1'][k] == 1:
        Vmag_a.append(df[' pu1'][k])
    if df[' Node2'][k] == 1:
        Vmag_a.append(df[' pu2'][k])
    if df[' Node3'][k] == 1:
        Vmag_a.append(df[' pu3'][k])

    if df[' Node1'][k] == 2:
        Vmag_b.append(df[' pu1'][k])
    if df[' Node2'][k] == 2:
        Vmag_b.append(df[' pu2'][k])       
    if df[' Node3'][k] == 2:
        Vmag_b.append(df[' pu3'][k])

    if df[' Node1'][k] == 3:
        Vmag_c.append(df[' pu1'][k])
    if df[' Node2'][k] == 3:
        Vmag_c.append(df[' pu2'][k])
    if df[' Node3'][k] == 3:
        Vmag_c.append(df[' pu3'][k])
        
for k in range(0,Count_Row):
    if df[' Node1'][k] == 1:
        Vang_a.append(df[' Angle1'][k])
    if df[' Node2'][k] == 1:
        Vang_a.append(df[' Angle2'][k])
    if df[' Node3'][k] == 1:
        Vang_a.append(df[' Angle3'][k])

    if df[' Node1'][k] == 2:
        Vang_b.append(df[' Angle1'][k])
    if df[' Node2'][k] == 2:
        Vang_b.append(df[' Angle2'][k])       
    if df[' Node3'][k] == 2:
        Vang_b.append(df[' Angle3'][k])

    if df[' Node1'][k] == 3:
        Vang_c.append(df[' Angle1'][k])
    if df[' Node2'][k] == 3:
        Vang_c.append(df[' Angle2'][k])
    if df[' Node3'][k] == 3:
        Vang_c.append(df[' Angle3'][k])        

for k in range(0,Count_Row):
    if df[' Node1'][k] == 1:
        Vbase_a.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node2'][k] == 1:
        Vbase_a.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node3'][k] == 1:
        Vbase_a.append(df[' BasekV'][k]*1000/1.732)

    if df[' Node1'][k] == 2:
        Vbase_b.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node2'][k] == 2:
        Vbase_b.append(df[' BasekV'][k]*1000/1.732)       
    if df[' Node3'][k] == 2:
        Vbase_b.append(df[' BasekV'][k]*1000/1.732)

    if df[' Node1'][k] == 3:
        Vbase_c.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node2'][k] == 3:
        Vbase_c.append(df[' BasekV'][k]*1000/1.732)
    if df[' Node3'][k] == 3:
        Vbase_c.append(df[' BasekV'][k]*1000/1.732)

Vmag_phas=Vmag_a+Vmag_b+Vmag_c
Vang_phas=Vang_a+Vang_b+Vang_c
Vbase_phas=Vbase_a+Vbase_b+Vbase_c

import pandas

original = pandas.DataFrame({
    'Vmag':Vmag, 
    'Vang':Vang,
    'Vbase':Vbase,
    'Vmag_phas':Vmag_phas,
    'Vang_phas':Vang_phas,
    'Vbase_phas':Vbase_phas    
    })
original = original[['Vmag','Vang','Vbase','Vmag_phas','Vang_phas','Vbase_phas' ]]

## End

## Data frame for Pins information
df11 = original.T
##

writer = pd.ExcelWriter("test3_new.xlsx", engine='xlsxwriter')
df1.to_excel(writer,'Line 3-phase',index=False)
workbook  = writer.book
worksheet = writer.sheets['Line 3-phase']

worksheet.set_column(0, 25, 16)


df2.to_excel(writer,'Switch',index=False)
workbook  = writer.book
worksheet = writer.sheets['Switch']

worksheet.set_column(0, 3, 16)

df3.to_excel(writer,'Load 3-phase',index=False)
workbook  = writer.book
worksheet = writer.sheets['Load 3-phase']

worksheet.set_column(0, 19, 16)

df4.to_excel(writer,'Transformer 3-phase',index=False)
workbook  = writer.book
worksheet = writer.sheets['Transformer 3-phase']

worksheet.set_column(0, 19, 16)

df5.to_excel(writer,'Shunt 3-phase',index=False)
workbook  = writer.book
worksheet = writer.sheets['Shunt 3-phase']

worksheet.set_column(0, 19, 16)

df6.to_excel(writer,'Bus Faults 3-phase',index=False)
workbook  = writer.book
worksheet = writer.sheets['Bus Faults 3-phase']

worksheet.set_column(0, 25, 16)

df7.to_excel(writer,'Vsource 3-phase',index=False)
workbook  = writer.book
worksheet = writer.sheets['Vsource 3-phase']

worksheet.set_column(0, 25, 16)

df8.to_excel(writer,'Current Injector',index=False)
workbook  = writer.book
worksheet = writer.sheets['Current Injector']

worksheet.set_column(0, 2, 16)

df9.to_excel(writer,'Bus',index=False)
workbook  = writer.book
worksheet = writer.sheets['Bus']

worksheet.set_column(0, 3, 16)


df10.to_excel(writer,'Pins',index=False)
workbook  = writer.book
worksheet = writer.sheets['Pins']

worksheet.set_column(0, 2, 16)

df11.to_excel(writer,'vresults',index=False)
workbook  = writer.book
worksheet = writer.sheets['vresults']

worksheet.set_column(0, 2, 16)


writer.save()

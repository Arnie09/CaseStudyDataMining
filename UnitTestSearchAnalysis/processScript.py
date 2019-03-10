import pandas as pd
import xlrd
import os
import sys
import openpyxl

outputpath = os.path.join(sys.path[0])
path = os.path.join(sys.path[0],'UT_Data.xlsx')

df=pd.read_excel(path)
df.set_index('Roll No.',inplace=True)
df=df.drop(columns = ['Name','Total (30)','No. of Classes Present (19) till 31.03.2017','Attd.   (5)','CS201  (15)', 'CS201  (15).1',])
df=df.drop([7,42,49])

data={}
for i in df.columns:
    data[i]=[]

for i in df.index:
    score=""
    atd=df.loc[i]['% of Attendance till 31.03.2017']
    if atd>=80:
        score="Good Attendance"
    elif atd>=60:
        score="Average Attendance"
    else:
        score="Bad Attendance"
    
    data['% of Attendance till 31.03.2017'].append(score)

    marks=df.loc[i]['UT_MAX (15)']
    if marks>=12:
        score="Good UT marks"
    elif marks>=9:
        score="Average UT marks"
    else:
        score="Bad UT marks"
    data['UT_MAX (15)'].append(score)

    cf=df.loc[i]['Class Performance (10)']
    if cf>=8:
        score="Good Class Performance"
    elif cf>=6:
        score="Average Class Performance"
    else:
        score="Bad Class Performance"

    data['Class Performance (10)'].append(score)

    total=df.loc[i]['Total (30).1']
    if total>=24:
        score="Good Internal Marks"
    elif total>=18:
        score="Average Internal marks"
    else:
        score="Bad Internal marks"

    data['Total (30).1'].append(score)

DF=pd.DataFrame.from_dict(data)
DF.index.name="RollNo."
DF.to_excel(os.path.join(sys.path[0],"MainData.xlsx"))

import pandas as pd
import xlrd
import os
import sys

outputpath = os.path.join(sys.path[0])
path1 = os.path.join(sys.path[0],'UnprocessedData/2ndSem_data.csv')
path2 = os.path.join(sys.path[0],'UnprocessedData/3rdSem_data.csv')
path3 = os.path.join(sys.path[0],'UnprocessedData/4thSem_data.csv')
path4 = os.path.join(sys.path[0],'UnprocessedData/5thSem_data.csv')
path5 = os.path.join(sys.path[0],'UnprocessedData/6thSem_data.csv')

dataset1 = pd.read_csv(path1)
dataset2 = pd.read_csv(path2)
dataset3 = pd.read_csv(path3)
dataset4 = pd.read_csv(path4)
dataset5 = pd.read_csv(path5)

dataset1.set_index(' ROLL NO. ',inplace  = True)
dataset2.set_index(' ROLL NO. ',inplace  = True)
dataset3.set_index(' ROLL NO. ',inplace  = True)
dataset4.set_index(' ROLL NO. ',inplace  = True)
dataset5.set_index('ROLL NO.',inplace  = True) 

'''dropping unnecessary headers'''
dataset1  = dataset1.drop(columns = ['Unnamed: 0',' SGPA1 ', ' SGPA2 ',' YGPA ', ' DGPA ', ' RESULT '])
dataset2 = dataset2.drop(columns = ['Unnamed: 0',' SGPA '])
dataset3  = dataset3.drop(columns = ['Unnamed: 0',' SGPA3 ', ' SGPA4 ',' YGPA ', ' DGPA ', ' RESULT '])
dataset4 = dataset4.drop(columns = ['Unnamed: 0',' SGPA '])
dataset5  = dataset5.drop(columns = ['Unnamed: 0','SGPA5', 'SGPA6', 'YGPA','RESULT'])

subjectslist = []
subjectslist.append(list(dataset1.columns.values))
subjectslist.append(list(dataset2.columns.values))
subjectslist.append(list(dataset3.columns.values))
subjectslist.append(list(dataset4.columns.values))
subjectslist.append(list(dataset5.columns.values))

marks = {'O':10,'E':9,'A':8,'B':7,'C':6,'D':5,'F':4,'I':3}

listOfDataFrames = []
listOfDataFrames.append( dataset1)
listOfDataFrames.append( dataset2)
listOfDataFrames.append( dataset3)
listOfDataFrames.append( dataset4)
listOfDataFrames.append( dataset5)


for i in range (0,5):
    for subjects in subjectslist[i]:
        x = 0
        for j in listOfDataFrames[i][subjects]:
            listOfDataFrames[i][subjects][x:x+1] = listOfDataFrames[i][subjects][x:x+1].str.replace(j,str(marks[j]))
            x+=1

'''creating subjects list'''
subjectsfordataframe = list(dataset1.columns.values)+list(dataset2.columns.values)+list(dataset3.columns.values)+list(dataset4.columns.values)+list(dataset5.columns.values)
print(len(subjects))


# data = [{'b': 2, 'c':3}, {'a': 10, 'b': 20, 'c': 30}] 
  
# # Creates padas DataFrame by passing  
# # Lists of dictionaries and row index. 
# df = pd.DataFrame(data, index =['first', 'second']) 
data = {}
rollNo = list(listOfDataFrames[0].index)

#print(listOfDataFrames[0].loc[rollNo[0]]['CS201'])
for students in rollNo:
    try: 
        #print(students)
        marks = []
        for i in range(0,5):
            
            for subjects in subjectslist[i]:
                #print(subjects," ",listOfDataFrames[i].loc[students][subjects],end = " ")
                marks.append(listOfDataFrames[i].loc[students][subjects])
        data[students] = marks
    except:
        continue        
            
            
# for i in data:
#     print(i," : ",data[i])

DATAFRAME = pd.DataFrame.from_dict(data,orient = "index",columns = subjectsfordataframe)
DATAFRAME.to_csv(os.path.join(sys.path[0],"MainData.csv"))
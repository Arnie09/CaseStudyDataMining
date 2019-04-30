import pandas as pd
import os
import sys
import openpyxl

dataFrame = pd.read_excel((os.path.join(sys.path[0],'ManipulatedDataset2.xlsx')))
dataFrame.set_index('RollNo.',inplace  = True)
MAIN_LIST={}
SUBJECTS = list(dataFrame.columns)

'''filling up the dictionary with empty lists'''
for students in dataFrame.index:
    MAIN_LIST[students] = []

'''grouping of marks into good,average,poor based on the higest and lowest in the subjects is done here'''
for subjects in SUBJECTS:
    marks = sorted(dataFrame[subjects])
    min,max = marks[0], marks[len(marks)-1]
    diff= (max-min)/3
    for students in dataFrame.index:
        scores = ""
        marks = dataFrame.loc[students][subjects]
        String = ""
        if(marks>=max - diff):
            String = "Good"
        elif(marks>= min+diff and marks<max-diff):
            String = "Average"
        else:
            String = "Poor"
        scores = String
        MAIN_LIST[students].append(scores)

df = pd.DataFrame.from_dict(MAIN_LIST,orient = "index",columns = SUBJECTS)
df.index.name = "Roll No"
df.to_excel(os.path.join(sys.path[0],'ProcessedData.xlsx'))

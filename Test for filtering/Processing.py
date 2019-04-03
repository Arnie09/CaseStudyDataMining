import pandas as pd
import os
import sys
import openpyxl

from  FP_Growth import FP_Tree
dataFrame = pd.read_excel((os.path.join(sys.path[0],'MainData.xlsx')))
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
            String = "Good marks in "
        elif(marks>= min+diff and marks<max-diff):
            String = "Average marks in "
        else:
            String = "Poor marks in "
        scores = (String+subjects)
        MAIN_LIST[students].append(scores)

df = pd.DataFrame.from_dict(MAIN_LIST,orient = "index",columns = SUBJECTS)
df.index.name = "Roll No"
df.to_excel(os.path.join(sys.path[0],'ProcessedData.xlsx'))

'''old technique where we decided the good,average and poor'''
# print(MAIN_LIST)
# for students in dataFrame.index:
#     scores = []
#     for subject in SUBJECTS:
#
#         marks = dataFrame.loc[students][subject]
#         String = ""
#         if(marks>=8):
#             String = "Good marks in "
#         elif(marks>=6 and marks<8):
#             String = "Average marks in "
#         else:
#             String = "Poor marks in "
#         scores.append((String+subject))
#     MAIN_LIST[students] = scores

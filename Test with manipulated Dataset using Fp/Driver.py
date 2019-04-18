#loading dependancies
import pandas as pd
import os
import sys
import openpyxl

#loading function
from  FP_Growth import FP_Tree

#loading dataSet
dataset = pd.read_excel((os.path.join(sys.path[0],'ProcessedData.xlsx')))

#making dictionary of transactions
MAIN_LIST = {}
#MAIN_LIST.fill([])
for index in dataset.index:
    MAIN_LIST[index] = []
    MAIN_LIST[index].append(dataset.loc[index]['Data Structure & Algorithm'])
    MAIN_LIST[index].append(dataset.loc[index]['Design & Analysis of Algorithm'])
    MAIN_LIST[index].append(dataset.loc[index]['Object Oriented Programming'])
    MAIN_LIST[index].append(dataset.loc[index]['Introduction to Computing'])
#print(MAIN_LIST)
FptreeObject = FP_Tree(min = 6,transactions = MAIN_LIST)
FptreeObject.displayRules(conf=0.5)
rules = FptreeObject.finalRules
for i in rules:
    if ("Computing" not in i[0] and "Computing" not in i[1]) or 1:
        print(i[0],'=>',i[1],":",str(round(i[2]))+"%")

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

#print(MAIN_LIST)

FptreeObject = FP_Tree(min = 1,transactions = MAIN_LIST)
FptreeObject.displayRules(confmin=0.0,confmax = 1.0)
rules = FptreeObject.rulesMainDict
for rule in  rules:
    #print((rule))
    if('Data Structure & Algorithm' in rule and 'Design & Analysis of Algorithm' in rule and 'Object Oriented Programming' in rules[rule]):
        print(rule+" : "+rules[rule])
    # for elements in rule:
    #     print(elements)
    #     if ('Computer Organisation' in elements):
    #         print(rule+":"+rules[rule])

#loading dependancies
import pandas as pd
import os
import sys
import openpyxl

#loading function
from  FP_Growth import FP_Tree
from Apriori_core import apriori

#loading dataSet
dataset = pd.read_excel((os.path.join(sys.path[0],'ProcessedData.xlsx')))

#making dictionary of transactions
MAIN_LIST = {}

dataset.set_index('Roll No',inplace = True)
subjects = list(dataset.columns)
#subjects = ['Data Structure & Algorithm','Design & Analysis of Algorithm','Object Oriented Programming']
subjects_to_be_analysed = []

for items in subjects:
    subjects_to_be_analysed.append('Good marks in '+items)
    subjects_to_be_analysed.append('Average marks in '+items)
    subjects_to_be_analysed.append('Poor marks in '+items)
#subjects_to_be_analysed = ['Good marks in Data Structure & Algorithm','Good marks in Design & Analysis of Algorithm','Good marks in Object Oriented Programming']

for index in dataset.index:
    MAIN_LIST[index] = []
    # MAIN_LIST[index].append(dataset.loc[index]['Data Structure & Algorithm'])
    # MAIN_LIST[index].append(dataset.loc[index]['Design & Analysis of Algorithm'])
    # MAIN_LIST[index].append(dataset.loc[index]['Object Oriented Programming'])
    # MAIN_LIST[index].append(dataset.loc[index]['Introduction to Computing'])
    for each_subjects in subjects:
        MAIN_LIST[index].append(dataset.loc[index][each_subjects])

    #MAIN_LIST[index].append(dataset.loc[index]['Introduction to Computing'])
    # MAIN_LIST[index].append(dataset.loc[index]['Analog & Digital Electronics'])
    # MAIN_LIST[index].append(dataset.loc[index]['Computer Organisation'])
    # MAIN_LIST[index].append(dataset.loc[index]['Numerical Methods'])
    # MAIN_LIST[index].append(dataset.loc[index]['Communication Engg & Coding Theory'])
    # MAIN_LIST[index].append(dataset.loc[index]['Formal Language & Automata Theory'])

# for index in dataset.index:
#     MAIN_LIST[index] = []
#     for each_subjects in subjects:
#         MAIN_LIST[index].append(dataset.loc[index][each_subjects])

# print(dataset.loc[10900113101]['Numerical Methods'])
# FptreeObject = FP_Tree(min = 1,transactions = MAIN_LIST)
# FptreeObject.displayRules(confmin=0.0,confmax = 1.0)
# rules = FptreeObject.rulesMainDict
# for rule in  rules:
#     if('Data Structure & Algorithm' in rule and 'Design & Analysis of Algorithm' in rule and 'Object Oriented Programming' in rules[rule] and rule.count(',') == 1 and rules[rule].count(',') == 0):
#         print(rule+" : "+rules[rule])

AprioriObject = apriori(min = 15,transactions = MAIN_LIST,productlist = subjects_to_be_analysed,rulesMin = 0.1)

for items in AprioriObject.finalRules:
    if(items == 3):
        for rules in AprioriObject.finalRules[items]:
            left_part,right_part = rules.split('=>')
            if('Data Structure & Algorithm' in left_part and 'Design & Analysis of Algorithm' in left_part and 'Object Oriented Programming' in right_part):
                print(rules)

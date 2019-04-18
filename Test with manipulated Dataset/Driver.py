#loading dependancies
import pandas as pd
import os
import sys
import openpyxl
import re

#loading function
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


for index in dataset.index:
    MAIN_LIST[index] = []
    for each_subjects in subjects:
        MAIN_LIST[index].append(dataset.loc[index][each_subjects])


AprioriObject = apriori(min = 15,transactions = MAIN_LIST,productlist = subjects_to_be_analysed,rulesMin = 0.1,rules_len = 3)

PATTERNS = ["Good marks in ","Average marks in ","Poor marks in "]

relations = {}

for items in AprioriObject.finalRules:
    if(items == 3):
        for rules in AprioriObject.finalRules[items]:
            #print(rules)
            main_stuff = rules
            rules,percentage = rules.split(": ")
            left_part,right_part = rules.split('=>')
            left_part = left_part[1:-1]
            right_part = right_part[1:-1]
            left_part = left_part.split(", ")
            right_part = right_part.split(", ")
            left_subjects = []
            right_subjects = []
            #print(left_part,right_part)
            for items_ in left_part:
                for pattern in PATTERNS:
                    if(re.search(pattern,items_)):
                        left_subjects.append(items_.replace(pattern,""))
            for items_ in right_part:
                for pattern in PATTERNS:
                    if(re.search(pattern,items_)):
                        right_subjects.append(items_.replace(pattern,""))


            subjects_in_this_rule = tuple(sorted([subject for subject in left_subjects]+[subject for subject in right_subjects]))

            #print(subjects_in_this_rule)
            if(float(percentage[:-1])>90):
                if(subjects_in_this_rule not in relations):
                    #print("The relations between :",subjects_in_this_rule," are --- ")
                    relations[subjects_in_this_rule] = [main_stuff]
                else:
                    relations[subjects_in_this_rule].append(main_stuff)

for subjects in relations:
    if(len(relations[subjects])>2):
        for items in relations[subjects]:
            print(items)
        print()

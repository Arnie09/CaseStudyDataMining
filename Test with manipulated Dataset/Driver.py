'''loading dependancies'''
import pandas as pd
import os
import sys
import openpyxl
import re

'''loading function'''
from Apriori_core import apriori

'''loading dataSet'''
dataset = pd.read_excel((os.path.join(sys.path[0],'ProcessedData.xlsx')))

'''making dictionary of transactions'''
MAIN_LIST = {}

'''Setting index and storing the names of all subjects as a list in 'subjects' '''
dataset.set_index('Roll No',inplace = True)
subjects = list(dataset.columns)

'''subjects_to_be_analysed will contain all possible scenarios of text that our dataset has.
The algorithm works on similar entry datas and since our data set contain the phrases "Good/Average/Poor marks in " before
the name of every subject hence this step has to be done to create a list of all possible data entries which may be present in our dataSet
and we need to send over this list to the Apriori object'''

subjects_to_be_analysed = []
for items in subjects:
    subjects_to_be_analysed.append('Good marks in '+items)
    subjects_to_be_analysed.append('Average marks in '+items)
    subjects_to_be_analysed.append('Poor marks in '+items)

'''MAIN_LIST is a dictionary that contains all the transactions that are present in our dataset which needs to be sent as
an argument for Apriori object'''

for index in dataset.index:
    MAIN_LIST[index] = []
    for each_subjects in subjects:
        MAIN_LIST[index].append(dataset.loc[index][each_subjects])


'''Initialising the Apriori Object with the following arguments :
    min : the minimum number of rows in which the specific data needs to be present in, inorder to consider it for furthur evaluation,i.e,
          in other word, the frequency of the item in the list.
    transaction : The dictionary containing all the transactions present in the dataset
    productlist : The list containing all the data entries that are present in the dataset which we had aldready found out and stored if in
                  subjects_to_be_analysed
    rulesMin : The minimum percentage in decimals of the rule that the rule needs to qualify as in order to be considdered as a part of the
               result
    rules_len : The maximum length each rule can have. This argument simply halps to save time as longer rules are not evaluated which are
                necessarily not useful'''

AprioriObject = apriori(min = 15,transactions = MAIN_LIST,productlist = subjects_to_be_analysed,rulesMin = 0.1,rules_len = 4)

'''A list containg the texts which are useful for searching in a text for filtering purposes'''

PATTERNS = ["Good marks in ","Average marks in ","Poor marks in "]

''' A dictionary which stores the name of the subject as keys and their occurence in the course as the value which means courses in the
    first semester will have lower number than courses in the later part of the curriculum'''
Chronological_order = {}
count = 0
for subject in subjects:
    Chronological_order[subject] = count
    count+=1

''' A dictionary that will store all the valid rules'''
relations = {}

'''We loop over every key of the rules. We ignore the rules of length > 3 (which are not calculated anyway)
    1---> We loop over each rules and break it down into left subjects and right subjects
    2---> We extract just the names of the subject using some regex functions and then analyse if the subjects are in proper chronological order,i.e.,
          whether the subjects in the left of the list come before subjects in the right part of the rules
    3---> If True then we add that rule as a VALUE to the dictionary relations under the KEY which is made up of a sorted tuple of the subjects present in the rule'''

for items in AprioriObject.finalRules:
    if(items != 1):
        for rules in AprioriObject.finalRules[items]:
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

            if all(Chronological_order[subject_in_left[1:-1]] < Chronological_order[subject_in_right[1:-1]] for subject_in_left in left_subjects for subject_in_right in right_subjects ):
                if(float(percentage[:-1])>75):
                    if(subjects_in_this_rule not in relations):
                        relations[subjects_in_this_rule] = [main_stuff]
                    else:
                        relations[subjects_in_this_rule].append(main_stuff)


'''We loop over relations and print the rules with proper heading'''
for subjects in relations:
    if(len(relations[subjects])>1):
        print('Relationship between: ',subjects)
        for items in relations[subjects]:
            print(items)
        print()

import pandas as pd
import os
import sys
from  FP_Growth import FP_Tree

dataFrame = pd.read_csv(open(os.path.join(sys.path[0],'MainData.csv')))

dataFrame.set_index('RollNo.',inplace  = True)

subjectList = ['CS201', 'CH201', 'M201', 'ME201', 'ES201','HU301', 'PH301', 'CH301', 'CS301', 'CS302', 'CS303', 'M(CS)401', 'M401', 'CS401', 'CS402', 'CS403', 'HU481', 'HU501', 'CS501', 'CS502', 'CS503', 'CS504D', 'HU601', 'CS601', 'CS602', 'CS603', 'CS604A/ CS604B', 'CS605A', 'CS681']
coresubs=[]
noncoresubs=[]

for i in subjectList:
    if "CS" in i:
        coresubs.append(i)
    elif "HU" in i:
        noncoresubs.append(i)

GOOD_MAIN_LIST = {}
BAD_MAIN_LIST={}


for rollNo in dataFrame.index:
    good=[]
    bad=[]
    for subject in noncoresubs:
        if dataFrame.loc[rollNo][subject]<7:
            bad.append(subject)
        else:
            good.append(subject)
    if good!=[]:
        GOOD_MAIN_LIST[rollNo]=good
    if bad!=[]:
        BAD_MAIN_LIST[rollNo]=bad

print("Rules for doing bad in HU:\n")
obj=FP_Tree(min=35,transactions=BAD_MAIN_LIST)
obj.displayRules(conf=0.9)
print("\n\nRules for doing good in HU:\n")
obj1=FP_Tree(min=35,transactions=GOOD_MAIN_LIST)
obj1.displayRules(conf=0.9)

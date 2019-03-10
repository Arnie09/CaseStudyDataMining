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
    else:
        noncoresubs.append(i)


MAIN_LIST = {}

for rollNo in dataFrame.index:
    SUBJECTS_WITH_MARKS={}
    for subject in coresubs:
        SUBJECTS_WITH_MARKS[subject]=dataFrame.loc[rollNo][subject]
    Chosen_10=[x[0] for x in sorted(SUBJECTS_WITH_MARKS.items(), key=lambda P:P[1],reverse =False)][:10]
    MAIN_LIST[rollNo]=Chosen_10

obj=FP_Tree(min=25,transactions=MAIN_LIST)
obj.displayRules(conf=0.9)

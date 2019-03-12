import pandas as pd
import os
import sys
from  FP_Growth import FP_Tree
dataFrame = pd.read_csv((os.path.join(sys.path[0],'MainData.csv')))
dataFrame.set_index('RollNo.',inplace  = True)
MAIN_LIST={}
SUBJECTS = list(dataFrame.columns)
for students in dataFrame.index:
    scores = []
    for subject in SUBJECTS:
        if("CS" in subject and "9" not in subject and "8" not in subject):
            marks = dataFrame.loc[students][subject]
            String = ""
            if(marks>=8):
                String = "Good marks in "
            elif(marks>=6 and marks<8):
                String = "Average marks in "
            else:
                String = "Poor marks in "
            scores.append((String+subject))
    MAIN_LIST[students] = scores

FptreeObject = FP_Tree(min = 30,transactions = MAIN_LIST)
FptreeObject.displayRules(conf=0.9)

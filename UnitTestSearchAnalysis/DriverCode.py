import pandas as pd
import os
import sys
from  FP_Growth import FP_Tree

dataFrame = pd.read_excel((os.path.join(sys.path[0],'MainData.xlsx')))

dataFrame.set_index('RollNo.',inplace  = True)

MAIN_LIST={}

for rollNo in dataFrame.index:
    eachTrans=[]
    for attribute in dataFrame.columns:
        eachTrans.append(dataFrame.loc[rollNo][attribute])
    MAIN_LIST[rollNo]=eachTrans


obj=FP_Tree(min=5,transactions=MAIN_LIST)
obj.displayRules(conf=0.8)

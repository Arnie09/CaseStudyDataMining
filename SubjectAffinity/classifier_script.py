import pandas as pd
import xlrd
import os
import sys

outputpath = os.path.join(sys.path[0])
path1 = os.path.join(sys.path[0],'MainData.csv')
dataset1 = pd.read_csv(path1)

dataset1.set_index("RollNo.",inplace = True)
dataCore = {}
dataCoreTheory = {}
dataOther = {}
dataOtherTheory = {}

subjectsCoreTheory = []
subjectsOtherTheory = []
subjectsCore = []
subjectsOther = []

for i in dataset1.columns.values:
    if('CS' in i):
        subjectsCore.append(i)
    elif('CS' not in i and 'Roll' not in i):
        subjectsOther.append(i)
    if('CS' in i and '9' not in i and '8' not in i):
        subjectsCoreTheory.append(i)
    elif('CS' not in i and '9' not in i and 'Roll' not in i and '8' not in i):
        subjectsOtherTheory.append(i)


Roll = list(dataset1.index)

for students in Roll:
    marksC = []
    marksCT = []
    marksO = []
    marksOT = []
    for subjects in dataset1.columns.values:
          if(subjects in subjectsCore):
              marksC.append(dataset1.loc[students][subjects])
          if(subjects in subjectsCoreTheory):
              marksCT.append(dataset1.loc[students][subjects])
          if(subjects in subjectsOther):
              marksO.append(dataset1.loc[students][subjects])
          if(subjects in subjectsOtherTheory):
              marksOT.append(dataset1.loc[students][subjects])

    dataCore[students] = marksC
    dataCoreTheory[students] = marksCT
    dataOther[students] = marksO
    dataOtherTheory[students] = marksOT

datasetCore = pd.DataFrame.from_dict(dataCore,orient = "index",columns = subjectsCore)
datasetCore.index.name = "RollNo."
datasetCore.to_csv(os.path.join(sys.path[0],"CoreSubjectsData.csv"))

datasetCoreTheory = pd.DataFrame.from_dict(dataCoreTheory,orient = "index",columns = subjectsCoreTheory)
datasetCoreTheory.index.name = "RollNo."
datasetCoreTheory.to_csv(os.path.join(sys.path[0],"CoreSubjectsDataTheory.csv"))

datasetOther = pd.DataFrame.from_dict(dataOther,orient = "index",columns = subjectsOther)
datasetOther.index.name = "RollNo."
datasetOther.to_csv(os.path.join(sys.path[0],"OtherSubjectsData.csv"))

datasetOtherTheory = pd.DataFrame.from_dict(dataOtherTheory,orient = "index",columns = subjectsOtherTheory)
datasetOtherTheory.index.name = "RollNo."
datasetOtherTheory.to_csv(os.path.join(sys.path[0],"OtherSubjectsTheory.csv"))

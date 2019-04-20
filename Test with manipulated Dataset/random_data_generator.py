import pandas as pd
import xlrd
import openpyxl
import random
import os
import sys

subjects_to_randomise = ['Discrete Mathematics','Data Base Management System','Computer Networks','Operating System','Information Theory & Coding / Computer Graphics','Operation Research']

dataset = pd.read_excel((os.path.join(sys.path[0],'ManipulatedDataset.xlsx')))

dataset.set_index('RollNo.',inplace = True)

seed_val = 3
for students in dataset.index:
    random.seed(seed_val)
    seed_val+=3
    for subjects in subjects_to_randomise:
        dataset.loc[students][subjects] = random.randint(2,10)

dataset.to_excel(os.path.join(sys.path[0],'ManipulatedDataset2.xlsx'))

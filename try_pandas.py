import pandas as pd
import os

currentDir = os.getcwd()
fileName = "output.xlsx"


df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                  index=['one', 'two', 'three'], columns=['a', 'b', 'c'])
df.to_excel(currentDir + '/' + fileName, sheet_name='new_sheet_name')


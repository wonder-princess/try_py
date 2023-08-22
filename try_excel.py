import pandas as pd
import os
import datetime

currentDir = os.getcwd()
fileName = "output.xlsx"


df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                  index=['one', 'two', 'three'], columns=['a', 'b', 'c'])

humans = pd.DataFrame({
    'name':['sato', 'suzuki', 'tori'],
    'age':[21, 30, 18],
    'blood':['A', 'B', 'O']
})

address = pd.Series(['東京', '埼玉', '千葉'], name = 'address')
humans[address] = address

humans.to_excel(currentDir + '/' + fileName, sheet_name='new_sheet_name')

fileName = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S") + ".csv"

print(type(fileName))



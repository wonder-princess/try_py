import pandas as pd
import os

currentDir = os.getcwd()
fileName = "output.xlsx"

df = pd.read_csv('23-08-23 01-04-55.csv')
# df['userid'] = df['userid'].astype(str)
print(f"超複数:{df.duplicated().sum()}")
df.drop_duplicates(subset='URL', inplace=True)

print(df)

df.to_csv(f"{os.getcwd()}/output.csv", index=False)

# df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]], index=['one', 'two', 'three'], columns=['a', 'b', 'c'])
# df.to_excel(currentDir + '/' + fileName, sheet_name='new_sheet_name')


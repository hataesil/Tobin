import pandas as pd
import openpyxl
import datetime
#df1 = pd.DataFrame([['a','b','c'],['d','e','f']],columns=['col1','col2','col3'])
df = pd.DataFrame([['a','b','c'],['d','e','f']])

#df1.to_excel(excel_writer="output01.xlsx")
print(df)
df_list = df.values.tolist()
print(df_list)
df2 = pd.DataFrame(df_list,columns=['가','나','다'])
print(df2)

print(datetime.datetime.now())




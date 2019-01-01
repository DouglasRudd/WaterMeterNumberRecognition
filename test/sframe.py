import sframe
import pandas as pd

data_df = pd.read_csv('G:/trainingData/data8.csv', sep=',')

print(data_df.columns)

print data_df['id'][0]

df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))

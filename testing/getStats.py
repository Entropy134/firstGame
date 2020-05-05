import pandas as pd

FILE = '../assets/pokemon.csv'
TESTMON = 'Squirtle'

df = pd.read_csv(FILE)
df = df.loc[(df['Name'].str.contains('Mega')==False)&(df['Name'].str.contains('Primal')==False)]
df.set_index("Name", inplace = True)
print('Show the first few values of the dataset')
print(df.head(9))

val = df.loc[TESTMON]
# print('The base special attack for '+TESTMON+' is :' + str(val))
print(val['Attack'])


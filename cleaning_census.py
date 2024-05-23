import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

list_csv = glob.glob('states*.csv')
print(list_csv)

df_list = []
for filename in list_csv:
  data = pd.read_csv(filename)
  df_list.append(data)

census = pd.concat(df_list)

# inspect df
# print(census.head(10))
# print(census.shape)

# reset df index
census.reset_index(drop=True, inplace=True)

# rename df columns
census.rename(columns={
  'State': 'state',
  'TotalPop': 'total_pop',
  'Hispanic': 'hispanic',
  'White': 'white',
  'Black': 'black',
  'Native': 'native',
  'Asian': 'asian',
  'Pacific': 'pacific',
  'Income': 'income',
  'GenderPop': 'gender_pop'
  }, inplace=True)

# print(census.columns)

# droping column 'Unnamed: 0' and 'prev_index'
census = census.drop(census.columns[[0,]], axis=1)

# print(census.head(10))
# print(census.dtypes)
# print(census.info())

# get rig of misslead formats
for col in census.columns:
  if census[col].dtype == 'object':
    census[col] = census[col].str.replace('[\s\%\$]', '')
  else:
    continue

# print(census.head(5))
# print(census.dtypes)

# convert hispanic to pacific columns dtypes object to numeric
for col in census.columns[2:9]:
  census[col] = pd.to_numeric(census[col])

# print(census.dtypes)

# split gender_pop column and format dtype
gender_pop_split = census.gender_pop.str.split('_')
census['pop_male'] = gender_pop_split.str.get(0).str.replace('\D', '')
census['pop_female'] = gender_pop_split.str.get(1).str.replace('\D', '')
census.pop_male = pd.to_numeric(census.pop_male)
census.pop_female = pd.to_numeric(census.pop_female)
# drop gender_pop column
census = census.drop(columns='gender_pop', axis=1)

# print(census.head())

# finding missing data
print(census.info())
# displaying  pop_females missing data
# print(census[['state','total_pop','pop_male','pop_female']][census.pop_female.isna()])
# displaying pacific missing data
# print(census[['state','total_pop','pacific']][census.pacific.isna()])

# # display plots
# plt.scatter(data=census, x='pop_female', y='income')
# plt.show(); plt.clf()

# fill Nan values in pop_female by difference of total_pop - pop_male in the relevant state
census.pop_female = census['pop_female'].fillna(census.total_pop - census.pop_male)
print(census.pop_female.isna().sum())    # also can use isna().any() to return bool

# fill missing nan values in pacific column
census['pacific'] = census['pacific'].fillna(0) 

# displaying duplicated observations
# print(census[census.duplicated()])
print('Num of duplicates:',census.duplicated().sum())
# drop duplicates
census = census.drop_duplicates()
print('Num of duplicates:',census.duplicated().sum())
census.reset_index(drop=True, inplace=True)
print(census.head(10))

# display scatter plot
plt.scatter(data=census, x='pop_female', y='income')
plt.show(); plt.clf()

# print(census.info())

# display histogram
for col in census.columns:
  if census[col].dtype != 'object':
  # print(col)
    plt.hist(census[col])
    plt.title(str(col).title())
    plt.ylabel('count')
    plt.show(); plt.clf()

# create new_df etnics by droping unuseful columns
etnics = census.drop(columns=['state', 'total_pop', 'income', 'pop_male', 'pop_female'])
print(etnics.columns)
# create dictionary
etnics_dict = {column: etnics[column].mean() for column in etnics.columns}
print(etnics_dict)
# plot etnic groups distribution pie chart
plt.pie(pd.Series(etnics_dict), labels=list(etnics.columns), labeldistance=0.6, autopct='%1.1f%%', pctdistance=1.15)
plt.axis('equal')
plt.show(); plt.clf()
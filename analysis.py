import pandas as pd

pd.set_option('display.max_columns',14)

# reads the csv files
df_gen = pd.read_csv("test/general.csv")
df_pre = pd.read_csv("test/prenatal.csv")
df_spo = pd.read_csv("test/sports.csv")

# rename columns in dataframe other option: prenatal.columns, sports.columns = general.columns, general.columns
df_pre = df_pre.rename(columns={'HOSPITAL':'hospital', 'Sex':'gender'})
df_spo = df_spo.rename(columns={'Hospital':'hospital','Male/female':'gender'})

# merges dataframes
df_hos = pd.concat([df_gen, df_pre, df_spo], ignore_index=True)

# delete unnamed column and na
df_hos.drop(columns=['Unnamed: 0'], inplace=True)
df_hos.dropna(axis=0, how='all', inplace=True)

# replace values in gender column
df_hos['gender'] = df_hos['gender'].replace(['female', 'woman'],'f')
df_hos['gender'] = df_hos['gender'].replace(['male', 'man'],'m')
df_hos['gender'] = df_hos['gender'].fillna('f')

# fill 0 instead of na in columns in list
column_list = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
for column_name in column_list:
    df_hos[column_name] = df_hos[column_name].fillna('0')

# Questions
# Which hospital has the highest number of patients?
# What share of the patients in the general hospital suffers from stomach-related issues? Round the result to the third
# decimal place.
# What share of the patients in the sports hospital suffers from dislocation-related issues? Round the result to the
# third decimal place.
# What is the difference in the median ages of the patients in the general and sports hospitals?
# After data processing at the previous stages, the blood_test column has three values: t= a blood test was taken,
# f= a blood test wasn't taken, and 0= there is no information. In which hospital the blood test was taken the most
# often (there is the biggest number of t in the blood_test column among all the hospitals)? How many blood tests were
# taken?

print(f"The answer to the 1st question is {df_hos['hospital'].value_counts().idxmax()}")
df_stomach = df_hos.loc[(df_hos["hospital"]=="general")&(df_hos["diagnosis"]=="stomach")]
df_general = df_hos.loc[df_hos["hospital"]=="general"]
print(f"The answer to the 1st question is {round(df_stomach.shape[0]/df_general.shape[0], 3)}")
df_disloc = df_hos.loc[(df_hos["hospital"]=="sports")&(df_hos["diagnosis"]=="dislocation")]
df_sport = df_hos.loc[df_hos["hospital"]=="sports"]
print(f"The answer to the 3rd question is {round(df_disloc.shape[0]/df_sport.shape[0], 3)}")
med_gen = df_hos.loc[df_hos["hospital"]=="general", "age"].mean()
med_spo = df_hos.loc[df_hos["hospital"]=="sports", "age"].mean()
print(f"The answer to the 4th question is {med_gen - med_spo}")
bt_g = df_hos.loc[(df_hos["hospital"]=="general")&(df_hos["blood_test"]=="t")]
bt_s = df_hos.loc[(df_hos["hospital"]=="sports")&(df_hos["blood_test"]=="t")]
bt_p = df_hos.loc[(df_hos["hospital"]=="prenatal")&(df_hos["blood_test"]=="t")]
bt_max = [bt_g.shape[0], bt_p.shape[0], bt_s.shape[0]]
print(f"The answer to the 5th question is prenatal, {max(bt_max)} blood tests")
# print(df_hos.sample(n=20, random_state=30))

# import packages
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import pickle
import pandas as pd

# import data
path_to_data = "/Users/gabrielgilling/Downloads/"
df = pd.read_csv(path_to_data+'nuMoM2b_Dataset_NICHD Data Challenge.csv')

demographic_cols = [
    'GAwks_screen',
    'Age_at_V1',
    'eRace',
    'BMI',
    'Education',
    'GravCat',
    'SmokeCat1',
    'SmokeCat2',
    'Ins_Govt',         
    'Ins_Mil',           
    'Ins_Comm',         
    'Ins_Pers',        
    'Ins_Othr',
    'V1AF14',
    'V1AG01',
    'V1AG11',]

# create subsetted df
df_demographics = df[demographic_cols].copy()

df_demographics['Age_at_V1'] = df_demographics['Age_at_V1'].fillna(df_demographics['Age_at_V1'].mean())
df_demographics['BMI'] = df_demographics['BMI'].fillna(df_demographics['BMI'].mean())

for cat_col in ['Education', 'GravCat', 'SmokeCat1', 'SmokeCat2', 'Ins_Govt', 'Ins_Mil', 
                'Ins_Comm', 'Ins_Pers', 'Ins_Othr', 'V1AG11', 'V1AG01', 'V1AF14']:
    mode = df_demographics[cat_col].mode().values[0]
    df_demographics[cat_col] = df_demographics[cat_col].fillna(mode)

# impute and standardize numeric features
df_demographics[['GAwks_screen','Age_at_V1', 'BMI']] = df_demographics[['GAwks_screen','Age_at_V1', 'BMI']].apply(lambda x: (x - np.mean(x)) / np.std(x))

df_demographics[[code for code in df_demographics.columns if code not in ['GAwks_screen','Age_at_V1', 'BMI']]] = df_demographics[[code for code in df_demographics.columns if code not in ['GAwks_screen','Age_at_V1', 'BMI']]].astype(str)

df_demographics = pd.concat([df_demographics, df.PublicID], axis = 1)

df_demographics.to_pickle('df_demographics.pkl')
import pandas as pd
import numpy as np
import json
import pickle
import warnings
warnings.filterwarnings("ignore")

path_to_data = "/Users/gabrielgilling/Downloads/"
df = pd.read_csv(path_to_data+'nuMoM2b_Dataset_NICHD Data Challenge.csv')

#Drop Empty Rows and Empty Columns
df = df.dropna(how='all')
df = df.dropna(how='all', axis = 'columns')

pregnancy_outcome_v3 = 'pOUTCOME'

df[pregnancy_outcome_v3] = df[pregnancy_outcome_v3].astype(str)

target_codes = ['PEgHTN', 
                'ChronHTN', 
                'pOUTCOME',
                'CMAD01a',
                'CMAD01b',
                'CMAD01c',
                'CMAD01d',
                'CMAD01e',
                'CMAD01f',
                'CMAD01g',
                'CMAD01h',
                'CMAE04a1c',
                'CMAE04a2c',
                'CMAE04a3c',
                'CMAE04a4c',
                'CMAE04a5c',
               ]

df_targets = df[target_codes].copy()

replace_map = {'S': np.nan, 'D': np.nan, 'E': np.nan, 'M': np.nan, 'N': np.nan, 'R':np.nan}

df_targets = df_targets.replace(replace_map)

df_targets['PEgHTN'] = [0 if val == 7 and not np.isnan(val) else 1 if val != 7 and not np.isnan(val) else val for val in df_targets['PEgHTN']]
df_targets['ChronHTN'] = [0 if val == 2 and not np.isnan(val) else 1 if val != 2 and not np.isnan(val) else val for val in df_targets['ChronHTN']]

# recode pregnancy outcomes
df_targets['pOUTCOME'] = pd.to_numeric(df_targets['pOUTCOME'], errors = 'coerce')

df_targets['Stillbirth'] = [1 if val == 2.0 and not np.isnan(val) else 0 if val != 2.0 and not np.isnan(val) else val for val in df_targets['pOUTCOME'] ]

df_targets['Miscarriage'] = [1 if val == 3.0 and not np.isnan(val) else 0 if val != 3.0 and not np.isnan(val) else val for val in df_targets['pOUTCOME'] ]

df_targets['Termination'] = [1 if (val == 4.0 or val == 5.0 and not np.isnan(val)) else 0 if (val != 4.0 or val != 5.0) and not np.isnan(val) else val for val in df_targets['pOUTCOME']] 

df_targets = df_targets.drop(['pOUTCOME'], axis = 1)
df_targets = df_targets.apply(lambda x :pd.to_numeric(x, errors = 'coerce'))

df_targets = pd.concat([df_targets, df.PublicID], axis = 1)

df_targets.to_pickle('targets_df.pkl')
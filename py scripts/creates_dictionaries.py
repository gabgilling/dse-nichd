## this file creates two dictionaries containing the metadata associated with the challenge variables

# import packages
import numpy as np
import pandas as pd
import json

# set your paths here
path_to_data_dictionary = "nuMoM2b_Codebook_NICHD Data Challenge (1).xlsx"

# import Excel sheets to convert to dictionary format
var_df = pd.read_excel(path_to_data_dictionary, sheet_name =  "nuMoM2b_Variables", header = 1)
codes_df = pd.read_excel(path_to_data_dictionary, sheet_name =  "Code_Lists", header = 0)

# create dictionary containing coded values
code_dict = {}
for code in codes_df['Code List Name'].unique():
    code_dict[code] = {}
    temp = codes_df[codes_df['Code List Name'] == code]
    for i in range(len(temp)):
        code_dict[code][temp['Value'].iloc[i]] = temp['Value Label'].iloc[i]

# create dictionary containing variable metadata
var_dict = {}
for i in range(len(var_df)):
    var_dict[var_df['Variable Name'].iloc[i]] = {'Type': var_df['Variable Type'].iloc[i], 
                                                 'Code': var_df['Variable Code List\n(if Coded)'].iloc[i],
                                                 'Label': var_df['Variable Label'].iloc[i],
                                                 'Dataset': var_df['Original Dataset Name'].iloc[i]}

# save dictionaries
with open('var_dict.txt', 'w') as outfile:
    json.dump(var_dict, outfile)

with open('code_dict.txt', 'w') as outfile:
    json.dump(code_dict, outfile)
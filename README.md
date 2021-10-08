# NICHD Submission

Team: 
- Ainesh Pandey - IBM
- Gabriel Gilling - IBM
- Demian Gass - IBM
- (Andre Violante) - IBM

# Abstract

For this challenge, we decided to assess the impact of changes in features that were measured across the visits on different pregnancy outcomes. To that extent, we divided the challenge's dataset into several components: a base dataset with demographic information, a delta dataset capturing changes in features between visits and finally a target dataset with target variables.

For each target variable we've identified, we run 3 classification models: a Lasso regression, a random forest and a catboost. For each model, we tabulate the most important features and for the Lasso model, we additionally tabulate the feature p-values in order to ascertain the uncertainty around their estimated effects.


# Methodology

First, we created our __base__ dataset, which sought to capture pregnant women characteristics _before_ their pregnancies. This consisted of the following variables:
- Demographic variables:
  - GAwks_screen
  - Age_at_V1
  - eRace
  - BMI
  - Education
  - GravCat
  - SmokeCat1
  - SmokeCat2
  - Ins_Govt         
  - Ins_Mil           
  - Ins_Comm         
  - Ins_Pers        
  - Ins_Othr
  
- Other important variables we identified:
  - V1AF14
  - V1AG01
  - V1AG11

Second, we created a __delta__ dataset

# Results

# NICHD Submission

Team: 
- Ainesh Pandey - IBM
- Gabriel Gilling - IBM
- Demian Gass - IBM
- (Andre Violante) - IBM

# Running this project

Run these files:


# Abstract

For this challenge, we decided to assess the impact of changes in features that were measured across the visits on different pregnancy outcomes. To that extent, we divided the challenge's dataset into several components: a __base__ dataset with demographic information, a __delta__ dataset capturing changes in features between visits and finally a __target__ dataset with outcome variables related to maternal morbidity.

For each target variable we've identified, we run 2 classification models: a _Light Gradient Boosting Machine_ (LGBM) and a _Random Forest_ (RF). For each target variable, we first assess which of the two models perfomed the best in terms of f-1 score ( the harmonic mean between precision and recall metrics, going beyond the accuracy metric which we found to be unhelpful given the imbalanced distributions of the target variables). After dropping target variables with low support (AINESH FLAG), we worked with XXX targets. We then identify the 10 most important features in predicting each target variable and then break down the top feature's univariate distribution by racial categories.

We find that [Ainesh to fill]


# Methodology

First, we created our __base__ dataset, which sought to capture pregnant women characteristics _before_ their pregnancies. When running [predictive] models, it is important to adjust for important covariates that could 

This consisted of the following variables:
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
  - V1AF14: Total family income for the past 12 months
  - V1AG01: Have you ever drunk alcohol?
  - V1AG11: Have you ever used illegal drugs or drugs not prescribed for you?



Second, we created a __delta__ dataset

# Results

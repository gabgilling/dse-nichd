# NICHD Submission

Team: 
- Ainesh Pandey - ainesh93@gmail.com - IBM
- Gabriel Gilling  - gabrielgilling@gmail.com - IBM
- Demian Gass - demian.gass@gmail.com - IBM

# Running this project

Run these files:


# Abstract

For this challenge, we decided to assess the impact of changes in features that were measured across the visits on different pregnancy outcomes. To that extent, we divided the challenge's dataset into several components: a __base__ dataset with demographic information, a __delta__ dataset capturing changes in features between visits and finally a __target__ dataset with outcome variables related to maternal morbidity.

For each target variable we've identified, we run 2 classification models: a _Light Gradient Boosting Machine_ (LGBM) and a _Random Forest_ (RF). For each target variable, we first assess which of the two models perfomed the best in terms of f-1 score ( the harmonic mean between precision and recall metrics, going beyond the accuracy metric which we found to be unhelpful given the imbalanced distributions of the target variables). After dropping target variables with low support (AINESH FLAG), we worked with XXX targets. We then identify the 10 most important features in predicting each target variable and then break down the top feature's univariate distribution by racial categories.

We find that [Ainesh to fill]


# Methodology

## 1. Base Dataset
First, we created our __base__ dataset in the [create_base_df.py](https://github.com/gabgilling/dse-nichd/blob/main/create_base_df.py) script which sought to capture pregnant women characteristics _before_ their pregnancies. When running [predictive] models, it is important to adjust/control for important covariates that are likely to account for the variation observed in the target variable. The base dataset was created by using the variables included in the _demographics_ ancillary file. We dropped redundant variables (i.e. we dropped `BMI_cat` since we had `BMI` already), as well as variables with too many null values. We also manually parsed through the _V1A_ file in order to find additional covariates that were deemed important when predicting maternal morbidity, skipping over any variable with too many missing values.

As such, our base dataset consists of the following `16` variables:
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

We then imputated missing values using the following process:
  1. For numerical variables, we imputed the mean of the variable's distributions
  2. For categorical variables, we imputed the mode (the category occuring the most often)
  3. For numerical variables, we performed Z-score standardisation, expressing the variables as Z-scores (the "distance" from the mean of the distribution in standard deviation terms).


## Delta dataset
Second, we created a __delta__ dataset which measured the changes with respect to certain features that were measured on multiple visits. Specifically, we tracked changes in features from the following tables:

  - Clinical Measurements: V1B, V2B, V3B
  - Edinburgh Postnatal Depression Scale: V1C and V3C
  - Sleep Monitoring: V1K and V3K
  - Revised Sleep Questionnaire: V1L and V3L
  - Uterine Artery Doppler: U1C, U2C, U3C
  - Fetal Biometry: U2A and U3A
  - Cervical Length: U2B and U3B

Of these datasets, we only tracked those variables which were measured at multiple visits. We were interested in understanding how changes in these features might be predictive of adverse pregnancy outcomes. For numeric features, we simply calculated the difference in measurements between two visits. For instance, Resting blood pressure was measured at Visit 2(V2BA02a1) and Visit 3(V3BA02a1). These two measurements were used to create a new feature, V2BA02a1_delta_V3BA02a1, which is the difference in blood pressure measurements between Visit 3 and Visit 2, or $V3BA02a1 - V2BA02a1$. For encoded categorical features, we took a similar approach in tracking changes in these features across visits. Here

## Target dataset

# Results

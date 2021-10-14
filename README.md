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

## Preparing the Data for Modeling

### 1. Base Dataset
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


### 2. Delta Feature Creation

Second, we created a __delta__ dataset which measured the changes with respect to certain features that were measured on multiple visits. Specifically, we tracked changes in features from the following tables:

  - Clinical Measurements: V1B, V2B, V3B
  - Edinburgh Postnatal Depression Scale: V1C and V3C
  - Sleep Monitoring: V1K and V3K
  - Revised Sleep Questionnaire: V1L and V3L
  - Uterine Artery Doppler: U1C, U2C, U3C
  - Fetal Biometry: U2A and U3A
  - Cervical Length: U2B and U3B

Of these datasets, we only tracked those variables which were measured at multiple visits. We were interested in understanding how changes in these features might be predictive of adverse pregnancy outcomes. This technique could present an exciting new area of research in the medical field: how does the rate of change in certain measures of health and body metrics relate to adverse pregnancy outcomes. Our hope in taking this approach was to find certain *delta features* which showed signs of being predictive of certain APOs after controlling for such things like socio-economic status, race, etc.. If we were to find evidence of this predictive power, it may tell us which metrics doctors and health professionals should be tracking during the antepartum and intrapartum phases of pregnancy when looking to screen for APOs. The ultimate goal with this research would be to build an alert system which flags certain patients as being at risk when we see worrying changes in their health measurements. 

Before calculating these differences, or delta features, we first standardized all of the numeric features. Null values in both the encoded features as well as the numeric features were left in the data, for now. We standardized the numeric features before calculating differences so that our delta features represented the change in a metric with respect to the population. Once this preprocessing step was complete, we began the process of creating the delta features.

For numeric features, we simply calculated the difference in measurements between two visits. For instance, Resting blood pressure was measured at Visit 2(V2BA02a1) and Visit 3(V3BA02a1). These two measurements were used to create a new feature, V2BA02a1_delta_V3BA02a1, which is the difference in blood pressure measurements between Visit 3 and Visit 2, or $V3BA02a1 - V2BA02a1$. 

For encoded categorical features, we took a similar approach in tracking changes in these features across visits by tracking the different combinations of changes that can occur within a feature. For instance, U1CD01 and U2CD01 track whether or not the placenta is implanted on the ipsilateral side for the right uterine artery during the first visit and second visit, respecitively. As an example, let us say that for a given patient the U1CD01 value is 1.0 (Yes) and the U2CD01 value is 2.0 (No), we create a delta feature, U1CD01_delta_U2CD01, and give this patient the value 1.0-2.0. The levels of this new delta feature then signify the different changes that can happen wihtin the measured feature. We also treat missing values for these encoded features as a level, so that we know if a patient's measurement changes from missing to present.

Finally, once the delta features were created, we imputed the missing values within the numeric features using mean imputation. Having done this after calculting the delta features, this was akin to assuming that where the values were missing, patients had the average amount of change as found in the population. This seemed more approriate to us than imputing those missing values before standardizing and taking the difference between visits.

### 3. Target creation
Third, we created the target dataset with the [create_targets_df.py](https://github.com/gabgilling/dse-nichd/blob/main/create_targets_df.py) script. We started by identifying variables available in the _pregnancy_outcomes_ file, zeroing in on variables most closely related to maternal morbidity. We then manually iterated over the _CMA_ file in order to choose additional variables linked to complications arising out of pregnancies.

The `pOUTCOME` variable included in the _pregnancy_outcomes_ file was split into 3 new variables according to the categories included in it: `Stillbirth`, `Termination` and `Miscarriage`.

As such, we have a total of `18` potential targets coded as binary [0,1] variables:
- From _pregnancy_outcomes_:
  - PEgHTN: Preeclampsia/Gestational hypertension
  - ChronHTN: Chronic hypertension based on CMDA01 & CMAE01
  - pOUTCOME split into:
    - Stillbirth
    - Termination
    - Miscarriage
- From _CMA_ postpartum complication:
  - CMAD01a: 
  - CMAD01b:
  - CMAD01c:
  - CMAD01d:
  - CMAD01e:
  - CMAD01f:
  - CMAD01g:
  - CMAD01h:
- From _CMA_ postpartum mental health conditions:
  - CMAE04a1c:
  - CMAE04a2c:
  - CMAE04a3c:
  - CMAE04a4c:
  - CMAE04a5c:

## Modeling outcome variables
justifying LGBM + RF 
non-linear and non-parametric ML methods that a straightforward OLS model wouldn't get 
RFs are ensemble methods, ensemble methods powerful

AINESH

# Analysis of Results
In understanding the results of our models, we were most interested in understanding which models appeared to have the most predictive power of certain target features, as well as which features were most important in predicting certain adverse outcomes. Models that perform well in predicting our target features show evidence that a machine learning approach could be useful when trying to predict adverse pregnancy outcomes in future patients. Finding features that appear to be important when predicting those outcomes provides us with some explainability and potential areas for future research (i.e. why are these features so predictive of certain APOs?). 

First, we only focus on models where the support for the minority class is greater than 50. This means that we drop those models where there were fewer than 50 observations of the "positive" instances, or cases in which the adverse outcome did occur (e.g. there were fewer than 50 cases of miscarriage, so we decided to drop those models from our analysis). We decided to take this approach because model results can be misleading and uncertain when the support is so low. We are left with 4 target features: Chronic Hypertension (ChronHTN), Postpartum Depression (CMAE04a1c), Postpartum Anxiety (CMAE04a2c), and Preeclampsia (PEgHTN). For these 4 targets, we choose one of the three modeling approaches (Logistic Regression, Random Forest, LGBM) that achieved the highest F1 score to analyze the results for. We decided to focus on F1 score because of the large class imbalance in our data (most patients did not have the adverse pregancy outcome occur). In this context, false negatives are extremely costly to us, and so we want to place an emphasis on recall. However, we also don't want to dilute our predictions with false positives, and thus F1 score allows us to optimize on both recall and precision.

For the models that remain, we extract the top 10 most impactful features, including both covariates and the delta features. For each of the 4 target features, we analyze the model performance and the 10 most important features driving those predictions. This provides us with insight into the feasability of modeling certain APOs as well as the potential drivers of these outcomes. Please see the *Analysis of Results* notebook for more detail.

We believe that our results present promising signs for future research. For four different APOs, we were able to build models with strong predictive power. With further iterations in parameter tuning, feature engineering, and model refinement, we believe that these models have the potential to unlock new predictive capabilities in the medical industry. There would be an immense benefit in being able to accurately predict an adverse pregnancy outcome for a patient before it actually occurs, allowing time to take preventative measures.

Additionally, we are able to understand the features that were the most important drivers in our models' predictions. While the feature importance results aren't necessarily conclusive in terms of causality, they do point to possible drivers of these APOs. This provides us with starting areas for future research. If we find that there are certain controllable factors in a mother's health that may affect the likelihood of an APO, then this could inform the care that mothers receive. We hope that these results lead to a more informed understanding of APOs and drive a more informed approach to caring for pregnant women, thereby reducing the cost of APOs throughout the country.
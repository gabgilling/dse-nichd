# NICHD Submission

Team: 
- Ainesh Pandey (Lead) - ainesh93@gmail.com - IBM
- Gabriel Gilling  - gabrielgilling@gmail.com - IBM
- Demian Gass - demian.gass@gmail.com - IBM

# Running this project

In order to run our challenge submission, you first need to run the `requirements.txt` file. After cloning the repo to your local drive, simply run `pip install -r requirements.txt` in your shell/terminal. This will adjust the package dependencies to match the ones used in our project. One of the models we used came from the LightGBM library, you may also want to navigate to the package's [documentation](https://lightgbm.readthedocs.io/en/latest/Installation-Guide.html) for additional steps should the requirements file return an error.

We have structured our analysis into 3 Jupyter Notebooks. Before running the notebooks, please set the paths to where the `nuMoM2b_Dataset_NICHD Data Challenge.csv` and `nuMoM2b_Codebook_NICHD Data Challenge.xlsx` files are located in the `my_path.py` file located [here](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/scripts/my_path.py).

First, [EDA and Data Preparation.ipynb](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/EDA%20and%20Data%20Preparation.ipynb) walks through the creation of the Delta variables used in our analysis, and it also runs scripts used to create the Covariate and Target variables datasets.

Second, [Modeling.ipynb](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/Modeling.ipynb) runs Logistic Regression, Random Forest, and LGBM models for selected target variables.

Third, [Analysis of Results.ipynb](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/Analysis%20of%20Results.ipynb) goes over our findings, and provides graphics and plots explaining them.

# Abstract

For this challenge, we decided to assess the impact of changes in features that were measured across maternal hospital visits on different adverse pregnancy outcomes. To that extent, we divided the challenge's dataset into several components:
- a __covariates__ dataset with demographic and socio-economic information,
- a __deltas__ dataset capturing changes in features across multiple visits, and
- a __targets__ dataset with outcome variables related to maternal morbidity.

For each target variable, we trained and tuned 3 classification models: a _Logistic Regression Model_, a _Light Gradient Boosting Machine (LGBM)_ and a _Random Forest_. We assessed which of the three models perfomed the best in terms of the F-1 score (the harmonic mean between precision and recall metrics, going beyond the accuracy metric which we found to be unhelpful given the imbalanced distributions of the target variables) of the positive class. After dropping target variables with low support, we were able to identify impactful features for the following morbidities:
- Chronic Hypertension
- Postpartum Depression
- Postpartum Anxiety
- Preeclampsia

We then identified the 10 most important features in predicting each target and broke down the top features' univariate distributions by racial categories. We find that there are several impactful delta features related to the mother's sleep behavior, the mother's general health, pregnancy progression, and fetal health that also demonstrate distinctly different distributional behavior for the majority race class (white women) when compared to minority race classes. These findings can guide the direction of future research into the drivers of the APOs analyzed in this solution.

# Methodology

## Approach

The goal of our approach is to analyze the changes (or _deltas_) in measured characteristics throughout pregnancy to identify which deltas are highly indicative of certain maternal morbidities. The `nuMoM2b` dataset tracks various elements of the condition of the pregnancy through maternal hospital visits. Therefore, we will use the deltas between features measured across multiple visits as inputs into our machine learning models.

## Preparing the Data for Modeling


### 1. Creating the Delta Features Dataset

First, we created the __deltas__ dataset which measured the changes with respect to certain features that were measured on multiple visits. Specifically, we tracked changes in features from the following tables:

  - Clinical Measurements: V1B, V2B, V3B
  - Edinburgh Postnatal Depression Scale: V1C and V3C
  - Sleep Monitoring: V1K and V3K
  - Revised Sleep Questionnaire: V1L and V3L
  - Uterine Artery Doppler: U1C, U2C, U3C
  - Fetal Biometry: U2A and U3A
  - Cervical Length: U2B and U3B

Of these datasets, we only tracked those variables which were measured across multiple visits. We were interested in understanding how changes in these features might be predictive of adverse pregnancy outcomes (APOs). This technique could present an exciting new area of research in the medical field: how the rate of change in standardized measures of health and body metrics throughout active pregnancies relates to APOs. The intent of this approach was to identify *delta features* which showed signs of being predictive of certain APOs after controlling for covariates such as demographics and socio-economic status. If we were to find evidence of this predictive power, it may tell us which metrics doctors and health professionals should be tracking during the antepartum and intrapartum phases of pregnancy when looking to screen for APOs. The ultimate goal with this research would be to build an alert system which flags certain patients as being at risk when we see worrying changes in real-time health measurements that have been identified as predictive for certain APOs. 

Before calculating these differences, or delta features, we first standardized all of the numeric features. Null values in both the encoded features as well as the numeric features were left in the data, for now. We standardized the numeric features before calculating differences so that our delta features represented the change in a metric with respect to the population. Once this preprocessing step was complete, we began the process of creating the delta features.

For numeric features, we simply calculated the difference in measurements between two visits. For instance, systolic resting blood pressure was measured at Visit 2(`V2BA02a1`) and Visit 3(`V3BA02a1`). These two measurements were used to create a new feature, `V2BA02a1_delta_V3BA02a1`, which is the difference in standardized blood pressure measurements between Visit 3 and Visit 2, or $`V3BA02a1` - `V2BA02a1`$. 

For encoded categorical features, we took a similar approach in tracking changes in these features across visits by tracking the different combinations of changes that can occur within a feature. For instance, `U1CD01` and `U2CD01` track whether or not the placenta is implanted on the ipsilateral side for the right uterine artery during the first visit and second visit, respectively. As an example, let us say that for a given patient, the `U1CD01` value is *1.0 (Yes)* and the `U2CD01` value is *2.0 (No)*. We create a delta feature, `U1CD01_delta_U2CD01`, and give this patient the value *1.0-2.0*. The levels of this new delta feature then signify the different changes that can happen within the measured feature. We also treat missing values for these encoded features as a level, in order to know if a patient's measurement changes from missing to present.

Finally, once the delta features were created, we imputed the missing values within the numeric features using mean imputation. Having done this after calculating the deltas between standardized features, this was akin to assuming that where the values were missing, patients had the average amount of change as found in the population. This is a more appropriate way of handling missing values, given our actual inputs are the deltas between features, not the features themselves.

Please see the [EDA and Data Preparation](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/EDA%20and%20Data%20Preparation.ipynb) notebook for a detailed run-through of our delta features prep.

### 2. Creating the Covariates Dataset (in the EDA and Data Preparation Notebook)

Second, we created our __covariates__ dataset in the [create_covariates_df.py](https://github.com/gabgilling/dse-nichd/blob/main/scripts/create_covariates_df.py) script which sought to capture pregnant women characteristics _before_ their pregnancies. When running predictive models, it is important to adjust/control for important covariates that are likely to account for the variation observed in the target variable. The covariates dataset was initially created by using the variables included in the _demographics_ ancillary file. We dropped redundant variables (i.e. we dropped `BMI_cat` since we had `BMI` already), as well as variables with too many null values. We also manually parsed through the _V1A_ file in order to find additional covariates that were deemed important when predicting maternal morbidity, skipping over any variable with too many missing values.

As such, our covariates dataset consists of the following `16` variables:
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
  2. For categorical variables, we imputed the mode
  3. For numerical variables, we performed Z-score standardisation, expressing the variables as Z-scores (the "distance" from the mean of the distribution in standard deviation terms).


### 3. Creating the Targets Dataset (in the EDA and Data Preparation Notebook)

Third, we created the target dataset with the [create_targets_df.py](https://github.com/gabgilling/dse-nichd/blob/main/scripts/create_targets_df.py) script. We started by identifying variables available in the _pregnancy_outcomes_ file, zeroing in on variables most closely related to maternal morbidity. We then manually iterated over the _CMA_ file in order to identify additional features linked to complications arising out of pregnancy.

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
  - CMAD01a: Postpartum hemorrhage requiring transfusion
  - CMAD01b: Retained placenta
  - CMAD01c: Endometritis
  - CMAD01d: Wound Infection
  - CMAD01e: Wound dehiscence requiring debridement, packing, and/or reapproximation
  - CMAD01f: Cardiomyopathy
  - CMAD01g: Hysterectomy
  - CMAD01h: Surgery other than for delivery of baby or hysterectomy
- From _CMA_ postpartum mental health conditions:
  - CMAE04a1c: Postpartum depression
  - CMAE04a2c: Postpartum anxiety
  - CMAE04a3c: Postpartum bipolar disorder
  - CMAE04a4c: Postpartum post traumatic stress disorder
  - CMAE04a5c: Postpartum schizophrenia/schizoaffective disorder

## Modeling

We joined the covariate and delta features into a __base__ dataset. To be able to compare the coefficients or feature importances associated with the delta variables in our results, we had to normalize the base dataset using min-max normalization (so all features' ranges were [0, 1]). This approach is usually not robust to outliers, but we had already standardized the numeric features before creating the deltas, so the impact of outliers was minimized. We then looped through the various targets we had selected, and modeled on each.

The outcome variables are categorical (we are predicting a boolean outcome indicating whether an observed pregnancy will result in the selected target morbidity). Historically, medical research surrounding classification problems have relied heavily on logistic regression techniques. However, we contend that there is much more value in **ensemble** and **boosting** methods, which usually have higher predictive power.

`Ensemble methods`, like random forests, bring a lot of benefits to the table.
- Single models are usually subject to a bias/variance tradeoff. For example, an unpruned decision tree can classify every single training data point perfectly, leading to low bias and high variance (overfitting). However, a single decision stump would result in high bias and low variance (underfitting). In practice, we find that employing random forests (an ensemble of trees) leaves bias unaffected while reducing variance, allowing us to get the best of both worlds.
<p align="center">
  <img src="Images/BiasVarianceTradeoff.jpeg" width="600"><br>
  <em>Bias vs. Variance Tradeoff</em><br>
  <em><a href="https://towardsdatascience.com/bias-and-variance-but-what-are-they-really-ac539817e171">Source</a></em>
</p>

- Ensemble methods can take advantage of many different types of models, having each "vote" on the prediction of the output variable. This allows us to take advantage of the benefits of each included models, expecting the law of large numbers (or, in this case, larger numbers) to more often identify the correct classification.
<p align="center">
  <img src="Images/RF_Voting.png" width="600"><br>
  <em>Random Forest voting process</em>
</p>

- In models like random forests, bootstrapping allows individual decision trees in the random forest to "specialize" on different parts of the feature space.

Similarly, `boosting algorithms` also offer higher predictive power.
- Weak learners, like like logistic regression or shallow decision trees, are good at finding general "rules of thumb" because of the associated low variance. On their own, they are not good at solving complicated problems. However, a bunch of weak classifiers that specialize in different parts of the input space can do much better than a single classifier. That is the basis of boosting.
- Each consecutive weak learner in a boosting algorithm specializes in the part of the feature space the previous learners performed poorly on. The resulting classification is found by taking a weighted "vote" among all of the learners, with classifiers that are more "sure" of their prediction having a higher weight. In practice, we see that these boosted weak models outperform individual classifiers.
- Boosting is often robust to overfitting. In practice, we often see the test set error continue to decrease even while the train set error stays constant (or even 0!).
<p align="center">
  <img src="Images/BoostingProcess.png" width="600"><br>
  <em>Boosting process</em>
</p>

For the purposes of our analysis, we will run the following three models for each target variable:
- A `Logistic Regression model`, with the regularization variable tuned
- A `Random Forest model`, with various hyperparameters tuned
- A `Light GBM (gradient boosting machine)`, with various hyperparameters tuned

In practice, we generally see random forests and boosting algorithms outperforming logistic regression models for complicated problems with a large amount of data. However, many of our target variables have a small number of true cases. Therefore, it was plausible that logistic regression could outperform the other more complicated models for some of the output variables. Therefore, we let the model performance metrics themselves (specifically, the F-1 score on the True class) tell us which models did best. Please see the [Modeling](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/Modeling.ipynb) notebook for a detailed run-through of our modeling efforts.

# Analysis of Results
In understanding the results of our models, we were most interested in identifying:
- which models appeared to have the most predictive power for certain target features, and
- which features were most impactful in predicting certain APOs

Models that perform well in predicting our target features show evidence that a machine learning approach could be useful when trying to predict APOs in future patients. Finding features that appear to be important when predicting those outcomes provides us with some explainability and potential areas for future research (i.e. why are these features so predictive of certain APOs?). 

First, we only focus on models where the support for the minority class in our test set (we took a 70/30 split between our train set and test set) is greater than 50. This means that we drop those models where there were fewer than 50 observations of the "positive" instances in our test set, or cases in which the APOs did occur (e.g. there were fewer than 50 cases of miscarriage in our test set, so we decided to drop those models from our analysis). We decided to take this approach because model results can be misleading and uncertain when the support is so low.

We are left with 4 target features: Chronic Hypertension (`ChronHTN`), Postpartum Depression (`CMAE04a1c`), Postpartum Anxiety (`CMAE04a2c`), and Preeclampsia (`PEgHTN`). For these 4 targets, we select the modeling approach (Logistic Regression, Random Forest, LGBM) that achieved the highest F-1 score. We decided to focus on F-1 score because of the large class imbalance in our data (most patients did not have the APOs occur). In this context, false negatives are extremely costly to us, and so we want to place an emphasis on recall. However, we also don't want to dilute our predictions with false positives. The F-1 score allows us to optimize on both recall and precision.

For the models that remain, we extract the top 10 most impactful features, including both covariates and the delta features. Because all of our best models were either LGBMs of Random Forests, we determined feature importance by _Gini importance_, which is a measure of how much the feature decreases impurity on average over all of the trees in the model. For each of the 4 target features, we analyze the model performance and the 10 most important features driving those predictions. This provides us with insight into the feasability of modeling certain APOs as well as the potential drivers of these outcomes. Please see the [Analysis of Results](https://github.com/gabgilling/dse-nichd/blob/main/Notebooks/Analysis%20of%20Results.ipynb) notebook for more information, along with useful visualizations and tables detailing the specifics of our findings.

We believe that our results present promising signs for future research. For the four different APOs, we were able to build models with strong predictive power (with an average F-1 score of ~0.7125). With further iterations in parameter tuning, feature engineering, model refinement, and data acquisition, we believe that these models have the potential to unlock new predictive capabilities in the medical industry. There would be an immense benefit in being able to accurately predict an APO for a patient before it actually occurs, allowing time to take preventative measures.

Additionally, we are able to understand the features that were the most important drivers in our models' predictions. While the feature importance results aren't necessarily conclusive in terms of causality, they do point to possible drivers of these APOs. This provides us with starting areas for future research. If we find that there are certain controllable factors in a mother's health that may affect the likelihood of an APO, then this could inform the care that mothers receive. We hope that these results lead to a more informed understanding of APOs and drive a more informed approach to caring for pregnant women, thereby reducing the cost of APOs throughout the country.

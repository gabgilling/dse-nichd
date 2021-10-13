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

#### Delta Feature Creation
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

# Results

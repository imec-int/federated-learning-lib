# AKI Parameters

as it is unclear to me right now what the correct AKI parameters are, which are being used in the ExaScience model, I'll first investigate what the used parameters are and what could be their corresponding value in the eICU database

It seems that Exascience is using the [Kdigo Classification](https://kdigo.org)

I'm not sure yet if we have all data for enough participants and or how ExaScience worked with missing data. #TODO check with ExaScience

Important, the sql requests are from postgresSQL  


| AKI parameter            | category                 | MIMIC III name                              | MIMIC III location                 | eICU name  | eICU location | unit preferred |
| ------------------------ | ------------------------ | ------------------------------------------- | ---------------------------------- | ---------- | ------------- | -------------- |
| AKI                      | --OUTPUT--               |                                             |                                    |            |               |                |
| AKI_STAGE_7DAY           | --OUTPUT--               |                                             |                                    |            |               |
| ETHNICITY                |                          |                                             | ADMISSIONS                         | ethnicity  | patient       | -              |
| AGE                      |                          | df['ADMITTIME'].dt.year - df['DOB'].dt.year | ADMITTIME: ADMISSIONS,DOB:PATIENTS | age        | patient       | -              |
| GENDER                   |                          | PATIENTS                                    |                                    | gender     | patient       | -              |
| HYPERTENSION             |                          |                                             |                                    |            |               |
| HYPOTHYROIDISM           |                          |                                             |                                    |            |               |
| CONGESTIVE_HEART_FAILURE |                          |                                             |                                    |            |               |
| CARDIAC_ARRHYTHMIAS      |                          |                                             |                                    |            |               |
| ALCOHOL_ABUSE            |                          |                                             |                                    |            |               |
| DRUG_ABUSE               |                          |                                             |                                    |            |               |
| VALVULAR_DISEASE         |                          |                                             |                                    |            |               |
| OBESITY                  |                          |                                             |                                    |            |               |
| PERIPHERAL_VASCULAR      |                          |                                             |                                    |            |               |
| DIABETES_COMPLICATED     |                          |                                             |                                    |            |               |
| LIVER_DISEASE            |                          |                                             |                                    |            |               |
| DIABETES_UNCOMPLICATED   |                          |                                             |                                    |            |               |
| RENAL_FAILURE            |                          |                                             |                                    |            |               |
| UO_RT_24HR               | urine output             |                                             |                                    |            |               |
| UO_RT_12HR               | urine output             |                                             |                                    |            |               |
| UO_RT_6HR                | urine output             |                                             |                                    |            |               |
| CREAT                    | kidigo 7 days creatinine | creat                                       |                                    | creatinine | apacheApsVar  |
| EGFR                     |                          | Estimated Glomerular Filtration Rate        |                                    |            |               |
| TEMPC_MIN                | vitals                   |                                             |                                    |            |               |
| TEMPC_MAX                | vitals                   |                                             |                                    |            |               |
| TEMPC_MEAN               | vitals                   |                                             |                                    |            |               |
| HEARTRATE_MIN            | vitals                   |                                             |                                    |            |               |
| HEARTRATE_MAX            | vitals                   |                                             |                                    |            |               |
| HEARTRATE_MEAN           | vitals                   |                                             |                                    |            |               |
| SPO2_MIN                 | vitals                   |                                             |                                    |            |               |
| SPO2_MAX                 | vitals                   |                                             |                                    |            |               |
| SPO2_MEAN                | vitals                   |                                             |                                    |            |               |
| MEANBP_MIN               | vitals                   |                                             |                                    |            |               |
| MEANBP_MAX               | vitals                   |                                             |                                    |            |               |
| MEANBP_MEAN              | vitals                   |                                             |                                    |            |               |
| DIASBP_MIN               | vitals                   |                                             |                                    |            |               |
| DIASBP_MAX               | vitals                   |                                             |                                    |            |               |
| DIASBP_MEAN              | vitals                   |                                             |                                    |            |               |
| RESPRATE_MIN             | vitals                   |                                             |                                    |            |               |
| RESPRATE_MAX             | vitals                   |                                             |                                    |            |               |
| RESPRATE_MEAN            | vitals                   |                                             |                                    |            |               |
| SYSBP_MIN                | vitals                   |                                             |                                    |            |               |
| SYSBP_MAX                | vitals                   |                                             |                                    |            |               |
| SYSBP_MEAN               | vitals                   |                                             |                                    |            |               |
| ALBUMIN_MIN              |                          | LABEVENTS                                   |                                    |            |               |
| ALBUMIN_MAX              |                          | LABEVENTS                                   |                                    |            |               |
| ANIONGAP_MIN             |                          | LABEVENTS                                   |                                    |            |               |
| ANIONGAP_MAX             |                          | LABEVENTS                                   |                                    |            |               |
| BANDS_MIN                |                          | LABEVENTS                                   |                                    |            |               |
| BANDS_MAX                |                          | LABEVENTS                                   |                                    |            |               |
| BICARBONATE_MIN          |                          | LABEVENTS                                   |                                    |            |               |
| BICARBONATE_MAX          |                          | LABEVENTS                                   |                                    |            |               |
| BILIRUBIN_MIN            |                          | LABEVENTS                                   |                                    |            |               |
| BILIRUBIN_MAX            |                          | LABEVENTS                                   |                                    |            |               |
| BUN_MIN                  |                          | LABEVENTS (blood urea nitrogen)              |                                    |            |               |                |
| BUN_MAX                  |                          | LABEVENTS                                   |                                    |            |               |                |
| CHLORIDE_MIN             |                          | LABEVENTS                                   |                                    |            |               |
| CHLORIDE_MAX             |                          | LABEVENTS                                   |                                    |            |               |
| CREATININE_MIN           |                          | LABEVENTS                                   |                                    |            |               |
| CREATININE_MAX           |                          | LABEVENTS                                   |                                    |            |               |
| GLUCOSE_MIN              | vitals?                  | LABEVENTS                                   |                                    |            |               |
| GLUCOSE_MAX              | vitals?                  | LABEVENTS                                   |                                    |            |               |
| GLUCOSE_MEAN             | vitals?                  | LABEVENTS                                   |                                    |            |               |
| HEMATOCRIT_MIN           |                          | LABEVENTS                                   |                                    |            |               |
| HEMATOCRIT_MAX           |                          | LABEVENTS                                   |                                    |            |               |
| HEMOGLOBIN_MIN           |                          | LABEVENTS                                   |                                    |            |               |
| HEMOGLOBIN_MAX           |                          | LABEVENTS                                   |                                    |            |               |
| INR_MIN                  |                          | LABEVENTS(international normalized ratio)   |                                    |            |               |
| INR_MAX                  |                          | LABEVENTS                                   |                                    |            |               |
| LACTATE_MIN              |                          | LABEVENTS                                   |                                    |            |               |
| LACTATE_MAX              |                          | LABEVENTS                                   |                                    |            |               |
| PLATELET_MIN             |                          | LABEVENTS                                   |                                    |            |               |
| PLATELET_MAX             |                          | LABEVENTS                                   |                                    |            |               |
| POTASSIUM_MIN            |                          | LABEVENTS                                   |                                    |            |               |
| POTASSIUM_MAX            |                          | LABEVENTS                                   |                                    |            |               |
| PT_MIN                   | prothrombin time         | LABEVENTS                                   |                                    |            |               |
| PT_MAX                   |                          | LABEVENTS                                   |                                    |            |               |
| PTT_MIN                  |                          | LABEVENTS(partial throm- boplastin time)    |                                    |            |               |
| PTT_MAX                  |                          | LABEVENTS(partial throm- boplastin time)    |                                    |            |               |
| SODIUM_MIN               |                          | LABEVENTS                                   |                                    |            |               |
| SODIUM_MAX               |                          | LABEVENTS                                   |                                    |            |               |
| WBC_MIN                  | (white blood count)      | LABEVENTS                                   |                                    |            |               |
| WBC_MAX                  |                          | LABEVENTS                                   |                                    |            |               |

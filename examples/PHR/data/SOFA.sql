/* in this sql we retrieve the columns for parameters which are of influence for the SOFA score
 */
/* Ademhaling: PaO2/FiO2 (kPa) */
SELECT patientunitstayid,
    pao2,
    fio2,
    pao2 / fio2 as ademhaling
FROM eicu_crd.apacheapsvar;
-- OR
/*
 SELECT patientunitstayid,
 pao2,
 fio2,
 pao2 / fio2 as respiratory
 FROM eicu_crd.apachepredvar 
 
 */
/* Functioneren zenuwstelsel: Glasgow-comaschaal */
SELECT patientunitstayid,
 eyes + verbal + motor as glasgow_coma_scale
 FROM eicu_crd.apacheapsvar;
/* Functioneren Hart/bloedsomloop: Gemiddelde bloeddruk (MAP) 
 needs: MAP, dopamine, dobutamin, epinephrine, norepinephrine
 MAP = (SBP + 2* DBP)/3 
 ==> SBP = pasystolic
 ==> DBP = padiastolic
 TODO: dopamine:  
 when lower(drugname) like '%(ml/hr)%' then round(cast(drugrate as numeric) / 3, 3) -- rate in ml/h * 1600 mcg/ml / 80 kg / 60 min, to convert in mcg/kg/min
 when lower(drugname) like '%(mcg/kg/min)%' then cast(drugrate as numeric)
 */
SELECT v.patientunitstayid,
 (v.pasystolic + 2 * v.padiastolic) / 3 as MAP,
 i.patientunitstayid,
 i.drugname,
 i.drugrate
 FROM eicu_crd.vitalperiodic v
 FULL OUTER JOIN eicu_crd.infusiondrug i
 ON v.patientunitstayid = i.patientunitstayid
 WHERE lower(drugname) like '%dopamine%'
 or lower(drugname) like '%dobutamin%'
 or lower(drugname) like '%epinephrine%'
 or lower(drugname) like '%norepinephrine%'
 ORDER BY i.patientunitstayid;
/* Leverfunctie: Bilirubine-concentratie */
SELECT patientunitstayid,
 bilirubin as leverfunctie
 FROM eicu_crd.apacheapsvar;

/* Bloedstolling: Bloedplaatjes-concentratie */
SELECT patientunitstayid,
    labname as bloedstolling,
    labresult / 1000
FROM eicu_crd.lab
WHERE labname like '%platelet%';
/* Nierfunctie: Creatinine-concentratie */
SELECT patientunitstayid,
    creatinine as nierfunctie
FROM eicu_crd.apacheapsvar;
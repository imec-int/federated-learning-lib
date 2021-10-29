CREATE SCHEMA results;

CREATE TABLE results.nbAdmissionsByGender(
    sourceDatabase CHARACTER VARYING(64),
    gender CHARACTER VARYING(64),
    admissionHour INTEGER,
    count INTEGER
);
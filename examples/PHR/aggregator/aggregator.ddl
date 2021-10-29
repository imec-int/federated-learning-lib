CREATE SCHEMA results;

CREATE TABLE results.maleFemaleRatio(
    sourceDatabase CHARACTER VARYING(64),
    nbMale INTEGER,
    nbFemale INTEGER,
    nbOther INTEGER,
    nbUnknown INTEGER
);
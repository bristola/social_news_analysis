ALTER USER postgres PASSWORD 'admin';

CREATE TABLE JOB (
    ID          SERIAL PRIMARY KEY,
    TOPIC       VARCHAR(20)
);

CREATE TABLE RUN (
    ID          SERIAL PRIMARY KEY,
    JOB_ID      INTEGER REFERENCES JOB(ID),
    RUN_TIME    TIMESTAMP
);

CREATE TABLE SENTIMENT (
    RUN_ID      INTEGER REFERENCES RUN(ID),
    TYPE        VARCHAR(10),
    VALUE       DECIMAL,
    WEIGHT      INTEGER
);

CREATE TABLE MOOD (
    RUN_ID      INTEGER REFERENCES RUN(ID),
    TYPE        VARCHAR(10),
    MOOD        VARCHAR(15),
    AMOUNT      INTEGER
);

CREATE TABLE EMOTICON (
    RUN_ID      INTEGER REFERENCES RUN(ID),
    TYPE        VARCHAR(10),
    EMOTE        VARCHAR(15),
    AMOUNT      INTEGER
);

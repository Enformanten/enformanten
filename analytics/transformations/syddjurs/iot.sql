create or replace table "1_RAW_SYDDJURS_IOT_META" (Navn	varchar, 
DevEUI	varchar,
Placering varchar,
Beskrivelse varchar);

create or replace table "1_RAW_SYDDJURS_IOT_SENSOR_DESC" (SensorID	varchar,
SensorNavn	varchar,
Forbrugstype	varchar,
Maaleenhed	varchar,
Faktor	varchar,
srcTagID	varchar,
Sensorplacering1	varchar,
Sensorplacering2	varchar
);

create or replace table "1_RAW_SYDDJURS_IOT_VALUES" (Data Variant);

create or replace table "1_RAW_SYDDJURS_IOT_VALUES_HISTORY" (ID varchar, 
SensorID varchar, 
Dato varchar, 
Timestamp varchar,
LokaleID varchar,
ENhedID varchar,
SensorValue varchar,
Lokalenavn varchar);

create or replace view "2_STANDARD_SYDDJURS_IOT" as
select d.SensorNavn, d.Forbrugstype, d.Maaleenhed, d.Faktor, d.Sensorplacering1, d. Sensorplacering2, h.sensorid as sensorid, v.data:From::date as dato, v.data:From::timestamp::time as time, h.LokaleID::int as LokaleID, h.ENhedID::int as EnhedID, v.data:Value as Value, h.LokaleNavn as LokaleNavn from "1_RAW_SYDDJURS_IOT_SENSOR_DESC" d, "1_RAW_SYDDJURS_IOT_VALUES" v, lateral flatten(input=>data), (select distinct sensorid, lokalenavn, lokaleid, enhedid from "1_RAW_SYDDJURS_IOT_VALUES_HISTORY") h where d.srcTagID = v.data:TagID::text and h.sensorid = d.sensorid;

create or replace view "2_STANDARD_SYDDJURS_IOT_HISTORY" as
select d.SensorNavn, d.Forbrugstype, d.Maaleenhed, d.Faktor, d.Sensorplacering1, d. Sensorplacering2, v.SensorID, v.Dato::date as dato, v.Timestamp::time as time, v.LokaleID::int as LokaleID, v.ENhedID::int as EnhedID, v.SensorValue::float as SensorValue, v.LokaleNavn as LokaleNavn from "1_RAW_SYDDJURS_IOT_SENSOR_DESC" d, "1_RAW_SYDDJURS_IOT_VALUES_HISTORY" v where v.SensorID = d.SensorID;

create or replace view "2_STANDARD_SYDDJURS_IOT_JOINED" as
select distinct * from "2_STANDARD_SYDDJURS_IOT_HISTORY" union all select * from "2_STANDARD_SYDDJURS_IOT";

create or replace view "3_CLEANSED_SYDDJURS_IOT" as
select s.lokaleid, s.sensornavn, s.dato as date, s.time, s.forbrugstype, s.sensorvalue::float as value,
SPLIT_PART(sensornavn, '_', 2) as ending_navn from "2_STANDARD_SYDDJURS_IOT_JOINED" s where ending_navn in  ('Temperature', 'Humidity', 'CO2', 'Motion', 'Light', 'Humidity');
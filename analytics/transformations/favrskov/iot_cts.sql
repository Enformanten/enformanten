create or replace table "1_RAW_ZURFACE_DATA" (data variant); -- Used both for Favrskov and Aarhus Zurface-data

create or replace view "2_STANDARD_ZURFACE_DATA" as -- Used both for Favrskov and Aarhus Zurface-data
select 
$1:deviceId::string as deviceId,
$1:Battery:value::float as Battery,
$1:CO2:value::int as CO2,
$1:Humidity:value::float as Humidity,
$1:IAQ:value::float as IAQ,
$1:Light:value::int as Light,
$1:Sound:value::int as Sound,
$1:Temperature:value::float as Temperature,
$1:timestamp::int as timestamp_unix,
to_timestamp(timestamp_unix) as timestamp
from "1_RAW_ZURFACE_DATA" where ARRAY_CONTAINS('deviceId'::variant, OBJECT_KEYS($1));

create or replace table "1_RAW_FAVRSKOV_IOT_META" (NR varchar, Navn varchar, Alias varchar, Deviceid varchar);

create or replace view "3_CLEANSED_FAVRSKOV_IOT" as
select distinct Navn, i.DEVICEID::STRING AS SENSORNAVN, TIMESTAMP::DATE AS DATE, TIMESTAMP::TIME AS TIME, Replace(CO2, ',', '.')::float as CO2,
REPLACE(SOUND, ',', '.')::float as SOUND,REPLACE(LIGHT, ',', '.')::float as LIGHT,
REPLACE(IAQ, ',', '.')::float as IAQ,REPLACE(TEMPERATURE, ',', '.')::float as TEMPERATURE,REPLACE(HUMIDITY, ',', '.')::float as HUMIDITY 
from "2_STANDARD_ZURFACE_DATA" i, "1_RAW_FAVRSKOV_IOT_META" m where i.DEVICEID::STRING = m.deviceid order by date, time desc;

create or replace table "1_RAW_FAVRSKOV_CTS_HISTORY" (Timestamp varchar,
CO2  varchar,
Motorventil varchar,
Rum_tilstand varchar,
Motorspjaeld_indblaesning  varchar,
Motorspjaeld_udblaesning  varchar,
Temperatur   varchar,
VAV_spjaeld  varchar,
Ventilationskanal_1 varchar,
Ventilationskanal_2 varchar,
Lokale varchar,
Dato varchar,
Time varchar
);

create or replace view "2_STANDARD_FAVRSKOV_CTS_HISTORY" as
select Timestamp, CO2, Motorventil,Rum_tilstand ,Motorspjaeld_indblaesning  ,Motorspjaeld_udblaesning ,Temperatur   ,VAV_spjaeld ,Ventilationskanal_1,Ventilationskanal_2 ,Lokale, Dato,
Time::time as Time from "1_RAW_FAVRSKOV_CTS_HISTORY";

create or replace table "1_RAW_FAVRSKOV_CTS_ENERGYCONSUMPTION_HISTORY" (Timestamp varchar,
Dato varchar,
Time varchar,
Running_total varchar,
total_consumption varchar);

create or replace view "2_STANDARD_FAVRSKOV_CTS_ENERGYCONSUMPTION_HISTORY" as
select * from "1_RAW_FAVRSKOV_CTS_ENERGYCONSUMPTION_HISTORY";
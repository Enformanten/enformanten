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

create table "1_RAW_AARHUS_IOT_META" as
select distinct lokaleid, sensornavn from "2_STANDARD_AARHUS_IOT_HISTORY";

create or replace table "1_RAW_AARHUS_IOT_HISTORY" as
select split(split(METADATA$FILENAME, '/')[2], '-')[0]::string as id, $1 as timestamp, $2 as deviceid, $3 as CO2, $4 as SOUND, $5 as LIGHT, $6 as IAQ, $7 as TEMPERATURE, $8 as HUMIDITY 
 from @ZURFACE_HISTORY_STAGE;

 create or replace view "2_STANDARD_AARHUS_IOT_HISTORY" as
 select id::string AS LOKALEID, DEVICEID::STRING AS SENSORNAVN, Try_to_timestamp(TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS')::DATE AS DATE, Try_to_timestamp(TIMESTAMP, 'DD-MM-YYYY HH24:MI:SS')::TIME AS TIME, Replace(CO2, ',', '.')::float as CO2,REPLACE(SOUND, ',', '.')::float as SOUND,REPLACE(LIGHT, ',', '.')::float as LIGHT,REPLACE(IAQ, ',', '.')::float as IAQ,REPLACE(TEMPERATURE, ',', '.')::float as TEMPERATURE,REPLACE(HUMIDITY, ',', '.')::float as HUMIDITY from "1_RAW_AARHUS_IOT_HISTORY";

create or replace view "3_CLEANSED_AARHUS_IOT" as
select distinct * from "2_STANDARD_AARHUS_IOT_HISTORY"
union all
 select distinct lokaleid, DEVICEID::STRING AS SENSORNAVN, TIMESTAMP::DATE AS DATE, TIMESTAMP::TIME AS TIME, Replace(CO2, ',', '.')::float as CO2,REPLACE(SOUND, ',', '.')::float as SOUND,REPLACE(LIGHT, ',', '.')::float as LIGHT,REPLACE(IAQ, ',', '.')::float as IAQ,REPLACE(TEMPERATURE, ',', '.')::float as TEMPERATURE,REPLACE(HUMIDITY, ',', '.')::float as HUMIDITY from "2_STANDARD_ZURFACE_DATA" i, "1_RAW_AARHUS_IOT_META" m where i.DEVICEID::STRING = m.sensornavn order by date, time desc;

select * from "3_CLEANSED_AARHUS_IOT" where date is not null order by date desc, time desc;
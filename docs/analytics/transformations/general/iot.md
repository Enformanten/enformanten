``` sql
create or replace view "3_CLEANSED_CTS_X_IOT" as
with iot_aarhus as (select distinct s.date, 
date_trunc('HOUR', TIME) as time,
TIMESTAMP_NTZ_FROM_PARTS(s.date, date_trunc('HOUR', TIME)) as timestamp,
date_trunc('HOUR', date_trunc('HOUR', TIME)) as TIME_GROUP,
avg(CO2) as CO2,
avg(SOUND) as SOUND,
avg(LIGHT) as LIGHT,
avg(IAQ) as IAQ,
avg(TEMPERATURE) as TEMPERATURE,
avg(HUMIDITY) as HUMIDITY, 
null as motion, 
Rum_ID as ID,
'Aarhus' as KOMMUNE, 
'Strandskolen' as SKOLE,
concat(kommune, '-',rum_id) as kommune_lokale
from "3_CLEANSED_AARHUS_IOT" s, "2_STANDARD_AARHUS_LOKALE_STAMDATA_AREAL" m where trim(s.LOKALEID::string) = m.RUM_ID::string group by s.date, time_group, time, m.rum_id)

,iot_syddjurs as (
select distinct s.date, 
s.TIME as TIME, 
TIMESTAMP_NTZ_FROM_PARTS(s.date, date_trunc('HOUR', TIME)) as timestamp,
date_trunc('HOUR', TIME) as TIME_GROUP,
avg("'CO2'"::float) as co2, 
null as sound,
avg("'Belysningsstyrke'"::float) as light, 
null as IAQ,
avg("'Temperature'"::float) as temp,
avg("'Relativ Luftfugtighed'"::float) as Humid, 
sum("'Quantity'"::float) as motion, 
RIGHT(LOKALENUMMER, length(LOKALENUMMER) - 4) as ID, 
'Syddjurs' as KOMMUNE, 
'Thorsager Skole' as SKOLE,
concat(kommune, '-',id) as kommune_lokale
from "3_CLEANSED_SYDDJURS_IOT" PIVOT(AVG(value) FOR FORBRUGSTYPE IN ('Temperature', 'CO2', 'Belysningsstyrke', 'Quantity', 'Light', 'Relativ Luftfugtighed')) as s, "2_STANDARD_SYDDJURS_LOKALE_STAMDATA_AREAL" m where s.LOKALEID = m.LOKALEID group by ID, s.date, s.time, m.lokalenummer
),

cts_favrskov as (
select Concat(Right(Left(s.Timestamp, 10), 4), '-', substr(Left(s.Timestamp, 10), 4, 2), '-', Left(Left(s.Timestamp, 10), 2))::DATE as DATE, 
s.TIME as TIME, 
TIMESTAMP_NTZ_FROM_PARTS(date, date_trunc('HOUR', TIME)) as timestamp, 
date_trunc('HOUR', TIME) as TIME_GROUP,
avg(s.CO2::float) as co2, 
null as sound,
null as light, 
null as IAQ,
avg(REPLACE(s.TEMPERATUR, ',', '.')::float) as temp,
null as Humid, 
null as motion, 
s.LOKALE::string as ID,
'Favrskov' as KOMMUNE, 
'Rønbækskolen' as SKOLE,
concat(kommune, '-',id) as kommune_lokale
from "2_STANDARD_FAVRSKOV_CTS_HISTORY" s, "2_STANDARD_FAVRSKOV_LOKALE_STAMDATA_AREAL" m where s.LOKALE = m.Lokalenr
group by ID, date, s.Time, m.Lokalenr
),

iot_favrskov as(
select distinct s.date, 
date_trunc('HOUR', TIME) as time,
TIMESTAMP_NTZ_FROM_PARTS(s.date, date_trunc('HOUR', TIME)) as timestamp,
date_trunc('HOUR', date_trunc('HOUR', TIME)) as TIME_GROUP,
avg(CO2) as CO2,
avg(SOUND) as SOUND,
avg(LIGHT) as LIGHT,
avg(IAQ) as IAQ,
avg(TEMPERATURE) as TEMPERATURE,
avg(HUMIDITY) as HUMIDITY, 
null as motion, 
navn as ID,
'Favrskov' as KOMMUNE, 
'Rønbækskolen' as SKOLE,
concat(kommune, '-',navn) as kommune_lokale
from "3_CLEANSED_FAVRSKOV_IOT" s group by s.date, time,s.navn
)

select * from iot_aarhus
union all 
select * from iot_syddjurs
union all 
select * from cts_favrskov
union all
select * from iot_favrskov;


create or replace table "4_FEATURIZ_CTS_X_IOT" as
select distinct * from "3_CLEANSED_CTS_X_IOT";

```
create or replace table "1_RAW_DRIFTOPTIMERINGSMODEL" 
(DATE varchar, TIME VARCHAR, DATETIME varchar, ID varchar, KOMMUNE VARCHAR, IN_USE INT, ANOMALY_SCORE FLOAT);

create or replace view "2_STANDARD_DRIFTOTIMERINGSMODEL" as
select date::date as date, 
date_trunc(HOUR, timestamp_from_parts(date, time)::timestamp)::time as time, 
date_trunc(HOUR, timestamp_from_parts(date, time)::timestamp) as datetime, 
id, 
kommune, 
IN_USE as IF_ANOMALY, 
anomaly_score as IF_anomaly_score, 
concat(kommune, '-', ID) as KOMMUNE_LOKALE 
from "1_RAW_DRIFTOPTIMERINGSMODEL"; 

create or replace view "3_CLEANSED_DRIFTOPTIMERINGSMODEL" as
select date, time, datetime, id, kommune, sum(if_anomaly) as brugte_kvarter, 
iff(brugte_kvarter > 0, 1, brugte_kvarter) as in_use, kommune_lokale
from "2_STANDARD_DRIFTOTIMERINGSMODEL"  
where if_anomaly is not null 
group by date, time, datetime, id, kommune, kommune_lokale;

create or replace table "4_FEATURIZ_DRIFTOPTIMERINGSMODEL" as
select distinct * from "3_CLEANSED_DRIFTOPTIMERINGSMODEL";

---Bookings x Drift---

create or replace view "3_CLEANSED_BOOKINGS_X_DRIFTOPTIMERINGSMODEL" as
select b.*, d.in_use, iff(b.booket = 1 and d.in_use = 1, 1, 0) as brugt_booking from "4_FEATURIZ_DRIFTOPTIMERINGSMODEL" d
 join "4_FEATURIZ_BOOKINGS_TIME" b on d.kommune_lokale = b.kommune_lokale and d.datetime = b.timestamp
;

create or replace table "4_FEATURIZ_BOOKINGS_X_DRIFTOPTIMERINGSMODEL"
as select * from "3_CLEANSED_BOOKINGS_X_DRIFTOPTIMERINGSMODEL";


---DATA---
create or replace view "2_STANDARD_DRIFTOPTIMERING_DATA" as
select 
distinct
r.ID,
r.KOMMUNE,
r.SKOLE,
d.DATE,
d.TIME,
d.DAYNAME,
d.TIDSPUNKT_TYPE,
k.TYPE,
k.NAVN,
avg(i.CO2) as co2,
avg(i.TEMP) as temp,
sum(i.MOTION) as motion,
avg(i.IAQ) as IAQ,
min(b.booket) as booket,
iff(s.starttid is not null and s.sluttid is not null, 1, null) as skemalagt
FROM
"4_FEATURIZ_LOKALER" r
CROSS JOIN "KALENDER_KVARTER" d
LEFT JOIN "1_RAW_KALENDER" k on d.date = k.date 
LEFT JOIN "CTS_X_IOT_KVARTER" i on r.id = i.id and r.kommune = i.kommune and r.skole = i.skole and d.date = i.date and d.time = i.timestamp::time
LEFT JOIN "BOOKINGER_KVARTER" b on r.id = b.id and r.kommune = b.kommune and r.skole = b.skole and d.date = b.dato and d.time = b.time
LEFT JOIN "2_STANDARD_SKEMAER" s on r.id = s.rumid and r.kommune = s.kommune and r.skole = s.skole and d.dayname = s.dag and d.time >= s.starttid and d.time < s.sluttid and d.date > '2022-08-07' and d.date < '2023-06-24' and k.TYPE = 'Normal Dag'
where co2 is not null and ((r.KOMMUNE = 'Aarhus' and (d.DATE < '2023-05-15' or d.DATE > '2023-09-21')) or (r.KOMMUNE = 'Favrskov' and (d.DATE < '2023-05-15' or d.DATE > '2023-09-21')) or r.kommune = 'Syddjurs') and d.date > '2022-09-01'
GROUP BY r.id, r.kommune, r.skole, d.date, d.time, d.dayname, d.tidspunkt_type, s.starttid, s.sluttid, k.type, k.navn;

--Skemaer
create or replace view "2_STANDARD_SKEMAER" as
select n.rumid, dag, starttid, sluttid, 'Aarhus' as KOMMUNE, 'Strandskolen' as SKOLE from "1_RAW_AARHUS_SKEMA" s INNER join "1_RAW_AARHUS_LOKALER_MED_NAVNE" n on n.navn = s.rumid
union all
select *, 'Syddjurs' as KOMMUNE, 'Thorsager Skole' as SKOLE from "1_RAW_SYDDJURS_SKEMA"
union all
select *, 'Favrskov' as KOMMUNE, 'Rønbækskolen' as SKOLE from "1_RAW_FAVRSKOV_SKEMA";


--Kalender
create view "KALENDER_KVARTER" as
select dateadd(minute, row_number() over (order by null) * 15, '2022-01-01 00:00') as timestamp, 
timestamp::date as date, timestamp::time as time, 
decode(DAYNAME(date), 'Mon','Mandag', 'Tue','Tirsdag', 'Wed', 'Onsdag', 'Thu', 'Torsdag', 'Fri', 'Fredag', 'Sat', 'Loerdag', 'Sun', 'Soendag') as dayname , 
DAYOFWEEKISO(date) as weekdaynum, weekofyear(timestamp) as weekno, 
iff(time >= '16:00', 'Fritid', iff(weekdaynum > 5, 'Fritid', 'Skole')) as TIDSPUNKT_TYPE 
from table(generator(rowcount => 70080)) g;


--Bookinger
create or replace view "BOOKINGER_KVARTER" as
SELECT 
    d.date as dato,
    d.TIME,
    concat(d.date::date, ' ', d.time)::datetime as timestamp,
    r.KOMMUNE,
    r.SKOLE,
    r.ID,
    concat(r.kommune, '-', r.id) as kommune_lokale,
    CONCAT(d.date::STRING, '-', d.TIME, '-', r.KOMMUNE) AS KOMMUNE_DATO_TIME,
    IFF(d.time >= b.start_tid, IFF(d.time <= b.slut_tid, 1, 0), 0) AS booket,
    IFF(booket = 1, start_tid, NULL) AS starttid,
    IFF(booket = 1, slut_tid, NULL) AS sluttid,
    IFF(booket = 1, lejer, NULL) AS lejerid,
    IFF(booket = 1, b.type, NULL) AS typebooking,
    CAST(IFF(booket = 1, timer_format, NULL) AS FLOAT) AS booket_tid
FROM
    "KALENDER_KVARTER" d
    CROSS JOIN "4_FEATURIZ_LOKALER" r
    LEFT JOIN "4_FEATURIZ_BOOKINGS" b ON d.date::date = iff(b.kommune = 'Aarhus', try_to_date(b.dato, 'dd-mm-yyyy'), try_to_date(b.dato, 'yyyy-mm-dd')) and r.id = b.id and r.kommune = b.kommune and r.skole = b.skole
WHERE
    booket = 1
GROUP BY
    d.date,
    TIME,
    slut_tid,
    start_tid,
    timer_format,
    r.KOMMUNE,
    r.ID,
    r.skole,
    lejer,
    b.type
ORDER BY
    date::date,
    time,
    kommune, 
    id;


--IoT/CTS-data
create or replace view "CTS_X_IOT_KVARTER" as
with iot_aarhus as (
select distinct 
s.date, 
time_slice(TIMESTAMP_NTZ_FROM_PARTS(s.date,  TIME), 15, 'MINUTE')::time as time,
time_slice(TIMESTAMP_NTZ_FROM_PARTS(s.date,  TIME), 15, 'MINUTE') as timestamp,
avg(CO2) as CO2,
avg(SOUND) as SOUND,
avg(LIGHT) as LIGHT,
avg(IAQ) as IAQ,
avg(TEMPERATURE) as temp,
avg(HUMIDITY) as humid, 
null as motion, 
Rum_ID as ID,
'Aarhus' as KOMMUNE, 
'Strandskolen' as SKOLE,
concat(kommune, '-',rum_id) as kommune_lokale
from "3_CLEANSED_AARHUS_IOT" s, "2_STANDARD_AARHUS_LOKALE_STAMDATA_AREAL" m where trim(s.LOKALEID::string) = m.RUM_ID::string group by s.date, time, m.rum_id)

,iot_syddjurs as (
select distinct s.date, 
time_slice(TIMESTAMP_NTZ_FROM_PARTS(s.date,  TIME), 15, 'MINUTE')::time as time,
time_slice(TIMESTAMP_NTZ_FROM_PARTS(s.date,  s.TIME), 15, 'MINUTE') as timestamp,
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
select distinct Concat(Right(Left(s.Timestamp, 10), 4), '-', substr(Left(s.Timestamp, 10), 4, 2), '-', Left(Left(s.Timestamp, 10), 2))::DATE as DATE, 
time_slice(TIMESTAMP_NTZ_FROM_PARTS(date,  TIME), 15, 'MINUTE')::time as time,
time_slice(TIMESTAMP_NTZ_FROM_PARTS(date,  TIME), 15, 'MINUTE') as timestamp,
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
select distinct 
s.date, 
time_slice(TIMESTAMP_NTZ_FROM_PARTS(s.date,  TIME), 15, 'MINUTE')::time as time,
time_slice(TIMESTAMP_NTZ_FROM_PARTS(s.date,  TIME), 15, 'MINUTE') as timestamp,
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
select * from iot_favrskov
union all
select * from cts_favrskov;



---TRAINING---
create or replace view "3_CLEANSED_DRIFTOPTIMERING_TRAINING"
as select distinct * from "2_STANDARD_DRIFTOPTIMERING_DATA" where date < convert_timezone('Europe/Copenhagen', CURRENT_TIMESTAMP)::date; -- where date > 6 months (future) ;

create or replace table "4_FEATURIZ_DRIFTOPTIMERING_TRAINING"
as select * from "3_CLEANSED_DRIFTOPTIMERING_TRAINING";

---PREDICT---
create or replace view "3_CLEANSED_DRIFTOPTIMERING_PREDICT" as
with unpredicted_data as(
select distinct t.* from "2_STANDARD_DRIFTOPTIMERING_DATA" t
LEFT JOIN "1_RAW_DRIFTOPTIMERINGSMODEL" r on r.date = t.date and r.time = t.time and r.id = t.id and r.kommune = t.kommune
where r.id is null order by date asc
),
unpredicted_rooms_dates as(
select distinct kommune, skole, id, date from unpredicted_data order by date
)

select distinct t.* from "2_STANDARD_DRIFTOPTIMERING_DATA" t
LEFT JOIN unpredicted_rooms_dates d on d.kommune = t.kommune and d.skole = t.skole and d.id = t.id and d.date = t.date
where d.id is not null and d.date < convert_timezone('Europe/Copenhagen', CURRENT_TIMESTAMP)::date;

create or replace table "4_FEATURIZ_DRIFTOPTIMERING_PREDICT"
as select * from "3_CLEANSED_DRIFTOPTIMERING_PREDICT";



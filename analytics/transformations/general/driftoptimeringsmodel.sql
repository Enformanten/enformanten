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
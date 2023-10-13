create or replace view "3_CLEANSED_PASSIVTIMER" as
select timestamp, 
date, 
time, 
year, 
month, 
monthname, 
monthno, 
kommune, 
iff(sum(booket) > 0, 0, 1) as passivtime, 
kommune_dato_time 
from (
SELECT d.timestamp, d.date, d.time, year(d.date::date)::string as year, month(d.date::date)::string as month, monthname(d.date::date) as monthname, month(d.date::date)::int as monthno,
r.kommune, sum(ifnull(booket, 0)) as booket, concat(r.kommune, '-', d.timestamp) as kommune_dato_time
FROM "4_FEATURIZ_DATOER" d
CROSS JOIN "4_FEATURIZ_LOKALER" r
LEFT JOIN "4_FEATURIZ_BOOKINGS_TIME" b ON d.Timestamp = b.Timestamp AND r.id = b.id and r.kommune = b.kommune
where d.tidspunkt_type = 'Fritid' and date <= current_date()
group by d.date, d.time, d.timestamp, r.kommune, kommune_dato_time order by timestamp asc) 
group by timestamp, date, time, year, month, monthname, monthno, kommune, kommune_dato_time 
order by timestamp asc;

create or replace table "4_FEATURIZ_PASSIVTIMER" as
select * from "3_CLEANSED_PASSIVTIMER";


create or replace view "3_CLEANSED_MINIMUM_EL" as
with Aarhus as (
select  'Aarhus' as Kommune, DATO, TIME, SUM(VALUE::float) as elforbrug from "3_CLEANSED_AARHUS_ENERGIDATA" where measuretype = 'electricity' and key = 3261220102 group by dato, time
)
,Aarhus_minimum as (
select * from Aarhus where elforbrug > 1 and time < '07:00' order by elforbrug asc limit 100
)
,Syddjurs as (
select 'Syddjurs' as Kommune, dato, time, sum(maaling::float) as elforbrug from "3_CLEANSED_SYDDJURS_ENERGIDATA" where enhedid in (216, 305) and forbrugstype = 'El_Samlet' group by dato, time 
)
,Syddjurs_minimum as (
select * from Syddjurs where elforbrug > 1 and time < '07:00' order by elforbrug asc limit 100
)
,Favrskov as (
select 'Favrskov' as Kommune, DATE, TIME, SUM(VALUE::float) as elforbrug from "3_CLEANSED_FAVRSKOV_ENERGIDATA" where tagid = 74 group by date, time
)
,Favrskov_minimum as (
select * from Favrskov where elforbrug > 1 and time < '07:00' order by elforbrug asc limit 100
)
select kommune, avg(elforbrug) as minimum_el, null as manuel_minimum from Aarhus_minimum group by kommune
union all
select kommune, avg(elforbrug) as minimum_el, 2.5 as manuel_minimum from Syddjurs_minimum group by kommune
union all
select kommune, avg(elforbrug) as minimum_el, null as manuel_minimum from Favrskov_minimum group by kommune;

create or replace table "4_FEATURIZ_MINIMUM_EL" as
select * from "3_CLEANSED_MINIMUM_EL";
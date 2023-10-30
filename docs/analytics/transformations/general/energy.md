```sql 
create or replace view "3_CLEANSED_ENERGIDATA" as
select KEY as MAALER_ID, 
DATO as DATO, 
MEASURETYPE as measure_type, 
VALUE::float, 
ENHED, 
TIME as TIME, 
concat(dato, ' ', time)::datetime as timestamp, 
concat(dato::string,'-Aarhus') as KOMMUNE_DATO, 
concat('Aarhus-', timestamp) as KOMMUNE_DATO_TIME, 
'Aarhus' as KOMMUNE, 
'Strandskolen' as SKOLE 
from "3_CLEANSED_AARHUS_ENERGIDATA" -- Aarhus

union all

select ENHEDID as MAALER_ID, 
DATO::date as DATO, 
FORBRUGSTYPE as measure_type, 
MAALING::string::float as VALUE, 
MAALEENHED as ENHED, 
TIME as TIME,
concat(dato, ' ', time)::datetime as timestamp, 
concat(dato::string,'-Syddjurs') as KOMMUNE_DATO, 
concat('Syddjurs-', timestamp) as KOMMUNE_DATO_TIME, 
'Syddjurs' as KOMMUNE, 
'Thorsager Skole' as SKOLE  
from "3_CLEANSED_SYDDJURS_ENERGIDATA" -- Syddjurs

union all 

select m.TAGID as MAALER_ID, 
v.DATE as DATO, 
m.ConsumptionType as measure_type, 
v.VALUE::float as VALUE, 
m.UNIT as ENHED, 
v.TIME as TIME, 
concat(dato, ' ', time)::datetime as timestamp, 
concat(dato::string,'-Favrskov') as KOMMUNE_DATO, 
concat('Favrskov-', timestamp) as KOMMUNE_DATO_TIME, 
'Favrskov' as KOMMUNE, 
'Rønbækskolen' as SKOLE  
from "2_STANDARD_FAVRSKOV_ENERGIDATA_META" m, "3_CLEANSED_FAVRSKOV_ENERGIDATA" v 
where m.TAGID = v.TAGID; --Favrskov

create or replace table "4_FEATURIZ_ENERGIDATA" as -- Persist data in table
select distinct * from "3_CLEANSED_ENERGIDATA";

create or replace view "3_CLEANSED_ENERGIDATA_OPTIMIZED" as
with aarhus as(
select  distinct * from "3_CLEANSED_AARHUS_ENERGIDATA"
)
,syddjurs as(
select distinct dato, time, maaling, maaleenhed, enhedid, forbrugstype from "3_CLEANSED_SYDDJURS_ENERGIDATA"
)
,favrskov as(

select distinct * from "3_CLEANSED_FAVRSKOV_ENERGIDATA"
)

,El as (
select  'Aarhus' as Kommune, DATO, TIME, SUM(VALUE::float) as value, ENHED as ENHED from aarhus where measuretype = 'electricity' and key = 3261220102 group by dato, time, ENHED 

union all

select 'Syddjurs' as Kommune, dato, time, sum(maaling::float) as value, MAALEENHED as ENHED from syddjurs where enhedid in (216, 305) and forbrugstype = 'El_Samlet' group by dato, time, ENHED  
union all

select 'Favrskov' as Kommune, DATE, TIME, SUM(VALUE::float) as value, 'kWh' as ENHED from favrskov where tagid = 74 group by date, time, ENHED 
)

,Fjernvarme as (
select  'Aarhus' as Kommune, DATO, TIME, SUM(VALUE::float) as value, ENHED as ENHED from aarhus where measuretype = 'district_heating' and key = 3261220204 group by dato, time, ENHED 

union all

select 'Syddjurs' as Kommune, dato, time, sum(maaling::float) as value, MAALEENHED as ENHED from syddjurs where enhedid in (216) and forbrugstype = 'Varme_Samlet' group by dato, time, ENHED 
union all

select 'Favrskov' as Kommune, DATE, TIME, SUM(VALUE::float) as value, 'MWh' as ENHED from favrskov where tagid = 75 group by date, time, ENHED 
)

,joined as (
select 'Fjernvarme' as measure_type, * from Fjernvarme
union all
select 'El' as measure_type, * from El
)

select *, 
TIMESTAMP_FROM_PARTS(year(dato), month(dato), day(dato), hour(time),0,0) as timestamp,
concat(kommune,'-',timestamp) as kommune_dato_time
from joined;


create or replace table "4_FEATURIZ_ENERGIDATA_OPTIMIZED" as -- Persist data in table
select distinct * from "3_CLEANSED_ENERGIDATA_OPTIMIZED";

```
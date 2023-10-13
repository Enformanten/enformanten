create or replace table "1_RAW_KALENDER" (DATE date, NAVN varchar,	TYPE varchar,	WeekNo int,	Dato varchar); -- raw table containing vacations

create or replace view "2_STANDARD_TIMESTAMPS" as -- generate timestamps from the 2022 to 2023 and define the types of days and timestamps
select dateadd(hour, row_number() over (order by null), '2022-01-01 00:00') as timestamp, timestamp::date as date, timestamp::time as time, decode(DAYNAME(date), 'Mon','Mandag', 'Tue','Tirsdag', 'Wed', 'Onsdag', 'Thu', 'Torsdag', 'Fri', 'Fredag', 'Sat', 'Loerdag', 'Sun', 'Soendag') as dayname , DAYOFWEEKISO(date) as weekdaynum, weekofyear(timestamp) as weekno, iff(time >= '16:00', 'Fritid', iff(weekdaynum > 5, 'Fritid', 'Skole')) as TIDSPUNKT_TYPE from table(generator(rowcount => 17496)) g;

create or replace view "3_CLEANSED_DATOER" as -- joining timestamps with the calendar for defining information for every hour since 2022
select k1.timestamp, k1.date::date as date, k1.TIME, k1.weekno, k1.dayname, k1.weekdaynum, year(k1.date::date)::string as year, month(k1.date::date)::string as month, monthname(k1.date::date) as monthname, month(k1.date::date)::int as monthno,
iff(k1.time <= '07:00' OR k1.time >= '16:00', 'Fritid', iff(k1.weekdaynum > 5 OR k2.type in ('Helligdag', 'Skole-ferie'), 'Fritid', 'Skole')) as TIDSPUNKT_TYPE, k2.navn, k2.type,

DATEDIFF(DAY,( -- calculating the number of day in the vacation the current date is
select min(s.date) from "1_RAW_KALENDER" s
where s.type = k2.type and s.navn = k2.navn and year(s.date) = year(k2.date) 
),k1.date::date)::int as dag_i_ferien,
iff(year(k1.date::date) = year(current_date), 'TY',
iff(year(k1.date::date) = year(current_date) - 1, 'LY', '')) as last_year_or_this_year,
iff(datediff(DAY,k1.date::date, current_date) <= 365, 'TY', 
iff(datediff(DAY,k1.date::date, current_date) > 365, 'LY', '')) as in_the_last_365_days,
iff(navn = (SELECT
  MAX(NAVN) AS max_name
FROM "1_RAW_KALENDER"
WHERE "DATE" = (
  SELECT MAX("DATE")
  FROM "1_RAW_KALENDER"
  WHERE "DATE" <= CURRENT_DATE
    AND "TYPE" = 'Skole-ferie'
)), 1,0) as last_vacation,
dayofyear(k1.date::date) as day_of_year
from 
"2_STANDARD_TIMESTAMPS" k1, 
"1_RAW_KALENDER" k2
where k1.date = k2.date and k1.date <= current_date -- only show dates on or before today
order by k1.date desc;

create or replace table "4_FEATURIZ_DATOER" as -- update persisted table
select * from "3_CLEANSED_DATOER";
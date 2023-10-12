create or replace table "1_RAW_SYDDJURS_ENERGIDATA_HISTORY" (ID varchar,
EnhedID varchar,
ForbrugsmaalerID varchar,
Dato varchar,
Time varchar,
Maaling varchar
);

create or replace table "1_RAW_SYDDJURS_ENERGIDATA" (ID varchar,
Type varchar,
MaalerID varchar,
TimeStart varchar,
TimeEnd varchar,
Maaling varchar,
Enhed varchar
);

create or replace table "1_RAW_SYDDJURS_ENERGIDATA_MAALERE" (ForbrugsmaalerID varchar,
Forbrugstype varchar,
Maaleenhed varchar
);

create or replace view "2_STANDARD_SYDDJURS_ENERGIDATA_HISTORY" as
select h.ID, h.EnhedID, h.ForbrugsmaalerID, h.Dato,h.Time, h.Maaling::float/1000 as MAALING, m.forbrugstype, m.maaleenhed from "1_RAW_SYDDJURS_ENERGIDATA_HISTORY" h, "1_RAW_SYDDJURS_ENERGIDATA_MAALERE" m where h.ForbrugsmaalerID = m.ForbrugsmaalerID;

create or replace view "2_STANDARD_SYDDJURS_ENERGIDATA" as 
select h.id, left(h.type,3) as enhedid , h.maalerid::int::varchar as ForbrugsmaalerID, h.timestart::timestamp::date as dato, h.timestart::timestamp::time as time, h.Maaling::float as maaling, 
substr(h.type, 5) as forbrugstype, h.enhed as maaleenhed from "1_RAW_SYDDJURS_ENERGIDATA" h;

create or replace view "3_CLEANSED_SYDDJURS_ENERGIDATA" as
select distinct * from "2_STANDARD_SYDDJURS_ENERGIDATA_HISTORY"
union all
select distinct * from "2_STANDARD_SYDDJURS_ENERGIDATA";
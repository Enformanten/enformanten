create or replace table "1_RAW_DMI_HISTORY" (INDEX INT,STATIONID INT,PARAMETER VARCHAR,VALUE VARCHAR,TIMESTAMP VARCHAR,SKOLE VARCHAR);

create or replace table "1_RAW_DMI" (data variant);

create or replace view "2_STANDARD_DMI" as select INDEX, STATIONID, PARAMETER, VALUE, TIMESTAMP, DATE(TIMESTAMP) as DATE, concat(DATE::string,'-Aarhus'), 
CASE 
WHEN PARAMETER = 'sun_last1h_glob' THEN 'Solskinsminutter'
WHEN PARAMETER = 'temp_mean_past1h' THEN 'Temperatur'
WHEN PARAMETER = 'humidity_past1h' THEN 'Fugtighed'
END as PARAMETER_DANSK as KOMMUNE_DATO, SKOLE as KOMMUNE from "1_RAW_DMI_HISTORY";

create or replace table "2_STANDARD_DMI_META" (Stationid varchar, skole varchar);
insert into "2_STANDARD_DMI_META" values ('06072', 'Favrskov'), ('06073', 'Syddjurs'), ('06074', 'Aarhus');

create or replace view "2_STANDARD_DMI" as
select 
value:properties:stationId::varchar as STATIONID, 
value:properties:parameterId::varchar as PARAMETER, 
value:properties:value::varchar as VALUE, 
value:properties:observed::varchar as observed, 
SKOLE from "1_RAW_DMI", lateral flatten(input=>data:features), "2_STANDARD_DMI_META" m where value:properties:stationId::varchar=m.STATIONID;

create or replace view "2_STANDARD_DMI_JOINED" as 
select * from "2_STANDARD_DMI" union all select STATIONID, PARAMETER,VALUE,TIMESTAMP,SKOLE from "1_RAW_DMI_HISTORY";

create or replace view "3_CLEANSED_DMI" as
select STATIONID, 
PARAMETER, 
CASE 
WHEN PARAMETER = 'sun_last1h_glob' THEN 'Solskinsminutter'
WHEN PARAMETER = 'temp_mean_past1h' THEN 'Temperatur'
WHEN PARAMETER = 'humidity_past1h' THEN 'Fugtighed'
END as PARAMETER_DANSK,
VALUE::float as VALUE, 
round(value) as value_round,
TIMESTAMP::datetime as timestamp, 
DATE(TIMESTAMP) as DATE,
SKOLE as KOMMUNE from "2_STANDARD_DMI_JOINED";

create or replace table "4_FEATURIZ_DMI"
as select distinct * from "3_CLEANSED_DMI";
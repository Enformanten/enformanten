create or replace table "1_RAW_FAVRSKOV_ENERGIDATA_META" (Data Variant);

create or replace table "1_RAW_FAVRSKOV_ENERGIDATA_HISTORY" (Data Variant);

create or replace table "1_RAW_FAVRSKOV_ENERGIDATA" (Data Variant);

create or replace view "2_STANDARD_FAVRSKOV_ENERGIDATA_META" as
select VALUE:"TagID" as TAGID, VALUE:"Name"::string as NAME, VALUE:"ConsumptionType"::string as ConsumptionType, REPLACE(VALUE:"Unit"::string, 'm³', 'm3') as Unit from "1_RAW_FAVRSKOV_ENERGIDATA_META", lateral flatten (input=>Data);

create or replace view "2_STANDARD_FAVRSKOV_ENERGIDATA_HISTORY" as
select VALUE:"TagID" as TAGID, VALUE:"Name"::string as NAME, VALUE:"Value"::string as VALUE, VALUE:"From"::Date as Date, TIME(VALUE:"From"::Timestamp) as Time from "1_RAW_FAVRSKOV_ENERGIDATA_HISTORY", lateral flatten (input=>Data);

create or replace view "2_STANDARD_FAVRSKOV_ENERGIDATA" as
select data:"TagID" as TAGID, data:"Name"::string as NAME, data:"Value"::string as VALUE, data:"From"::Date as Date, TIME(data:"From"::Timestamp) as Time from "1_RAW_FAVRSKOV_ENERGIDATA", lateral flatten (input=>Data);

create or replace view "3_CLEANSED_FAVRSKOV_ENERGIDATA" as
select * from "2_STANDARD_FAVRSKOV_ENERGIDATA" union all select * from "2_STANDARD_FAVRSKOV_ENERGIDATA_HISTORY";
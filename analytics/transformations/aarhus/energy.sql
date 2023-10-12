create or replace table "1_RAW_AARHUS_ENERGIDATA_HISTORY" (Source_Name varchar,
key varchar,
measureType varchar,
reportType varchar,
measuringType varchar,
resolution varchar,
periodList_periodStart varchar,
periodList_periodEnd varchar,
periodList_energy_budget_value varchar,
periodList_energy_budget_unit varchar,
periodList_energy_budget_valueComplete varchar,
periodList_energy_adjustedBudget varchar,
periodList_energy_consumption_value varchar,
periodList_energy_consumption_unit varchar,
periodList_energy_consumption_valueComplete varchar,
Dato varchar,
Time varchar);

create or replace table "1_RAW_AARHUS_ENERGIDATA" (data variant);

create or replace table "1_RAW_AARHUS_ENERGIDATA_TEMPERATURES" (data variant);

create or replace view "2_STANDARD_AARHUS_ENERGIDATA_HISTORY" as
select * from "1_RAW_AARHUS_ENERGIDATA_HISTORY";

create or replace view "2_STANDARD_AARHUS_ENERGIDATA" as
with unfolded as (
select data:periodList as periodList, data as info from "1_RAW_AARHUS_ENERGIDATA", lateral flatten(input => data))
select 'adf' as Source_Name,
info:key::varchar as key,
info:measureType::varchar as measureType,
info:reportType::varchar as reportType,
info:measuringType::varchar as measuringType,
info:resolution::varchar as resolution,
value:periodStart::datetime::varchar as periodStart,
value:periodEnd::datetime::varchar as periodEnd,
value:energy:budget:value::varchar as periodList_energy_budget_value,
value:energy:budget:unit::varchar as periodList_energy_budget_unit,
value:energy:budget:valueComplete::varchar as periodList_energy_budget_valueComplete,
value:energy:adjustedBudget::varchar as periodList_energy_adjustedBudget,
value:energy:consumption:value::varchar as periodList_energy_consumption_value,
value:energy:consumption:unit::varchar as periodList_energy_consumption_unit,
value:energy:consumption:valueComplete::varchar as periodList_energy_consumption_valueComplete,
value:energy:cooling:value as cooling,
periodStart::date::varchar as dato,
periodStart::datetime::time::varchar as time
from unfolded, lateral flatten (input=>periodList);

create or replace view "2_STANDARD_AARHUS_ENERGIDATA_TEMPERATURES" as
with unfolded as (
select data:periodList as periodList, data as info from "1_RAW_AARHUS_ENERGIDATA_TEMPERATURES", lateral flatten(input => data))
select distinct 'adf' as Source_Name,
info:installationNumber::varchar as key,
info:measureType::varchar as measureType,
info:reportType::varchar as reportType,
info:measuringType::varchar as measuringType,
info:resolution::varchar as resolution,
value:periodStart::datetime::varchar as periodStart,
value:periodEnd::datetime::varchar as periodEnd,
iff(array_size(value:values) > 5, value:values[5]:value::varchar, value:values[3]:value::varchar) as fremfoert_energi,
iff(array_size(value:values) > 5, value:values[6]:value::varchar, value:values[4]:value::varchar) as returneret_energi,
value:values[1]:value::varchar as volumen,
iff(volumen > 0, fremfoert_energi / volumen, null) as fremloebstemp,
iff(volumen > 0, returneret_energi / volumen, null) as returtemp,
periodStart::date::varchar as dato,
periodStart::datetime::time::varchar as time
from unfolded, lateral flatten (input=>periodList);


create or replace view "3_CLEANSED_AARHUS_ENERGIDATA" as
select distinct KEY, DATO, 'Returtemp' as measuretype, returtemp::string as VALUE, 'C' as ENHED, TIME as TIME from "2_STANDARD_AARHUS_ENERGIDATA_TEMPERATURES"
union all
select distinct KEY, DATO, 'cooling' as measuretype, cooling::string as VALUE, 'C' as ENHED, TIME as TIME from "2_STANDARD_AARHUS_ENERGIDATA"  where cooling is not null
union all
select distinct KEY, DATO, measuretype, PERIODLIST_ENERGY_CONSUMPTION_VALUE::string as VALUE, PERIODLIST_ENERGY_CONSUMPTION_UNIT as ENHED, TIME as TIME from "2_STANDARD_AARHUS_ENERGIDATA";
``` sql
create or replace view "3_CLEANSED_LOKALER" as -- Unifying datatypes and names from the municipalities to a singular table of rooms and metadata
select RUM_ID as ID, AREAL as AREAL, REPLACE(AREAL, ',', '.') as AREAL_FORMAT, RUMFUNKTION as type_rum, BYGNINGS_ID as FLOJ, 'Aarhus' as KOMMUNE, 'Strandskolen' as SKOLE,  concat(kommune, '-', id) as kommune_lokale from "2_STANDARD_AARHUS_LOKALE_STAMDATA_AREAL"
union all 
select LOKALENR as ID, AREAL as AREAL,  REPLACE(AREAL, ',', '.') as AREAL_FORMAT, TYPE as type_rum, FLOJ as FLOJ, 'Favrskov' as KOMMUNE, 'Rønbækskolen' as SKOLE, concat(kommune, '-', id)  from "2_STANDARD_FAVRSKOV_LOKALE_STAMDATA_AREAL"
union all
select RIGHT(LOKALENUMMER, length(LOKALENUMMER) - 4) as ID, NETTOAREAL as AREAL,  REPLACE(AREAL, ',', '.') as AREAL_FORMAT, LOKALEANVENDELSE as type_rum, LEFT(ID, 2) as FLOJ, 'Syddjurs' as KOMMUNE, 'Thorsager Skole' as SKOLE, concat(kommune, '-', id)  from "2_STANDARD_SYDDJURS_LOKALE_STAMDATA_AREAL";

create or replace table "4_FEATURIZ_LOKALER" as -- update the persisted table with all rooms for BI
select distinct * from "3_CLEANSED_LOKALER";
```
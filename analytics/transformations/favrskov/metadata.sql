create or replace table "1_RAW_FAVRSKOV_LOKALE_STAMDATA_AREAL" (Lokalenr varchar,
Floj varchar,
Overskrift varchar,
Type varchar,
Note varchar,
Areal varchar);

create or replace view "2_STANDARD_FAVRSKOV_LOKALE_STAMDATA_AREAL" as -- joining the rooms with their area
select * from "1_RAW_FAVRSKOV_LOKALE_STAMDATA_AREAL";

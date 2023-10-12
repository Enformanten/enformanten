create or replace table "1_RAW_AARHUS_BOOKINGS_HISTORY" ( -- Raw table for .csv-file with bookings
Dato varchar,
Ugedag varchar,
Start_tid varchar,
Slut_tid varchar,
Timer varchar,
Emne varchar,
Ressource varchar,
Foreningsnavn varchar,
Lokation varchar);

create or replace view "2_STANDARD_AARHUS_BOOKINGS_HISTORY" as -- Datatype conversions for standard
select DATO, UGEDAG, TO_TIME(START_TID) as START_TID, TO_TIME(SLUT_TID) as SLUT_TID, Emne, RESSOURCE, FORENINGSNAVN, LOKATION from "1_RAW_AARHUS_BOOKINGS_HISTORY";


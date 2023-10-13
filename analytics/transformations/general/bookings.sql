create or replace view "3_CLEANSED_BOOKINGS" as -- Joining the 3 municipalities booking-data in a unified format
select b.RUM_ID as  ID, 
DATO::string as DATO, 
START_TID as START_TID, 
SLUT_TID as SLUT_TID, 
to_char(timestampdiff(MINUTE, START_TID, SLUT_TID)/60) as TIMER, 
REPLACE(TIMER, ',', '.') as TIMER_FORMAT, 
EMNE as TYPE, 
FORENINGSNAVN as LEJER, 
concat(dato::string,'-Aarhus') as KOMMUNE_DATO, 
concat(dato::string,'-', ID, '-Aarhus') as KOMMUNE_DATO_LOKALE, 
'Aarhus' as KOMMUNE, 
'Strandskolen' as SKOLE 
from "2_STANDARD_AARHUS_BOOKINGS_HISTORY", "1_RAW_AARHUS_LOKALE_STAMDATA_BOOKBAR" b 
where RESSOURCE = RUM_NAVN -- Aarhus

union all 

select SUBSTR(LOKALE, 5, 4) as ID, 
DATE(DATO)::string as DATO, 
FRAKL as START_TID, 
TILKL as SLUT_TID, 
to_char(timestampdiff(MINUTE, START_TID, SLUT_TID)/60) as TIMER, 
REPLACE(TIMER, ',', '.') as TIMER_FORMAT, 
BOOKINGTYPE as TYPE, 
LEJER as LEJER,
concat(right(dato::string,5),'-', left(dato::string,4), '-Favrskov') as KOMMUNE_DATO, 
concat(right(dato::string,2),'-', substr(dato::string,6,2),'-',left(dato::string,4),'-', ID, '-Favrskov') as KOMMUNE_DATO_LOKALE, 
'Favrskov' as KOMMUNE, 
'Rønbækskolen' as SKOLE  
from "3_CLEANSED_FAVRSKOV_BOOKINGS" --Favrskov

union all

select RIGHT(LOKALENUMMER, length(LOKALENUMMER) - 4) as ID, 
DATE(BOOKING_START)::string as DATO, 
BOOKING_START as START_TID, 
BOOKING_END as SLUT_TID, 
to_char(timestampdiff(MINUTE, START_TID, SLUT_TID)/60) as TIMER, 
REPLACE(TIMER, ',', '.') as TIMER_FORMAT, 
BOOKING_TYPE as TYPE, 
ORGANIZATION_NAME as LEJER,
concat(right(dato::string,5),'-', left(dato::string,4), '-Syddjurs') as KOMMUNE_DATO, 
concat(right(dato::string,2),'-', substr(dato::string,6,2),'-',left(dato::string,4),'-', ID, '-Syddjurs') as KOMMUNE_DATO_LOKALE,
'Syddjurs' as KOMMUNE, 
'Thorsager Skole' as SKOLE  
from "3_CLEANSED_SYDDJURS_BOOKINGS",  "2_STANDARD_SYDDJURS_LOKALE_STAMDATA_AREAL" where RESOURCE_ID::string = CONVENTUSRESSOURCEID; --Syddjurs 

create or replace table "4_FEATURIZ_BOOKINGS" as -- Persisting of data in a table
select distinct * from "3_CLEANSED_BOOKINGS";

create or replace view "3_CLEANSED_BOOKINGS_TIME" as -- Bookings on an hourly-flattened level
SELECT 
    d.date as dato,
    d.TIME,
    concat(d.date::date, ' ', d.time)::datetime as timestamp,
    r.KOMMUNE,
    r.ID,
    concat(r.kommune, '-', r.id) as kommune_lokale,
    CONCAT(d.date::STRING, '-', d.TIME, '-', r.KOMMUNE) AS KOMMUNE_DATO_TIME,
    IFF(d.time >= b.start_tid, IFF(d.time <= b.slut_tid, 1, 0), 0) AS booket,
    IFF(booket = 1, start_tid, NULL) AS starttid,
    IFF(booket = 1, slut_tid, NULL) AS sluttid,
    IFF(booket = 1, lejer, NULL) AS lejerid,
    IFF(booket = 1, b.type, NULL) AS typebooking,
    CAST(IFF(booket = 1, timer_format, NULL) AS FLOAT) AS booket_tid
FROM
    "4_FEATURIZ_DATOER" d
    CROSS JOIN "4_FEATURIZ_LOKALER" r
    LEFT JOIN "4_FEATURIZ_BOOKINGS" b ON d.date::date = iff(b.kommune = 'Aarhus', try_to_date(b.dato, 'dd-mm-yyyy'), try_to_date(b.dato, 'yyyy-mm-dd')) and r.id = b.id and r.kommune = b.kommune
WHERE
    booket = 1
GROUP BY
    d.date,
    TIME,
    slut_tid,
    start_tid,
    timer_format,
    r.KOMMUNE,
    r.ID,
    lejer,
    b.type
ORDER BY
    date::date,
    time,
    kommune, 
    id;
    
create or replace table "4_FEATURIZ_BOOKINGS_TIME" -- Persisting of data in a table
as select * from "3_CLEANSED_BOOKINGS_TIME";
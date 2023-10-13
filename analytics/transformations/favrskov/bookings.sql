create or replace table "1_RAW_FAVRSKOV_BOOKINGS" (data variant);

create or replace view "2_STANDARD_FAVRSKOV_BOOKINGS_HISTORY" as -- Flatten the json-files from the historical bookings into a table
select 
value:dato as dato,
TO_TIME(REPLACE(value:frakl::string ,'24:00', '23:59')) as frakl,
TO_TIME(REPLACE(value:tilkl::string ,'24:00', '23:59')) as tilkl,
value:lokale::string as lokale,
value:lokalenr::string as lokalenr,
value:overskrift::string as overskrift,
value:beskrivelse::string as beskrivelse,
value:lejer::string as lejer,
value:gruppe::string as gruppe,
value:bookingid::int as bookingid,
value:bookingtype::string as bookingtype
from "1_RAW_FAVRSKOV_BOOKINGS_HISTORY", lateral flatten(INPUT => DATA);

create or replace view "2_STANDARD_FAVRSKOV_BOOKINGS" as -- Flatten the json-files from bookings API into a table
select 
data:dato as dato,
TO_TIME(REPLACE(data:frakl::string ,'24:00', '23:59')) as frakl,
TO_TIME(REPLACE(data:tilkl::string ,'24:00', '23:59')) as tilkl,
data:lokale::string as lokale,
data:lokalenr::string as lokalenr,
data:overskrift::string as overskrift,
data:beskrivelse::string as beskrivelse,
data:lejer::string as lejer,
data:gruppe::string as gruppe,
data:bookingid::int as bookingid,
data:bookingtype::string as bookingtype
from "1_RAW_FAVRSKOV_BOOKINGS", lateral flatten(INPUT => DATA);

create or replace view "3_CLEANSED_FAVRSKOV_BOOKINGS" as -- Merge the historical and current bookings
select * from "2_STANDARD_FAVRSKOV_BOOKINGS_HISTORY" union all select * from "2_STANDARD_FAVRSKOV_BOOKINGS";
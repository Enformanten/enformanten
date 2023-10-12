# Bookings

```sql
create or replace table "1_RAW_SYDDJURS_BOOKINGS_HISTORY" (data variant);

create or replace table "1_RAW_SYDDJURS_BOOKINGS" (data variant);

create or replace view "2_STANDARD_SYDDJURS_BOOKINGS_HISTORY" as -- Flatten the json-files from the historical bookings into a table
select 
to_timestamp(value:start::int, 3) as booking_start,
to_timestamp(value:end::int, 3) as booking_end,
value:bookingType::string as booking_type,
value:category:name::string as category_name,
value:category:id::int as category_id,
value:organization:id::int as organization_id,
value:organization:name::string as organization_name,
value:resource:id::int as resource_id,
value:resource:name::string as resource_name,
value:resource:organization:id::int as resource_organization_id,
value:resource:organization:name::string as resource_organization_name
from "1_RAW_SYDDJURS_BOOKINGS_HISTORY", lateral flatten(INPUT => DATA);

create or replace view "2_STANDARD_SYDDJURS_BOOKINGS" as -- Flatten the json-files from bookings API into a table
select 
to_timestamp(data:start::int, 3) as booking_start,
to_timestamp(data:end::int, 3) as booking_end,
data:bookingType::string as booking_type,
data:category:name::string as category_name,
data:category:id::int as category_id,
data:organization:id::int as organization_id,
data:organization:name::string as organization_name,
data:resource:id::int as resource_id,
data:resource:name::string as resource_name,
data:resource:organization:id::int as resource_organization_id,
data:resource:organization:name::string as resource_organization_name
from "1_RAW_SYDDJURS_BOOKINGS", lateral flatten(INPUT => DATA);

create or replace view "3_CLEANSED_SYDDJURS_BOOKINGS" as -- Merge the historical and current bookings
select * from "2_STANDARD_SYDDJURS_BOOKINGS_HISTORY" union all select * from "2_STANDARD_SYDDJURS_BOOKINGS";
```
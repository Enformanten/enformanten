CREATE or replace STORAGE INTEGRATION govtech_storage_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = AZURE
AZURE_TENANT_ID = '9c0c1cb6-e571-4e1d-a416-5b2b2bc8def6'
ENABLED = TRUE
STORAGE_ALLOWED_LOCATIONS = ('azure://stgovtech.blob.core.windows.net/bookings', 'azure://stgovtech.blob.core.windows.net/dmi', 'azure://stgovtech.blob.core.windows.net/zurface-data',
'azure://stgovtech.blob.core.windows.net/energi-data', 'azure://stgovtech.blob.core.windows.net/iot-data');

create or replace stage BOOKINGS_STAGE
storage_integration = govtech_storage_integration
url = 'azure://stgovtech.blob.core.windows.net/bookings'
FILE_FORMAT = (TYPE = JSON);

create or replace stage ENERGIDATA_STAGE
storage_integration = govtech_storage_integration
url = 'azure://stgovtech.blob.core.windows.net/energi-data'
FILE_FORMAT = (TYPE = JSON);

create or replace stage DMI_STAGE
storage_integration = govtech_storage_integration
url = 'azure://stgovtech.blob.core.windows.net/dmi'
FILE_FORMAT = (TYPE = JSON);

create or replace stage IOT_STAGE
storage_integration = govtech_storage_integration
url = 'azure://stgovtech.blob.core.windows.net/iot-data'
FILE_FORMAT = (TYPE = JSON);

create or replace stage ZURFACE_HISTORY_STAGE
storage_integration = govtech_storage_integration
url = 'azure://stgovtech.blob.core.windows.net/zurface-data/history'
FILE_FORMAT = CSV_FORMAT;

create or replace stage ZURFACE_STAGE
storage_integration = govtech_storage_integration
url = 'azure://stgovtech.blob.core.windows.net/zurface-data'
FILE_FORMAT = (TYPE=JSON);
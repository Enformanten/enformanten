create or replace table "1_RAW_SYDDJURS_LOKALE_STAMDATA_AREAL" (LokaleID varchar,
Lokalenummer varchar,
Enhed varchar,
Bygning varchar,
Lokale varchar,
Adresse varchar,
Postnummer varchar,
Postdistrikt varchar,
Nettoareal varchar,
Lokaleanvendelse varchar,
Energimaerke varchar,
EnergimaerkeAar varchar,
EnergimaerkeUdloebAar varchar,
BygningBookbar varchar,
LokaleBookbar varchar,
Opvarmet varchar,
Ejerforhold varchar,
GyldigFra varchar,
GyldigTil varchar,
ConventusRessourceID varchar,
CaretakerID varchar);

create or replace table "1_RAW_SYDDJURS_BYGNING_STAMDATA" (EnhedID varchar,
Enhedskode varchar,
Enhed varchar,
BDA_Areal varchar,
OmraadeKode varchar,
Omraade varchar);

create or replace view "2_STANDARD_SYDDJURS_LOKALE_STAMDATA_AREAL" as -- Joining the rooms with the area of the rooms from the other table
select l.*, b.enhedskode, b.enhedid from "1_RAW_SYDDJURS_LOKALE_STAMDATA_AREAL" l, 
"1_RAW_SYDDJURS_BYGNING_STAMDATA" b where l.enhed = b.enhed;
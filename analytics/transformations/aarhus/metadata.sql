create or replace table "1_RAW_AARHUS_LOKALE_STAMDATA_BOOKBAR" (Rum_Navn varchar,
Rum_ID varchar);

create or replace table "1_RAW_AARHUS_LOKALE_STAMDATA" (AEC_ObjectId varchar,
Bygnings_ID varchar,
Bygnings_ID_formatted varchar,
Etage_ID varchar,
Etage_ID_formatted varchar,
Gl_Rumnr varchar,
Gl_Rumnr_formatted varchar,
Rum_ID varchar,
Rum_ID_formattet varchar,
Rumnr varchar,
Rumnr_formatted varchar);

create or replace table "1_RAW_AARHUS_LOKALE_STAMDATA_AREAL" (AEC_ObjectId varchar ,
Areal varchar ,
Areal_formatted varchar ,
Bredde varchar ,Bredde_formatted varchar ,
Bygnings_ID varchar ,
Bygnings_ID_formatted varchar ,
Etage_ID varchar ,
Etage_ID_formatted varchar ,
Laengde varchar ,
Laengde_formatted varchar ,
Omkreds varchar ,
Omkreds_formatted varchar ,
Rumfunktion varchar ,
Rumfunktion_formatted varchar ,
Rumhojde varchar ,
Rumhojde_formatted varchar ,
Rumkode varchar ,Rumkode_formatted varchar ,
Skole_ID varchar ,
Skole_ID_formatted varchar ,
Skole_Navn varchar ,
Skole_Navn_formatted varchar ,
Vaegareal varchar ,
Vaegareal_formatted varchar);

create or replace view "2_STANDARD_AARHUS_LOKALE_STAMDATA_AREAL" as -- joining the rooms with their area
select ss.Rum_ID, aa.* from "1_RAW_AARHUS_LOKALE_STAMDATA" ss, "1_RAW_AARHUS_LOKALE_STAMDATA_AREAL" aa where ss.AEC_ObjectId = aa.AEC_ObjectId;
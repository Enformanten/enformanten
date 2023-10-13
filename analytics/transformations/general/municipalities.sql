create or replace table "1_RAW_KOMMUNER_SKOLER" 
(Kommune varchar,
Skole varchar, 
Driftsareal float);

insert into "1_RAW_KOMMUNER_SKOLER" values ('Syddjurs', 'Thorsager Skole', 4740);
insert into "1_RAW_KOMMUNER_SKOLER" values ('Aarhus', 'Strandskolen', 9093);
insert into "1_RAW_KOMMUNER_SKOLER" values ('Favrskov', 'Rønbækskolen', 9039);
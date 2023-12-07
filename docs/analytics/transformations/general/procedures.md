``` sql
create or replace PROCEDURE RAWLOADDATA("TGTDB" VARCHAR(16777216), "TGTSCHEMA" VARCHAR(16777216), "TGTTABLE" VARCHAR(16777216),"KOMMUNE" VARCHAR(16777216), "STAGE" VARCHAR(16777216))
RETURNS VARCHAR(16777216)
LANGUAGE JAVASCRIPT
EXECUTE AS OWNER
AS '  
        var insert_sql_command = `COPY INTO "${TGTDB}"."${TGTSCHEMA}"."${TGTTABLE}"                                 
                                  FROM @"${STAGE}"/${KOMMUNE}`;
                                  
         var statement = snowflake.createStatement({sqlText: insert_sql_command});
         
         statement.execute();
         
         return statement.getRowCount();
  ';
  

create or replace PROCEDURE UPDATEFEATURIZ("TGTDB" VARCHAR(16777216), "TGTSCHEMA" VARCHAR(16777216), "TGTTABLE" VARCHAR(16777216),"CLEANSEDTABLE" VARCHAR(16777216))
RETURNS VARCHAR(16777216)
LANGUAGE JAVASCRIPT
EXECUTE AS OWNER
AS '  
        var insert_sql_command = `CREATE OR REPLACE TABLE "${TGTDB}"."${TGTSCHEMA}"."${TGTTABLE}"                                 
                                  AS SELECT * FROM "${TGTDB}"."${TGTSCHEMA}"."${CLEANSEDTABLE}"`;
                                  
         var statement = snowflake.createStatement({sqlText: insert_sql_command});
         
         statement.execute();
         
         return statement.getRowCount();
  ';


create or replace PROCEDURE UPDATEFEATURIZDISTINCT("TGTDB" VARCHAR(16777216), "TGTSCHEMA" VARCHAR(16777216), "TGTTABLE" VARCHAR(16777216),"CLEANSEDTABLE" VARCHAR(16777216))
RETURNS VARCHAR(16777216)
LANGUAGE JAVASCRIPT
EXECUTE AS OWNER
AS '  
        var insert_sql_command = `CREATE OR REPLACE TABLE "${TGTDB}"."${TGTSCHEMA}"."${TGTTABLE}"                                 
                                  AS SELECT DISTINCT * FROM "${TGTDB}"."${TGTSCHEMA}"."${CLEANSEDTABLE}"`;
                                  
         var statement = snowflake.createStatement({sqlText: insert_sql_command});
         
         statement.execute();
         
         return statement.getRowCount();
  ';
  ```
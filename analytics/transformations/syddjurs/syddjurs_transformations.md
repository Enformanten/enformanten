# Sample of outputs

## Metadata

| LOKALEID | LOKALENUMMER | ENHED                 | BYGNING                                  | LOKALE              | ADRESSE      | POSTNUMMER | POSTDISTRIKT | NETTOAREAL | LOKALEANVENDELSE | ENERGIMAERKE | ENERGIMAERKEAAR | ENERGIMAERKEUDLOEBAAR | BYGNINGBOOKBAR | LOKALEBOOKBAR | OPVARMET   | EJERFORHOLD | GYLDIGFRA | GYLDIGTIL | CONVENTUSRESSOURCEID | CARETAKERID | ENHEDSKODE | ENHEDID |
| -------- | ------------ | --------------------- | ---------------------------------------- | ------------------- | ------------ | ---------- | ------------ | ---------- | ---------------- | ------------ | --------------- | --------------------- | -------------- | ------------- | ---------- | ----------- | --------- | --------- | -------------------- | ----------- | ---------- | ------- |
| 3622     | 305.3.0.001  | Sportshal i Thorsager | Sportshal med klub og Servicesmedarbejer | 305.3.0.001 (Entré) | Kløvervangen | 8410       | Rønde        | 5.6        | Entré            | NULL         | NULL            | NULL                  | Bookbar        | Ej bookbar    | Ingen data | Ejer        | NULL      | NULL      | NULL                 | 2001        | 305        | 53      |
| 3623     | 305.3.0.002  | Sportshal i Thorsager | Sportshal med klub og Servicesmedarbejer | 305.3.0.002 (Gang)  | Kløvervangen | 8410       | Rønde        | 35.77      | Gang             | NULL         | NULL            | NULL                  | Bookbar        | Ej bookbar    | Ingen data | Ejer        | NULL      | NULL      | NULL                 | 2000        | 305        | 53      |

## Bookings

| BOOKING_START           | BOOKING_END             | BOOKING_TYPE | CATEGORY_NAME | CATEGORY_ID | ORGANIZATION_ID | ORGANIZATION_NAME              | RESOURCE_ID | RESOURCE_NAME | RESOURCE_ORGANIZATION_ID | RESOURCE_ORGANIZATION_NAME |
| ----------------------- | ----------------------- | ------------ | ------------- | ----------- | --------------- | ------------------------------ | ----------- | ------------- | ------------------------ | -------------------------- |
| 2022-01-01 09:00:00.000 | 2022-01-01 11:00:00.000 | ordinary     | Skumtennis    | 26907       | 5104            | Thorsager-Rønde Idrætsforening | 10339       | Hallen        | 5125                     | Thorsager Skole            |
| 2022-01-02 08:00:00.000 | 2022-01-02 14:00:00.000 | ordinary     | Andet         | 9294        | 6133            | Cykel Klubben Djurs            | 39100       | multirum      | 5125                     | Thorsager Skole            |

## Energy

| ID  | ENHEDID | FORBRUGSMAALERID | DATO       | TIME     | MAALING | FORBRUGSTYPE | MAALEENHED |
| --- | ------- | ---------------- | ---------- | -------- | ------- | ------------ | ---------- |
| 152 | 45      | 3                | 2022-04-01 | 02:00:00 | 0       | Vand_Samlet  | m3         |
| 176 | 45      | 3                | 2022-04-02 | 02:00:00 | 0       | Vand_Samlet  | m3         |

## IoT

| LOKALEID | SENSORNAVN                   | DATE       | TIME     | FORBRUGSTYPE | VALUE        | ENDING_NAVN |
| -------- | ---------------------------- | ---------- | -------- | ------------ | ------------ | ----------- |
| 3571     | a81758fffe06b5fa_Temperature | 2022-05-15 | 00:00:00 | Temperature  | 20.033333333 | Temperature |
| 3574     | a81758fffe06b5fe_Temperature | 2022-05-15 | 00:00:00 | Temperature  | 19.366666667 | Temperature |
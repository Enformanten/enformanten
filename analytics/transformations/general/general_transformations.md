# Base table Schemas 

The below schemas are for tables that have been used both directly in the visual insights and analytics but also in transformations into derived tables. These tables could be the direct input for how the future dataformats might be.

## Municipalities

| Table              | Column |
| --------------------- | ----------- |
| 1_RAW_KOMMUNER_SKOLER  | KOMMUNE     |
| 1_RAW_KOMMUNER_SKOLER  | SKOLE       |
| 1_RAW_KOMMUNER_SKOLER  | DRIFTSAREAL |

## Rooms

| Table                   | Column         |
| ------------------      | -------------- |
| 4_FEATURIZ_LOKALER      | ID             |
| 4_FEATURIZ_LOKALER      | AREAL          |
| 4_FEATURIZ_LOKALER      | AREAL_FORMAT   |
| 4_FEATURIZ_LOKALER      | TYPE_RUM       |
| 4_FEATURIZ_LOKALER      | FLOJ           |
| 4_FEATURIZ_LOKALER      | KOMMUNE        |
| 4_FEATURIZ_LOKALER      | SKOLE          |
| 4_FEATURIZ_LOKALER      | KOMMUNE_LOKALE |

## Bookings

| Table          | Column         |
| ------------------- | ------------------- |
| 4_FEATURIZ_BOOKINGS | ID                  |
| 4_FEATURIZ_BOOKINGS | DATO                |
| 4_FEATURIZ_BOOKINGS | START_TID           |
| 4_FEATURIZ_BOOKINGS | SLUT_TID            |
| 4_FEATURIZ_BOOKINGS | TIMER               |
| 4_FEATURIZ_BOOKINGS | TIMER_FORMAT        |
| 4_FEATURIZ_BOOKINGS | TYPE                |
| 4_FEATURIZ_BOOKINGS | LEJER               |
| 4_FEATURIZ_BOOKINGS | KOMMUNE_DATO        |
| 4_FEATURIZ_BOOKINGS | KOMMUNE_DATO_LOKALE |
| 4_FEATURIZ_BOOKINGS | KOMMUNE             |
| 4_FEATURIZ_BOOKINGS | SKOLE               |


## Energy

| Table            | Column       |
| --------------------- | ----------------- |
| 4_FEATURIZ_ENERGIDATA | MAALER_ID         |
| 4_FEATURIZ_ENERGIDATA | DATO              |
| 4_FEATURIZ_ENERGIDATA | MEASURE_TYPE      |
| 4_FEATURIZ_ENERGIDATA | VALUE             |
| 4_FEATURIZ_ENERGIDATA | ENHED             |
| 4_FEATURIZ_ENERGIDATA | TIME              |
| 4_FEATURIZ_ENERGIDATA | TIMESTAMP         |
| 4_FEATURIZ_ENERGIDATA | KOMMUNE_DATO      |
| 4_FEATURIZ_ENERGIDATA | KOMMUNE_DATO_TIME |
| 4_FEATURIZ_ENERGIDATA | KOMMUNE           |
| 4_FEATURIZ_ENERGIDATA | SKOLE             |


## IoT & CTS

| Table                | Column         |
| -------------------- | -------------- |
| 4_FEATURIZ_CTS_X_IOT | DATE           |
| 4_FEATURIZ_CTS_X_IOT | TIME           |
| 4_FEATURIZ_CTS_X_IOT | TIMESTAMP      |
| 4_FEATURIZ_CTS_X_IOT | TIME_GROUP     |
| 4_FEATURIZ_CTS_X_IOT | CO2            |
| 4_FEATURIZ_CTS_X_IOT | SOUND          |
| 4_FEATURIZ_CTS_X_IOT | LIGHT          |
| 4_FEATURIZ_CTS_X_IOT | IAQ            |
| 4_FEATURIZ_CTS_X_IOT | TEMPERATURE    |
| 4_FEATURIZ_CTS_X_IOT | HUMIDITY       |
| 4_FEATURIZ_CTS_X_IOT | MOTION         |
| 4_FEATURIZ_CTS_X_IOT | ID             |
| 4_FEATURIZ_CTS_X_IOT | KOMMUNE        |
| 4_FEATURIZ_CTS_X_IOT | SKOLE          |
| 4_FEATURIZ_CTS_X_IOT | KOMMUNE_LOKALE |

## Ideal Curve

| Table                 | Column            |
| --------------------- | ----------------- |
| 4_FEATURIZ_IDEALKURVE | GRADER            |
| 4_FEATURIZ_IDEALKURVE | HAELDNING_BYGNING |
| 4_FEATURIZ_IDEALKURVE | SKAERING_BYGNING  |
| 4_FEATURIZ_IDEALKURVE | IDEALKURVE        |
| 4_FEATURIZ_IDEALKURVE | KOMMUNE           |

## Manuel benchmark values (Vacation Closing)

| Table                          | Column       |
| ----------------------------------- | ----------------- |
| 4_FEATURIZ_BENCHMARK_WEEKEND_MANUEL | KOMMUNE           |
| 4_FEATURIZ_BENCHMARK_WEEKEND_MANUEL | BENCHMARK_WEEKEND |

# Derived / Featurized tables

These schemas for tables are the ones that have been created by using base tables and raw data. They are the ones used mainly for specific analytics and insights

## Dates

| Table        | Column            |
| ----------------- | ---------------------- |
| 4_FEATURIZ_DATOER | TIMESTAMP              |
| 4_FEATURIZ_DATOER | DATE                   |
| 4_FEATURIZ_DATOER | TIME                   |
| 4_FEATURIZ_DATOER | WEEKNO                 |
| 4_FEATURIZ_DATOER | DAYNAME                |
| 4_FEATURIZ_DATOER | WEEKDAYNUM             |
| 4_FEATURIZ_DATOER | YEAR                   |
| 4_FEATURIZ_DATOER | MONTH                  |
| 4_FEATURIZ_DATOER | MONTHNAME              |
| 4_FEATURIZ_DATOER | MONTHNO                |
| 4_FEATURIZ_DATOER | TIDSPUNKT_TYPE         |
| 4_FEATURIZ_DATOER | NAVN                   |
| 4_FEATURIZ_DATOER | TYPE                   |
| 4_FEATURIZ_DATOER | DAG_I_FERIEN           |
| 4_FEATURIZ_DATOER | LAST_YEAR_OR_THIS_YEAR |
| 4_FEATURIZ_DATOER | IN_THE_LAST_365_DAYS   |
| 4_FEATURIZ_DATOER | LAST_VACATION          |
| 4_FEATURIZ_DATOER | DAY_OF_YEAR            |

## Bookings

| Table               | Column       |
| ------------------------ | ----------------- |
| 4_FEATURIZ_BOOKINGS_TIME | DATO              |
| 4_FEATURIZ_BOOKINGS_TIME | TIME              |
| 4_FEATURIZ_BOOKINGS_TIME | TIMESTAMP         |
| 4_FEATURIZ_BOOKINGS_TIME | KOMMUNE           |
| 4_FEATURIZ_BOOKINGS_TIME | ID                |
| 4_FEATURIZ_BOOKINGS_TIME | KOMMUNE_LOKALE    |
| 4_FEATURIZ_BOOKINGS_TIME | KOMMUNE_DATO_TIME |
| 4_FEATURIZ_BOOKINGS_TIME | BOOKET            |
| 4_FEATURIZ_BOOKINGS_TIME | STARTTID          |
| 4_FEATURIZ_BOOKINGS_TIME | SLUTTID           |
| 4_FEATURIZ_BOOKINGS_TIME | LEJERID           |
| 4_FEATURIZ_BOOKINGS_TIME | TYPEBOOKING       |
| 4_FEATURIZ_BOOKINGS_TIME | BOOKET_TID        |

## Energy

| Table                           | Column            |
| ------------------------------- | ----------------- |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | MEASURE_TYPE      |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | KOMMUNE           |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | DATO              |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | TIME              |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | VALUE             |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | ENHED             |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | TIMESTAMP         |
| 4_FEATURIZ_ENERGIDATA_OPTIMIZED | KOMMUNE_DATO_TIME |

## Weather

| Table          | Column          |
| -------------- | --------------- |
| 4_FEATURIZ_DMI | STATIONID       |
| 4_FEATURIZ_DMI | PARAMETER       |
| 4_FEATURIZ_DMI | PARAMETER_DANSK |
| 4_FEATURIZ_DMI | VALUE           |
| 4_FEATURIZ_DMI | VALUE_ROUND     |
| 4_FEATURIZ_DMI | TIMESTAMP       |
| 4_FEATURIZ_DMI | DATE            |
| 4_FEATURIZ_DMI | KOMMUNE         |

## Driftoptimeringsmodel

| Table                            | Column         |
| -------------------------------- | -------------- |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | DATE           |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | TIME           |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | DATETIME       |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | ID             |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | KOMMUNE        |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | BRUGTE_KVARTER |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | IN_USE         |
| 4_FEATURIZ_DRIFTOPTIMERINGSMODEL | KOMMUNE_LOKALE |

| Table                               | Column         |
| ----------------------------------- | -------------- |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | ID             |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | KOMMUNE        |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | SKOLE          |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | DATE           |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | TIME           |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | DAYNAME        |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | TIDSPUNKT_TYPE |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | TYPE           |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | NAVN           |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | CO2            |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | TEMP           |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | MOTION         |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | IAQ            |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | BOOKET         |
| 4_FEATURIZ_DRIFTOPTIMERING_TRAINING | SKEMALAGT      |

| Table                              | Column         |
| ---------------------------------- | -------------- |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | ID             |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | KOMMUNE        |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | SKOLE          |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | DATE           |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | TIME           |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | DAYNAME        |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | TIDSPUNKT_TYPE |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | TYPE           |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | NAVN           |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | CO2            |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | TEMP           |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | MOTION         |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | IAQ            |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | BOOKET         |
| 4_FEATURIZ_DRIFTOPTIMERING_PREDICT | SKEMALAGT      |

## Passive Hours

| Table                  | Column            |
| ---------------------- | ----------------- |
| 4_FEATURIZ_PASSIVTIMER | TIMESTAMP         |
| 4_FEATURIZ_PASSIVTIMER | DATE              |
| 4_FEATURIZ_PASSIVTIMER | TIME              |
| 4_FEATURIZ_PASSIVTIMER | YEAR              |
| 4_FEATURIZ_PASSIVTIMER | MONTH             |
| 4_FEATURIZ_PASSIVTIMER | MONTHNAME         |
| 4_FEATURIZ_PASSIVTIMER | MONTHNO           |
| 4_FEATURIZ_PASSIVTIMER | KOMMUNE           |
| 4_FEATURIZ_PASSIVTIMER | PASSIVTIME        |
| 4_FEATURIZ_PASSIVTIMER | KOMMUNE_DATO_TIME |

| Table                 | Column         |
| --------------------- | -------------- |
| 4_FEATURIZ_MINIMUM_EL | KOMMUNE        |
| 4_FEATURIZ_MINIMUM_EL | MINIMUM_EL     |
| 4_FEATURIZ_MINIMUM_EL | MANUEL_MINIMUM |



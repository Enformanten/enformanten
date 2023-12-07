``` sql
create or replace table "4_FEATURIZ_IDEALKURVE" as
WITH RECURSIVE number_range AS (
  SELECT -20 AS value
  UNION ALL
  SELECT value + 0.01
  FROM number_range
  WHERE value < 40
)
SELECT value as grader, -106 as haeldning_bygning, 1810 as skaering_bygning, iff((grader * -0.0225) + 0.3817 > 0.01, (grader * -0.0225) + 0.3817, 0.01)  as idealkurve, 'Syddjurs' as Kommune
FROM number_range;
```
// Bank branch openings and closures
/*
Compare the growth/decline of bank branches by state since the start of the pandemic.
*/
WITH pre_covid AS (
    SELECT state_abbreviation,
           COUNT(*) AS pre_covid_count
    FROM cybersyn.financial_branch_entities
    WHERE start_date <= '2020-03-01'
      AND (end_date >= '2020-03-01' OR end_date IS NULL)
    GROUP BY state_abbreviation
)
SELECT cur.state_abbreviation,
       pre_covid_count,
       COUNT(*)                            AS current_count,
       current_count / pre_covid_count - 1 AS pct_change
FROM cybersyn.financial_branch_entities AS cur
INNER JOIN pre_covid ON (cur.state_abbreviation = pre_covid.state_abbreviation)
WHERE end_date IS NULL
GROUP BY cur.state_abbreviation, pre_covid_count
ORDER BY pct_change;

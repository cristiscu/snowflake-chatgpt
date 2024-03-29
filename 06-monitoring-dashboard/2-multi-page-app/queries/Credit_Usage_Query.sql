-- Credit Usage Query
SELECT
    START_TIME,
    END_TIME,
    WAREHOUSE_NAME,
    CREDITS_USED
FROM
    SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE
    START_TIME >= DATEADD('hours', -24, CURRENT_TIMESTAMP())
ORDER BY
    START_TIME;
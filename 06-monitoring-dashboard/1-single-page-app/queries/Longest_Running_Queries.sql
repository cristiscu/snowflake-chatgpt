-- Longest Running Queries
SELECT 
    DATE_TRUNC('hour', start_time) AS hour_window, 
    AVG(EXECUTION_TIME) AS avg_execution_time_ms
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    dateadd('hours', -24, current_timestamp()), 
    current_timestamp()
))
GROUP BY 1
ORDER BY 1;
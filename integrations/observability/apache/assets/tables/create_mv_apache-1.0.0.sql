CREATE MATERIALIZED VIEW {table_name}_mview AS
SELECT
    `@timestamp`,
    clientip as `communication.source.ip`,
    split_part (request, ' ', 1) as `http.request.method`,
    split_part (request, ' ', 2) as `http.url`,
    split_part (request, ' ', 3) as `http.flavor`,
    status AS `http.response.status_code`,
    'apache.access' AS `event.domain`
FROM {table_name}
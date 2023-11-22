CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
   `@timestamp` TIMESTAMP,
    clientip STRING,
    request STRING, 
    status INT, 
    size INT, 
    year INT, 
    month INT, 
    day INT) 
USING json PARTITIONED BY(year, month, day) 
OPTIONS (path '{s3_bucket_location}', compression 'bzip2')
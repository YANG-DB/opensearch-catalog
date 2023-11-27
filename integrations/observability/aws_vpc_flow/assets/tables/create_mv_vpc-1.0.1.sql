CREATE MATERIALIZED VIEW {table_name}_mview AS
    SELECT
        version as `aws.vpc.version`,
        account_id as `aws.vpc.account-id`,
        interface_id as `aws.vpc.interface-id`,
        srcaddr as `aws.vpc.srcaddr`,
        dstaddr as `aws.vpc.dstaddr`,
        CAST(srcport AS INT) as `aws.vpc.srcport`,
        CAST(dstport AS INT) as `aws.vpc.dstport`,
        protocol as `aws.vpc.protocol`,
        CAST(packets AS LONG) as `aws.vpc.packets`,
        CAST(bytes AS LONG) as `aws.vpc.bytes`,
        CAST(FROM_UNIXTIME(start) AS TIMESTAMP) as `@timestamp`,
        CAST(FROM_UNIXTIME(end) AS TIMESTAMP) as `aws.vpc.end`,
        action as `aws.vpc.action`,
        log_status as `aws.vpc.log-status`,
        CASE
            WHEN regexp(dstaddr, '(10\\..*)|(192\\.168\\..*)|(172\\.1[6-9]\\..*)|(172\\.2[0-9]\\..*)|(172\\.3[0-1]\\.*)')
            THEN 'ingress'
            ELSE 'egress'
        END AS `aws.vpc.flow-direction`
FROM
    {table_name}
WITH (
  auto_refresh = true,
  refresh_interval = '30 Seconds',
  checkpoint_location = '{s3_bucket_location}/checkpoint',
  watermark_delay = '10 Second',
  output_mode = 'complete'
)
            
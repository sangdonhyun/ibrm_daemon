echo "======================================================================================================================================================="
$1/bin/sqlplus -s $2/$3@$4 << EOF
set lines 200
col "NO#" for 999
col DB_NAME for a12
col TYPE for a10
col START_TIME for a20
col END_TIME for a15
col STATUS for a20
col "INPUT_MByte" for 999,999,999
col "OUTPUT_MByte" for 999,999,999
col "OUT_BYTE/s" for a10
col "TIME_TAKEN" for a10
SELECT row_number() over (order by db_key) as NO#,
  DB_NAME,
  DB_KEY,
  INPUT_TYPE "TYPE",
  TO_CHAR(START_TIME,'yyyy-mm-dd hh24:mi:ss') START_TIME ,
  TO_CHAR(END_TIME,'mm-dd hh24:mi:ss') END_TIME ,
  STATUS,
  TRUNC(INPUT_BYTES /1024/1024) "INPUT_MByte" ,
  TRUNC(OUTPUT_BYTES/1024/1024) "OUTPUT_MByte",
  OUTPUT_BYTES_PER_SEC_DISPLAY "OUT_BYTE/s",
  TIME_TAKEN_DISPLAY "TIME_TAKEN"
FROM RC_RMAN_BACKUP_JOB_DETAILS
--- WHERE INPUT_TYPE IN ('DB INCR','DB FULL','ARCHIVELOG')
    WHERE INPUT_TYPE IN ('DB INCR','DB FULL')
AND (DB_NAME,START_TIME) IN
(SELECT DB_NAME,
  MAX(START_TIME) START_TIME
  FROM RC_RMAN_BACKUP_JOB_DETAILS
---  WHERE INPUT_TYPE IN ('DB INCR','DB FULL','ARCHIVELOG')
  WHERE INPUT_TYPE IN ('DB INCR','DB FULL')
  GROUP BY DB_NAME )
ORDER BY NO#, DB_KEY;
EOF

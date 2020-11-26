#!/bin/bash
display_usage() {
        echo ""
        echo "Enter Database Name"
        echo -e "\nUsage:\n$0 [DBNAME] \n"
        }

#if less than two arguments supplied, display usage
        if [  $# -lt 1 ]
        then
                display_usage
                exit 1
        fi
		
${ORACLE_HOME}/bin/sqlplus -s $1/$2@$3 << EOF		
set lines 200
set pagesize 40
col DB_NAME for a10
col start_time for a20
col end_time for a15
col input_type for a10
col STATUS for for a21
col "TIME_TAKEN" for a10
col "Output_MB" for 999,999,999
col "Input_MB" for 999,999,999
col "OUT_BYTE/s" for a10 
col "DEVICE" for a6
SELECT DB_NAME,
  TO_CHAR(start_time,'yyyy-mm-dd hh24:mi:ss') START_TIME ,
  TO_CHAR(end_time,'mm-dd hh24:mi:ss') END_TIME ,
  INPUT_TYPE ,
  STATUS,
  OUTPUT_DEVICE_TYPE "DEVICE",
  TRUNC(INPUT_BYTES /1024/1024) "Input_MB" ,
  TRUNC(OUTPUT_BYTES/1024/1024) "Output_MB" ,
  OUTPUT_BYTES_PER_SEC_DISPLAY "OUT_BYTE/s",
  TIME_TAKEN_DISPLAY "TIME_TAKEN"
FROM RC_RMAN_BACKUP_JOB_DETAILS jb
WHERE db_key =( select db_key from ( select row_number() over (order by db_key) as sr_no,reg_db_unique_name,db_key from db) where sr_no = $4)
and INPUT_TYPE IN ('DB INCR','DB FULL','ARCHIVELOG')
and start_time >= sysdate - 7
ORDER BY start_time,command_id
/
EOF

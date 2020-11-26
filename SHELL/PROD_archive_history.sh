sqlplus -s / as sysdba << EOF

set pages 80
set lines 160
col member for a70
col status for a10
col ARCHIVE_LOG_NAME for a100
col CREATOR for a8
col CREATE_DATE for a20

spool ${BACKUP_ARCH_DIR1}/2.Archive_history.log

SELECT a.group#, b.sequence#, a.member, b.bytes/1024/1024 MB, b.archived, b.status, b.first_change#
FROM v\$logfile a , v\$log b
WHERE a.group#=b.group#
ORDER BY 1;

select distinct SEQUENCE# as SEQUENCE_No, name as ARCHIVE_LOG_NAME, CREATOR, to_char(COMPLETION_TIME, 'yyyy/mm/dd hh24:mi:ss') as create_date from gv\$archived_log
	where to_char(COMPLETION_TIME, 'yyyymmdd') >= ${Arch_history}
	order by SEQUENCE_No;
spool off;

EOF

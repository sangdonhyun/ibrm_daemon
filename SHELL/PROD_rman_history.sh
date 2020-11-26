sqlplus -s / as sysdba << EOF
@/${SQLDIR}/rman_history.sql
EOF

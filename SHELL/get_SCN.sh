sqlplus -s / as sysdba << EOF
@/${SQLDIR}/check_SCN.sql
EOF

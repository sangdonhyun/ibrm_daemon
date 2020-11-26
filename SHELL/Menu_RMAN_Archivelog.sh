#!/bin/bash

echo " =================== Backup Started ==================="
if [ "$RUN_USER" = "root" ]
 then

        su - $ORACLE_USER -c "${RMANDIR}/backup_archivelog.sh  $DB_NAME  "
#        su - $ORACLE_USER -c "${SHELLDIR}/run_Archsnap.sh     $DB_NAME  "

        RSTAT=$?
 else

        /bin/sh -c "${RMANDIR}/backup_archivelog.sh  $DB_NAME  "
#        /bin/sh -c "${SHELLDIR}/run_Archsnap.sh     $DB_NAME  "

        RSTAT=$?
fi
################### status logging ######################
if [ "$RSTAT" = "0" ]
 then
            echo " [ CODE: $RSTAT ]                  				: `date '+%F_%H:%M:%S'`" >> $SHELL_LOG 
            echo "--------------------------------------------------------------------------------------"  >> $SHELL_LOG

 else
            echo " *** Error(s) has occured during Archive Log Manual Backup [ CODE: $RSTAT ] *** 	"   >> $SHELL_LOG
            echo "--------------------------------------------------------------------------------------"   >> $SHELL_LOG
fi
 exit $RSTAT


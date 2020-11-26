#!/bin/bash

echo " =================== Backup Started ==================="
if [ "$RUN_USER" = "root" ]
 then
        echo "======================================================================================"  >> $SHELL_LOG
        echo " Starting RMAN Level 1 + Merge Manual Backup                    : `date '+%F_%H:%M:%S'`" >> $SHELL_LOG


        su - $ORACLE_USER -c "${RMANDIR}/backup_rman_incr_level1.sh  $DB_NAME  "
        su - $ORACLE_USER -c "${SHELLDIR}/run_Daily_datasnap.sh      $DB_NAME  " 
 else

        echo "======================================================================================"  >> $SHELL_LOG
        echo " Starting RMAN Level 1 + Merge Manual Backup                    : `date '+%F_%H:%M:%S'`" >> $SHELL_LOG

        /bin/sh -c "${RMANDIR}/backup_rman_incr_level1.sh  $DB_NAME  "
        /bin/sh -c "${SHELLDIR}/run_Daily_datasnap.sh      $DB_NAME  " 

        RSTAT=$?
 fi
################### status logging ######################
if [ "$RSTAT" = "0" ]
 then
            echo " RMAN Incremental Level 1 Merge Backup has been finished        : `date '+%F_%H:%M:%S'`" >> $SHELL_LOG
            echo "======================================================================================"  >> $SHELL_LOG

 else
            echo " Error occured during RMAN Incremental Level 1 Backup [ CODE : $RSTAT ]  		" >> $SHELL_LOG
            echo "======================================================================================" >> $SHELL_LOG 
  fi
 exit $RSTAT


 echo "If you want to know that local backup snapshots list. Press [L] "
 echo "If you want to know that replicated backup snapshots list. Press [R] "
 echo -n "Enter your choice ( "L" or "R" ) : "
     read input
          input=`echo $input | tr '[a-z]' '[A-Z]'`
          if [ "$input" = L ]
               then
       	     	echo "=========================================================================="
    	     	echo "ZFS RMAN FULL Backup Snapshot List [ PROJECT: ${PROJNAME} ]"
    	             ${ZFSDIR}/show_snap.sh ${LOGINSTRING_1} ${POOLNAME_1} ${PROJNAME} ${SHARE_DATA_1} |grep -v " login:" 	
	     	echo "**************************************************************************"
	     	echo "ZFS Archive Log Backup Snapshot List "
  	      	     ${ZFSDIR}/show_snap.sh ${LOGINSTRING_1} ${POOLNAME_1} ${PROJNAME} ${SHARE_ARCH_1} |grep -v " login:"
	     	echo "=========================================================================="		
            else
            if [ "$input" = R ]
               then
	   	echo "=========================================================================="
	   	echo "List of replicated Data Snapshot [ SOURCE PROJECT: ${SPROJNAME} ]"
	       	     ${ZFSDIR}/show_rep_snap.sh ${RLOGINSTRING_1} ${SOURCENAME_1} ${PKGNAME_1} ${SPROJNAME} ${SDATANAME_1} |grep -v " login:"|grep -v ".rr-"
	     	echo "**************************************************************************"
	     	echo "List of Archive Log Backup Snapshot "
  	      	     ${ZFSDIR}/show_rep_snap.sh ${RLOGINSTRING_1} ${SOURCENAME_1} ${PKGNAME_1} ${SPROJNAME} ${SARCHNAME_1} |grep -v " login:"|grep -v ".rr-"
	   	echo "=========================================================================="

            fi
          fi

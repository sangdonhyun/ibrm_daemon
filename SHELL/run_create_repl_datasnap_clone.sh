echo "=========================================================================="
echo "Create Replicated Data Snapshot Image to Local Project!! "
echo -n "Input Replicated Data Snapshot Name for CloneDB : "
 read snapdata

echo -n "Please enter [y] to continue : "
 read yesno
      yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
   if [ "$yesno" = Y ]
      then

      i=1
        while [ $i -le $RDSHARE_NO ]
        do
#       ZFS="\${ZFSDIR}/make_project.sh  \${RLOGINSTRING_${i}} \${NPROJNAME} " ; echo $ZFS | sh
	ZFS1="\${ZFSDIR}/clone_replica.sh \${RLOGINSTRING_${i}} \${SOURCENAME_${i}} \${PKGNAME_${i}} \${SPROJNAME} \${SDATANAME_${i}} $snapdata \${NPROJNAME} \${SHARE_CLONE_DATA_${i}} " ; echo $ZFS1 | sh
      i=$(( $i + 1 ))
        done
   else
        echo "Request is canceled"
   fi
        echo "=========================================================================="

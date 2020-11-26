echo "-----------------------------------------------------------------------------"
echo "If you change this snapshot name then it would be not deleted by schedule    "
echo "Need to manually delete job if you want to delete changed snapshot.      "
echo "-----------------------------------------------------------------------------"

echo -n "Input Data Snapshot Name for CLONE DB :"
read datasnap

echo -n "Please enter [y] to continue : "
  read yesno
       yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
    if [ "$yesno" = Y ]
      then

        i=1
	while [ $i -le $DSHARE_NO ]
	do
          ZFS="\${ZFSDIR}/rename_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_DATA_${i}} ${datasnap} CLONE_${datasnap} " ; echo $ZFS | sh
          ZFS1="\${ZFSDIR}/clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_DATA_${i}} CLONE_${datasnap} \${SHARE_CLONE_DATA_${i}} " ; echo $ZFS1 | sh
            i=$(( $i + 1 ))
	done
      else
       echo "Request is canceled"
     fi

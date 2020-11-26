echo ""
echo "=========================================================================="
echo -n "Input Snapshot Name of Backup Archive Log : "
read snapshot

echo -n "Please enter [y] to continue : "
  read yesno
       yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
    if [ "$yesno" = Y ]
      then

	i=1
	while [ $i -le $ARCH_NO ]
	do
          ZFS="\${ZFSDIR}/clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_ARCH_${i}} $snapshot \${SHARE_CLONE_ARCH_${i}} " ; echo $ZFS | sh
          i=$(( $i + 1 ))
	done

     else
       echo "Request is canceled"
     fi

echo "=========================================================================="

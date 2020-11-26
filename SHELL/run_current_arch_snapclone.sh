if [ $# -lt 1 ]
then
        timestamp=`date '+%Y%m%d_%H%M'`
else
        timestamp=$1
fi

  echo -n "Please enter [y] to continue : "
  read yesno
       yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
    if [ "$yesno" = Y ]
    then

     i=1
	while [ $i -le $ARCH_NO ]
	do
          ZFS="\${ZFSDIR}/snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_ARCH_${i}} Arch_$timestamp " ; echo $ZFS | sh
          ZFS="\${ZFSDIR}/clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_ARCH_${i}} Arch_$timestamp \${SHARE_CLONE_ARCH_${i}} " ; echo $ZFS | sh
            i=$(( $i + 1 ))
	done

     else
       echo "Request is canceled"
     fi

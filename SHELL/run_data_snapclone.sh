echo ""
echo "=========================================================================="
echo -n "Input Data Snapshot Name for CloneDB : "
      read snapdata

echo -n "Please enter [y] to continue : "
   read yesno
             yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
     	if [ "$yesno" = Y ]
		   then

         i=1
      while [ $i -le $DSHARE_NO ]
do
ZFS="\${ZFSDIR}/clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_DATA_${i}} $snapdata \${SHARE_CLONE_DATA_${i}} " ; echo $ZFS | sh
         i=$(( $i + 1 ))
	   	done
      	else
       		echo "Request is canceled"
        fi

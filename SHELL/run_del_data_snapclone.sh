echo "If you want to delete a Local Shared Clone Data. Press [L] "
echo "If you want to delete a Replicated Shared Clone Data. Press [R] "
echo "=========================================================================="
echo -n "Enter your choice ( "Local" or "Replicate" ) : "
     read input
          input=`echo $input | tr '[a-z]' '[A-Z]'`
          if [ "$input" = L ]
              then
                echo    "Data Clone in the Project [ ${PROJNAME} ] will be deleted. "
		echo -n "Please enter [y] to continue : "
                read yesno
                     yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
                     if [ "$yesno" = Y ]
                        then
                         a=1
                         b=1
                            while [ $a -le $DSHARE_NO ]
                             do
                                ZFS="\${ZFSDIR}/del_clone.sh \${LOGINSTRING_${a}} \${POOLNAME_${a}} \${PROJNAME} \${SHARE_CLONE_DATA_${a}} " ; echo $ZFS | sh
                                a=$(( $a + 1 ))

                             done

                   else
                          echo "Request is canceled"
                   fi
           else
           if [ "$input" = R ]
               then
                echo    "Data Clone in the Project [ ${NPROJNAME} ] will be deleted."
		echo -n "Please enter [y] to continue : "
                read yesno
                     yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
                     if [ "$yesno" = Y ]
                        then
                          i=1
                          j=1
                             while [ $i -le $RDSHARE_NO ]
                              do
                                ZFS="\${ZFSDIR}/del_clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${NPROJNAME} \${SHARE_CLONE_DATA_${i}} " ; echo $ZFS | sh
                                i=$(( $i + 1 ))
                              done

                    else
                          echo "Request is canceled"

                    fi
            fi
           fi


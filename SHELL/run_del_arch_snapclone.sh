echo "If you want to delete a Local Shared Archive Log Clone. Press [L] "
echo "If you want to delete a Replicated Shared Archive Log Clone. Press [R] "
echo "=========================================================================="
echo -n "Enter your choice ( "Local" or "Replicate" ) : "
     read input
          input=`echo $input | tr '[a-z]' '[A-Z]'`
          if [ "$input" = L ]
              then
                echo    "Archive log Clone in the Project [ ${PROJNAME} ] will be deleted."
		echo -n "Please enter [y] to continue : "
                read yesno
                     yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
                     if [ "$yesno" = Y ]
                        then
                         i=1
                            while [ $i -le $ARCH_NO ]
                             do
                                ZFS1="\${ZFSDIR}/del_clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_CLONE_ARCH_${i}} " ; echo $ZFS1 | sh
                                i=$(( $i + 1 ))
                             done
                   else
                          echo "Request is canceled"
                   fi
           else
           if [ "$input" = R ]
               then
                echo    "Archive log Clone in the Project [ ${NPROJNAME} ] will be deleted."
		echo -n "Please enter [y] to continue : "
                read yesno
                     yesno=`echo $yesno | tr '[a-z]' '[A-Z]'`
                     if [ "$yesno" = Y ]
                        then
                          j=1
                             while [ $j -le $RARCH_NO ]
                              do
                                ZFS1="\${ZFSDIR}/del_clone.sh \${LOGINSTRING_${j}} \${POOLNAME_${j}} \${NPROJNAME} \${SHARE_CLONE_ARCH_${j}} " ; echo $ZFS1 | sh
                                j=$(( $j + 1 ))
                              done
                    else
                          echo "Request is canceled"

                    fi
                fi
           fi

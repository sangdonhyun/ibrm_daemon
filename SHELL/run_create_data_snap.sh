echo "If you want to create a Local Data Snap Clone. Press [L] "
echo "If you want to create a Replicated Data Snap Clone. Press [R] "
echo -n "Enter your choice ( "Local" or "Replicate" ) : "
     read input
          input=`echo $input | tr '[a-z]' '[A-Z]'`
          if [ "$input" = L ]
               then
       	     	echo "=========================================================================="
           	echo "If you want to use same snapshot name. Press [s] "
           	echo "If you want to change snapshot name for not schedule delete. Press [r] "
           	echo -n "Enter your choice ( "S" or "R" ) : "
            	     read input
               		input=`echo $input | tr '[a-z]' '[A-Z]'`
               		if [ "$input" = R ]
               		   then
                      		bash ${SHELLDIR}/run_rename_snapclone.sh
                        else
                 	   if [ "$input" = S ]
                  	      then
                      		bash ${SHELLDIR}/run_data_snapclone.sh
                 	   fi
               		fi
          else
           if [ "$input" = R ]
               then
                       bash ${SHELLDIR}/run_create_repl_datasnap_clone.sh
           fi
         fi

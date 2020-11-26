echo "If you want to create a Local Archive Snap Clone. Press [L] "
echo "If you want to create a Replicated Archive Snap Clone. Press [R] "
echo -n "Enter your choice ( "Local" or "Replicate" ) : "
     read input
          input=`echo $input | tr '[a-z]' '[A-Z]'`
          if [ "$input" = L ]
               then
       	     	echo "=========================================================================="
           	echo "If you want to use the backup snapshot name. Press [s] "
           	echo "If you want to create a new archive log snapshot at the current time. Press [c] "
           	echo -n "Enter your choice ( "S" or "C" ) : "
            	     read input
               		input=`echo $input | tr '[a-z]' '[A-Z]'`
               		if [ "$input" = C ]
               	  	   then
                    		bash ${SHELLDIR}/run_current_arch_snapclone.sh
                	   else
                 		if [ "$input" = S ]
                  		then
                    		   bash ${SHELLDIR}/run_arch_snapclone.sh
                 		fi
               		fi
          else
           if [ "$input" = R ]
               then
                       bash ${SHELLDIR}/run_create_repl_archsnap_clone.sh
           fi
         fi

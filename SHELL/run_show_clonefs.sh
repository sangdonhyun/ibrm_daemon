echo "If you want to know that shared Local Data list. Press [L] "
echo "If you want to know that shared Replicated Data list. Press [R] "
echo -n "Enter your choice ("L" or "R") : "
     read input
          input=`echo $input | tr '[a-z]' '[A-Z]'`
          if [ "$input" = L ]
               then
		i=1
		while [ $i -le $DSHARE_NO ]

		do
		echo "=========================================================================="
		echo "echo " List of Shared Local File systmes [ POOL: \${POOLNAME_${i}} ] [ PROJECT: \${PROJNAME} ]"" |sh
		echo ""
		 	ZFS1="\${ZFSDIR}/show_shared_fs.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} "; echo ${ZFS1} |sh |grep -v " login:"
       		     i=$(( $i + 1 ))
		done
		echo "=========================================================================="
            else
            if [ "$input" = R ]
               then
                i=1
                while [ $i -le $RDSHARE_NO ]

                do
                echo "===================================================================================================================="
                echo "echo " List of Shared Replicated File systmes [ POOL: \${POOLNAME_${i}} ] [ Source PROJECT: \${SPROJNAME} ] [ Repl PROJECT : \${NPROJNAME} ]"" |sh
                echo ""
                        ZFS1="\${ZFSDIR}/show_shared_fs.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${NPROJNAME} "; echo ${ZFS1} |sh |grep -v " login:"
                     i=$(( $i + 1 ))
                done
                echo "===================================================================================================================="

            fi
          fi

echo "Input CLONE_Data Name for delete !!"
read clone

i=1
while [ $i -le $DSHARE_NO ]
do
        ZFS="\${ZFSDIR}/del_clone.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} $clone " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

echo "Input Snap_Data Name for delete !!"
read snap

i=1
while [ $i -le $DSHARE_NO ]
do
        ZFS="\${ZFSDIR}/del_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} $snap \${SHARE_DATA_${i}} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

i=1
while [ "$i" -le "$DSHARE_NO" ]
do
        ZFS="\${ZFSDIR}/ch_zfs_latency.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_DATA_${i}} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

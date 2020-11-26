echo ""
echo "======================================================================="
echo "Select Backup Data Snapshot Name for Change !!"
read from_snap
echo "Input New Data Snapshot Name !!"
read to_snap

i=1
while [ $i -le $DSHARE_NO ]
do
        ZFS="\${ZFSDIR}/rename_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_DATA_${i}} ${from_snap} ${to_snap} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

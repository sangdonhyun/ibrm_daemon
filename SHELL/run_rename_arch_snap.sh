echo ""
echo "======================================================================="
echo "Select Archive LOG Snapshot Name for Change !!"
read from_snap
echo "Input New Archive LOG Snapshot Name !!"
read to_snap

i=1
while [ $i -le $ARCH_NO ]
do
        ZFS="\${ZFSDIR}/rename_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_ARCH_${i}} ${from_snap} ${to_snap} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

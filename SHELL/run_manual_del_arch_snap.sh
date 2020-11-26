echo "Input Snap_Archive Name for delete !!"
read snap

i=1
while [ $i -le $ARCH_NO ]
do
        ZFS="\${ZFSDIR}/del_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} $snap \${SHARE_ARCH_${i}} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done


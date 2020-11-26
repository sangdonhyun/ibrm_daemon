DB_NAME=$1
. ${BASEDIR}/SCRIPTS/Database/${DB_NAME}/ZFS_Profile

sh ${SHELLDIR}/run_show_PRODsnap.sh > /tmp/snaplist.out
grep Daily_Arch_ /tmp/snaplist.out |sort|uniq | awk '$1 < "Daily_Arch_'${Arch_SnapDate}'"' > /tmp/del_archlist.out

while read SNAP_ARCH
do

i=1
while [ $i -le $ARCH_NO ]
do
        ZFS="\${ZFSDIR}/del_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} $SNAP_ARCH \${SHARE_ARCH_${i}} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

done < /tmp/del_archlist.out

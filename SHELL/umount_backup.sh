  DATADIR=$1
. ${BASEDIR}/SCRIPTS/Database/${DATADIR}/ZFS_Profile

i=1
j=1
while [ $i -le $ARCH_NO ]
do
        ZFS="umount -f \${BACKUP_ARCH_DIR${i}} " ; echo ${ZFS} | sh
        i=$(( $i + 1 ))
done

while [ $j -le $DSHARE_NO ]
do
        ZFS="umount -f \${BACKUP_DATA_DIR${j}} " ; echo ${ZFS} | sh
        j=$(( $j + 1 ))
done


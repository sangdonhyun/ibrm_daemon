DB_NAME=$1
. ${BASEDIR}/SCRIPTS/Database/${DB_NAME}/ZFS_Profile

timestamp=`date '+%Y%m%d_%H%M'`

echo "${BACKUP_DATA_DIR1}/.zfs/snapshot/Monthly_Arch_$timestamp" >  ${BACKUP_DATA_DIR1}/arch_snapshot_tape.txt
echo "${BACKUP_DATA_DIR2}/.zfs/snapshot/Monthly_Arch_$timestamp" >> ${BACKUP_DATA_DIR1}/arch_snapshot_tape.txt

i=1
while [ "$i" -le "$ARCH_NO" ]
do
        ZFS="\${ZFSDIR}/snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_ARCH_${i}} Monthly_Arch_$timestamp " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

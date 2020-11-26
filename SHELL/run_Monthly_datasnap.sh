if [ $# -lt 1 ]
then
        timestamp=`date '+%Y%m%d_%H%M'`
else
        timestamp=$1
fi

echo "${BACKUP_DATA_DIR1}/.zfs/snapshot/Monthly_Data_$timestamp/DCH1" >  ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR1}/.zfs/snapshot/Monthly_Data_$timestamp/DCH3" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR1}/.zfs/snapshot/Monthly_Data_$timestamp/DCH5" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR1}/.zfs/snapshot/Monthly_Data_$timestamp/DCH7" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR2}/.zfs/snapshot/Monthly_Data_$timestamp/DCH2" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR2}/.zfs/snapshot/Monthly_Data_$timestamp/DCH4" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR2}/.zfs/snapshot/Monthly_Data_$timestamp/DCH6" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt
echo "${BACKUP_DATA_DIR2}/.zfs/snapshot/Monthly_Data_$timestamp/DCH8" >> ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt

i=1
while [ $i -le $DSHARE_NO ]
do
        ZFS="\${ZFSDIR}/snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_DATA_${i}} Monthly_Data_$timestamp " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done
echo "${BACKUP_DATA_DIR1}/.zfs/snapshot/Monthly_Data_$timestamp" > ${BACKUP_DATA_DIR1}/data_snapshot_tape.txt

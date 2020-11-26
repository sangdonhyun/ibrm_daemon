DB_NAME=$1
. ${BASEDIR}/SCRIPTS/Database/${DB_NAME}/ZFS_Profile

sh ${SHELLDIR}/run_show_PRODsnap.sh >> /tmp/snaplist.out
grep Weekly_Data_ /tmp/snaplist.out |sort|uniq | awk '$1 < "Weekly_Data_'${Weekly_SnapDate}'"' > /tmp/del_datalist.out

while read SNAP_DATA
do

i=1
while [ $i -le $DSHARE_NO ]
do
        ZFS="\${ZFSDIR}/del_snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} $SNAP_DATA \${SHARE_DATA_${i}} " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

done < /tmp/del_datalist.out

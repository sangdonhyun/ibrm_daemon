  CLONEDIR=$1
. ${BASEDIR}/SCRIPTS/CloneDB/${CLONEDIR}/CloneDB_Profile

i=1
j=1
while [ $i -le $ARCH_NO ]
do
        ZFS="umount -f \${CLONE_ARCH_DIR${i}} " ; echo ${ZFS} | sh
        i=$(( $i + 1 ))
done

while [ $j -le $DSHARE_NO ]
do
        ZFS="umount  \${CLONE_DATA_DIR${j}} " ; echo ${ZFS} | sh
        j=$(( $j + 1 ))
done

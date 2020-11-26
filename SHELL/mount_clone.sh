  CLONEDIR=$1
. ${BASEDIR}/SCRIPTS/CloneDB/${CLONEDIR}/CloneDB_Profile

i=1
j=1
while [ $i -le $DSHARE_NO ]
do
        ZFS="mount \${CLONE_DATA_DIR${i}} " ; echo ${ZFS} |sh
        i=$(( $i + 1 ))
done

while [ $j -le $ARCH_NO ]
do
        ZFS1="mount \${CLONE_ARCH_DIR${j}} " ; echo ${ZFS1} |sh
        j=$(( $j + 1 ))
done

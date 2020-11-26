if [ $# -lt 1 ]
then
        timestamp=`date '+%Y%m%d_%H%M'`
else
        timestamp=$1
fi

i=1
while [ $i -le $ARCH_NO ]
do
        ZFS="\${ZFSDIR}/snap.sh \${LOGINSTRING_${i}} \${POOLNAME_${i}} \${PROJNAME} \${SHARE_ARCH_${i}} Arch_$timestamp " ; echo $ZFS | sh
        i=$(( $i + 1 ))
done

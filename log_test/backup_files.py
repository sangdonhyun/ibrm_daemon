str="""
=========================================================================================================

Recovery Manager: Release 18.0.0.0.0 - Production on Tue Nov 24 13:30:24 2020
Version 18.6.0.0.0

Copyright (c) 1982, 2018, Oracle and/or its affiliates.  All rights reserved.

connected to target database: IBRM (DBID=212169558)
using target database control file instead of recovery catalog

RMAN> 2> 3> 4> 5> 6> 7> 8> 9> 10> 11> 12> 13> 14> 15> 16> 17> 18> 19> 20> 21> 22> 23> 24> 25> 26> 27> 28> 29> 30> 31> 32> 33> 34> 
allocated channel: DCH1
channel DCH1: SID=13 device type=DISK

allocated channel: DCH2
channel DCH2: SID=138 device type=DISK

allocated channel: DCH3
channel DCH3: SID=270 device type=DISK

allocated channel: DCH4
channel DCH4: SID=381 device type=DISK

Starting backup at 20/11/24
channel DCH1: starting datafile copy
input datafile file number=00002 name=+DATA/IBRM/DATAFILE/soe.272.1053701271
channel DCH2: starting datafile copy
input datafile file number=00005 name=+DATA/IBRM/DATAFILE/soe.271.1053700903
channel DCH3: starting datafile copy
input datafile file number=00008 name=+DATA/IBRM/DATAFILE/soe.273.1053701691
channel DCH4: starting datafile copy
input datafile file number=00003 name=+DATA/IBRM/DATAFILE/sysaux.258.1053699119
output file name=/u01/BACKUP/DATA_IBRM_02/DCH4/data_D-IBRM_I-212169558_TS-SYSAUX_FNO-3_abvgb0bs tag=ZFS_IBRM RECID=1625 STAMP=1057325571
channel DCH4: datafile copy complete, elapsed time: 00:02:15
channel DCH4: starting datafile copy
input datafile file number=00001 name=+DATA/IBRM/DATAFILE/system.257.1053699043
output file name=/u01/BACKUP/DATA_IBRM_02/DCH4/data_D-IBRM_I-212169558_TS-SYSTEM_FNO-1_acvgb0ge tag=ZFS_IBRM RECID=1626 STAMP=1057325718
channel DCH4: datafile copy complete, elapsed time: 00:02:17
channel DCH4: starting datafile copy
input datafile file number=00004 name=+DATA/IBRM/DATAFILE/undotbs1.259.1053699163
output file name=/u01/BACKUP/DATA_IBRM_02/DCH4/data_D-IBRM_I-212169558_TS-UNDOTBS1_FNO-4_advgb0l5 tag=ZFS_IBRM RECID=1627 STAMP=1057325850
channel DCH4: datafile copy complete, elapsed time: 00:01:58
channel DCH4: starting datafile copy
input datafile file number=00007 name=+DATA/IBRM/DATAFILE/users.260.1053699165
output file name=/u01/BACKUP/DATA_IBRM_02/DCH4/data_D-IBRM_I-212169558_TS-USERS_FNO-7_aevgb0pa tag=ZFS_IBRM RECID=1628 STAMP=1057325961
channel DCH4: datafile copy complete, elapsed time: 00:01:37
output file name=/u01/BACKUP/DATA_IBRM_01/DCH1/data_D-IBRM_I-212169558_TS-SOE_FNO-2_a8vgb0bi tag=ZFS_IBRM RECID=1629 STAMP=1057326197
channel DCH1: datafile copy complete, elapsed time: 00:12:57
output file name=/u01/BACKUP/DATA_IBRM_01/DCH3/data_D-IBRM_I-212169558_TS-SOE_FNO-8_aavgb0bl tag=ZFS_IBRM RECID=1630 STAMP=1057326203
channel DCH3: datafile copy complete, elapsed time: 00:12:51
output file name=/u01/BACKUP/DATA_IBRM_02/DCH2/data_D-IBRM_I-212169558_TS-SOE_FNO-5_a9vgb0bi tag=ZFS_IBRM RECID=1631 STAMP=1057326203
channel DCH2: datafile copy complete, elapsed time: 00:13:07
Finished backup at 20/11/24

Starting Control File and SPFILE Autobackup at 20/11/24
"""


import re


matchs=re.findall('datafile copy complete',str)

print len(matchs)
str="""94,     58779,RMAN: incremental datafile backup                               ,2567                                                            ,Set Count                       ,       610,       610,Blocks                          ,2020-08-18 10:30:13,2020-08-18 10:30:21,         ,             0,              8,         2,RMAN: incremental datafile backup: Set Count 2567: 610 out of 610 Blocks done                                                                                                                                                                                                                                                                                                                                                                                                                                                   ,SYS                           ,00              ,             0,             ,                  0,   16777902,                ,                              ,                              ,         0"""


aa=str.split(',')
print aa

for i in range(len(aa)):
    a=aa[i]
    print i,a.strip()

str2="""SID,   SERIAL#,OPNAME                                                          ,TARGET                                                          ,TARGET_DESC                     ,     SOFAR, TOTALWORK,UNITS                           ,START_TIME         ,LAST_UPDATE_TIME   ,TIMESTAMP,TIME_REMAINING,ELAPSED_SECONDS,   CONTEXT,MESSAGE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ,USERNAME                      ,SQL_ADDRESS     ,SQL_HASH_VALUE,SQL_ID       ,SQL_PLAN_HASH_VALUE,SQL_EXEC_ID,SQL_PLAN_LINE_ID,SQL_PLAN_OPERATION            ,SQL_PLAN_OPTIONS              ,     QCSID"""


bb=str2.split(',')
for i in range(len(bb)):
    b=bb[i]
    print i,b.strip()
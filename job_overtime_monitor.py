# -*- coding: utf-8 -*-
import os
import sys
import datetime
import ibrm_dbms
reload(sys)
sys.setdefaultencoding('utf-8')

class ov_mon():
    def __init__(self):
        self.rdb=ibrm_dbms.fbrm_db()


    def get_starting_job(self):
        dt=datetime.datetime.now() - datetime.timedelta(days=2)
        dt_format=dt.strftime('%Y%m%d')
        query=""" 

SELECT hs_job_dtl_id,hs_job_mst_id, tg_job_mst_id ,tg_job_dtl_id ,hjd.job_id,job_exec_dt ,job_stat,use_yn ,timeout,work_div_1,work_div_1,sh_id,mst.svr_id,mst.db_id,sh_file_nm,db_nm
FROM store.hs_job_dtl hjd LEFT OUTER JOIN 
            (
                SELECT mj.job_id,mj.job_nm ,ms.db_nm ,ms.sh_file_nm ,mj.timeout,mj.work_div_1 ,mj.work_div_2,mj.sh_id,ms.svr_id ,ms.db_id FROM master.mst_job mj 
                LEFT OUTER JOIN master.mst_shell ms ON mj.sh_id = ms.sh_id 
            ) mst
        ON hjd.job_id=mst.job_id WHERE mst.timeout > '0' AND hjd.job_stat IN ('Starting','Running') AND job_exec_dt > '{}'
        AND tg_job_dtl_id NOT IN (SELECT tg_job_dtl_id FROM event.evt_log WHERE EVT_CODE ='JOB_RUN_OVERTIME' )
        """.format(dt_format)
        print query
        ret_set=self.rdb.get_row(query)
        return ret_set
    def main(self):
        ret_set=self.get_starting_job()
        """
        hs_job_dtl_id,hs_job_mst_id,tg_job_mst_id ,tg_job_dtl_id ,job_id,job_exec_dt ,job_stat,use_yn ,timeout,work_div_1,work_div_1,sh_id,svr_id,db_id,sh_file_nm,db_nm        
        """
        titles = "hs_job_dtl_id,hs_job_mst_id,tg_job_mst_id,tg_job_dtl_id,job_id,job_exec_dt,job_stat,use_yn,timeout,work_div_1,work_div_1,sh_id,svr_id,db_id,sh_file_nm,db_nm".split(',')



        print ret_set

        if not ret_set == []:
            print 'count:',len(ret_set)
            for ret in ret_set:
                print ret

                job_info={}

                print len(ret)
                for i in range(len(titles)):
                    print titles[i],ret[i]
                    job_info[titles[i].strip()] = ret[i]
                print job_info
                self.set_event(job_info)


        def set_event(self,job_info):
            evt_info = {}

            print job_info.keys()
            print 'tg_job_dtl_id' in job_info.keys()
            print job_info['tg_job_dtl_id']
            evt_info['job_id'] = job_info['job_id']
            evt_info['tg_job_dtl_id'] = job_info['tg_job_dtl_id']
            log_dt = datetime.datetime.now().strftime('%Y%m%d')
            evt_info['log_dt'] = log_dt
            evt_info['svr_id'] = job_info['svr_id']
            evt_info['db_id'] = job_info['db_id']
            evt_info['sys_type'] = 'SCH'
            evt_info['evt_type'] = 'JOB_RUN_OVERTIME'
            evt_info['evt_code'] = 'JOB_RUN_OVERTIME'
            evt_info['evt_dtl_type'] = ''
            evt_info['evt_lvl'] = 'WARNNING'  # ERROR/CRITICAL/INFO
            evt_info['evt_msg'] = 'DB ({}) FILE ({})  LIMIT ORVER  JOB START TIME :{}  ,OVER TIME {} '.format(job_info['db_nm'],job_info['sh_file_nm'],job_info['job_exec_dt'],job_info['timeout'])

            # evt_info['evt_cntn'] = '{WORK_DIV_1} {WORK_DIV_2} {JOB_NM} {SH_NM} {SVR_NM} {DB_NM}'.format(
            #     WORK_DIV_1=work_div_1, WORK_DIV_2=work_div_2, JOB_NM=job_nm, SH_NM=sh_nm, SVR_NM=svr_nm, DB_NM=db_nm)
            evt_info['dev_type'] = 'DB'
            evt_info['act_yn'] = 'Y'
            evt_info['reg_usr'] = 'SYS'
            evt_info['reg_dt'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            evt_info_list = []
            evt_info_list.append(evt_info)
            # print 'evt_info :', evt_info
            table_name = 'event.evt_log'
            self.rdb.dbInsertList(evt_info_list, table_name)


if __name__=='__main__':
    ov_mon().main()
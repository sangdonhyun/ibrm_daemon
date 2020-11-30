#-*- coding: utf-8 -*-
import os
import ibrm_dbms
import datetime
import job_scheduler
import ibrm_logger
import ConfigParser
import logging

class ibrm_job_stat():
    def __init__(self):
        self.dbms=ibrm_dbms.fbrm_db()
        self.cfg = self.get_cfg()
        # self.log = ibrm_logger.ibrm_logger().logger('ibrm_server_job_status')




    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfg_file = os.path.join('config','config.cfg')
        cfg.read(cfg_file)
        return cfg
    def set_date(self):
        self.now = datetime.datetime.now()
        self.today_str = datetime.datetime.now().strftime('%Y%m%d')
        self.now_datetime = self.now.strftime('%Y%m%d%H%M%S')

    def job_stat_(self):
        """
        SELECT
        tg_job_dtl_id, tg_job_mst_id
        FROM
        store.tg_job_dtl
        where
        job_exec_dt = '20201106' and job_id = '42'

        SELECT
        hs_job_mst_id, tg_job_mst_id, job_exec_dt, job_stt_dt, job_end_dt, use_yn, mod_usr, mod_dt, reg_usr, reg_dt
        FROM
        store.hs_job_mst;


        SELECT
        hs_job_log_id, hs_job_dtl_id, hs_job_mst_id, pid, prgrs, run_spd, prgrs_time, adtnl_itm_1, adtnl_itm_2, rm_bk_stat, memo, use_yn, mod_usr, mod_dt, reg_usr, reg_dt
        FROM
        store.hs_job_log;

        insert
        into
        tg_job_mst_id, job_exec_dt, use_yn, mod_usr, mod_dt, reg_usr, ret_dt

        insert
        into
        store.hs_job_log(hs_job_dtl_id, hs_job_mst_id, rm_bk_stat, memo)


        """
    def get_hs_id(self,job_id):
        query = "SELECT  hs_job_dtl_id,hs_job_mst_id  FROM STORE.HS_JOB_DTL WHERE JOB_ID ='{JOB_ID}' and job_exec_dt='{EXEC_DT}'".format(
            JOB_ID=job_id, EXEC_DT=self.today_str)
        hs_job_dtl_id,hs_job_mst_id='',''

        try:
            ret_set = self.dbms.getRaw(query)
            if len(ret_set) > 0:
                hs_job_dtl_id = ret_set[0][0]
                hs_job_mst_id = ret_set[0][1]
        except Exception as e:
            print query
            print str(e)

            # self.log.error('hs_job_dtl_id error')
            # self.log.error('job_id :{}'.format(job_id))

        return hs_job_dtl_id,hs_job_mst_id


    def job_complete(self,job_info):
        self.set_date()
        job_id = job_info['job_id']
        self.job_update(job_info)

    def job_start_setup(self,job_info):
        self.set_date()
        job_id=job_info['job_id']
        tg_job_dtl_id, tg_job_mst_id = self.get_tg_id(job_id)



        table_name = 'store.hs_job_mst'
        query = "select count(*) from {} where tg_job_mst_id = '{}' and job_exec_dt = '{}'".format(table_name,tg_job_mst_id,job_info['job_exec_dt'])
        print query
        mst_cnt = self.dbms.getRaw(query)[0][0]
        print 'mst cnt :',mst_cnt,type(mst_cnt),mst_cnt == 0
        if mst_cnt == 0:
            set_job = {}
            set_job['tg_job_mst_id'] = job_info['tg_job_mst_id']
            set_job['job_exec_dt'] = job_info['job_exec_dt']
            set_job['job_stt_dt'] = ''
            set_job['job_end_dt'] = ''
            set_job['use_yn'] = 'Y'
            set_job['mod_usr'] = 'SYS'
            set_job['mod_dt'] = self.now_datetime
            set_job['reg_usr'] = 'SYS'
            set_job['reg_dt'] = self.now_datetime
            job_list = []
            job_list.append(set_job)
            print set_job
            print set_job.keys()

            self.dbms.dbInsertList(job_list, table_name)


        query ="select hs_job_mst_id from store.hs_job_mst where tg_job_mst_id ='{}' and job_exec_dt = '{}'".format(tg_job_mst_id,self.today_str)
        hs_job_mst_id =  self.dbms.getRaw(query)[0][0]
        set_job = {}
        set_job['tg_job_mst_id'] = job_info['tg_job_mst_id']
        set_job['hs_job_mst_id'] = hs_job_mst_id
        set_job['tg_job_dtl_id'] = job_info['tg_job_dtl_id']
        set_job['job_id'] = job_info['job_id']
        set_job['job_exec_dt'] = job_info['job_exec_dt']
        set_job['db_type'] = 'no catalog'
        set_job['job_stt_dt'] = ''
        set_job['job_end_dt'] = ''
        set_job['run_type'] = 'Run'
        set_job['job_stat'] = 'Starting'
        set_job['upd_stat'] = ''
        set_job['use_yn'] = 'Y'
        set_job['mod_usr'] = 'SYS'
        set_job['mod_dt'] = self.now_datetime
        set_job['reg_usr'] = 'SYS'
        set_job['reg_dt'] = self.now_datetime
        table_name = 'store.hs_job_dtl'
        job_list = [set_job]
        set_job
        self.dbms.dbInsertList(job_list, table_name)

    def job_status_insert(self,job_status):
        self.set_date()

        tg_job_dtl_id = job_status['tg_job_dtl_id']
        print 'tg_job_dtl_id',tg_job_dtl_id


        query = "SELECT hs_job_dtl_id, hs_job_mst_id, tg_job_mst_id	FROM store.hs_job_dtl where tg_job_dtl_id = '{TG_JOB_DTL_ID}'".format(
            TG_JOB_DTL_ID=tg_job_dtl_id)
        print query
        ret_set = self.dbms.getRaw(query)[0]
        hs_job_dtl_id = ret_set[0]
        hs_job_mst_id = ret_set[1]

        data_set = {}
        data_set['hs_job_dtl_id'] = hs_job_dtl_id
        data_set['hs_job_mst_id'] = hs_job_mst_id
        data_set['pid'] = job_status['pid']
        data_set['prgrs'] = ''
        data_set['adtnl_itm_1'] = ''
        data_set['adtnl_itm_2'] = ''
        data_set['run_spd'] = job_status['write_bps']
        if job_status['elapsed_seconds'] == '':
            prgs_time = 0
        else:
            prgs_time = int(job_status['elapsed_seconds'])
        data_set['prgrs_time'] = prgs_time
        data_set['rm_bk_stat'] = job_status['status']
        data_set['bk_in_size'] = job_status['input_bytes']
        data_set['memo'] = ''
        data_set['use_yn'] = 'Y'
        data_set['mod_usr'] = 'SYS'
        data_set['mod_dt'] = self.now_datetime
        data_set['reg_usr'] = 'SYS'
        data_set['reg_dt'] = self.now_datetime
        data_list = []
        data_list.append(data_set)
        db_table = 'store.hs_job_log'
        try:
            self.dbms.dbInsertList(data_list, db_table)
        except Exception as e:
            print str(e)




        print 'start_time :',job_status['start_time']
        print 'end_time :',job_status['end_time']
        try:
            start_time = datetime.datetime.strptime(job_status['start_time'],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        except Exception as e:
            start_time = ''
            print str(e)
        try:
            end_time = datetime.datetime.strptime(job_status['end_time'],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        except Exception as e:
            end_time = ''
            print str(e)
        print 'start time :',start_time,end_time
        query = """UPDATE store.HS_JOB_DTL
        SET 
        job_stt_dt='{JOB_STT_DT}', 
        job_end_dt='{JOB_END_DT}', 
        prgrs_time='{PRGRS_TIME}', 
        mod_usr='SYS' ,
        mod_dt='{MOD_DT}' ,
        rm_bk_stat = '{RM_BK_STAT}',
        job_stat='{JOB_STAT}'
        WHERE hs_job_dtl_id = '{MST_ID}';
                    """.format(JOB_STT_DT=start_time,
                               JOB_END_DT=end_time,
                               PRGRS_TIME=prgs_time,
                               MOD_DT=self.now_datetime,
                               RM_BK_STAT=job_status['status'],
                               JOB_STAT=job_status['job_st'],
                               MST_ID=hs_job_dtl_id)
        print '#'*50
        print query
        print '#'*50
        self.dbms.queryExec(query)



    def job_log_update(self, log_return_data):
            self.set_date()
            print 'LOG_UPDATE 33333'
            print log_return_data['job_id']
            job_id = log_return_data['job_id']
            tg_job_dtl_id = log_return_data['tg_job_dtl_id']
            print 'tg_job_dtl_id :',tg_job_dtl_id
            query = "SELECT hs_job_dtl_id, hs_job_mst_id, tg_job_mst_id	FROM store.hs_job_dtl where tg_job_dtl_id = '{TG_JOB_DTL_ID}'".format(
                TG_JOB_DTL_ID=tg_job_dtl_id)
            print 'qeury :',query
            ret_set = self.dbms.getRaw(query)[0]
            hs_job_dtl_id = ret_set[0]
            hs_job_mst_id = ret_set[1]
            tg_job_mst_id = ret_set[2]



            query = "SELECT COUNT(hs_job_dtl_id) FROM STORE.HS_JOB_LOGFILE WHERE hs_job_mst_id = '{}'".format(
                hs_job_mst_id)
            print query

            cnt_set = self.dbms.getRaw(query)
            cnt = cnt_set[0][0]
            if int(cnt) == 0:
                ins_bit = True
            else:
                ins_bit = False
            print 'INS BIT :', ins_bit
            print log_return_data['log_contents']
            log_file = os.path.basename(log_return_data['log_contents'])
            print log_file
            print 'sections :',self.cfg.sections()
            print 'options :', self.cfg.options('common')
            log_path = self.cfg.get('common', 'log_file_path')

            # log_path = os.path.join('E:\\','Fleta','data','ibrm_backup_log',log_file)
            log_path = os.path.join(log_path, log_file)
            print 'log path :',log_path,os.path.isfile(log_path)
            if os.path.isfile(log_path):
                with open(log_path) as f:
                    log_content = f.read()
                log_content = log_content.replace("'", '`')
            else:
                log_content = 'NOT FOUND'



            if ins_bit:
                log_data = {}
                log_data['hs_job_dtl_id'] = hs_job_dtl_id
                log_data['hs_job_mst_id'] = hs_job_mst_id
                log_data['pid'] = log_return_data['pid']
                log_data['logfile_nm'] = log_return_data['log_file']
                log_data['file_cntn'] = log_content
                log_data['rm_bk_stat'] = log_return_data['status']
                log_data['prgrs_time'] = log_return_data['elapsed_seconds']
                log_data['use_yn'] = 'Y'
                log_data['memo'] = ''
                log_data['mod_usr'] = ''
                log_data['mod_dt'] = ''
                log_data['reg_usr'] = 'SYS'
                log_data['reg_dt'] = self.now_datetime
                print log_data
                log_update_list = []
                log_update_list.append(log_data)
                table_name = 'store.hs_job_logfile'
                print log_data
                self.dbms.dbInsertList(log_update_list, table_name)
            else:
                reg_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                query = """UPDATE store.hs_job_logfile
    	SET file_cntn='{LOG_CONTENT}', rm_bk_stat='{JOB_ST}', prgrs_time='{ELAPSED_SEC}', mod_dt='{MOD_DT}'
    	WHERE hs_job_mst_id = '{MST_ID}';
                """.format(LOG_CONTENT=log_content, JOB_ST=log_return_data['status'],
                           ELAPSED_SEC=log_return_data['elapsed_seconds'], MOD_DT=reg_date, MST_ID=hs_job_mst_id)
                print query
                self.dbms.queryExec(query)

    def get_job(self):
            sql = """
    SELECT 
      tjm.tg_job_mst_id  -- 0[일작업ID] 일일 대상 작업 MST ID   
      ,tjm.job_exec_dt   -- 1[작업실행일자] DB 일자 or SYSTEM   
      ,tjd.tg_job_dtl_id -- 2[일작업상세ID]    
      ,tjd.run_type      -- 3[실행유형] Run, Stop, ReRun, Skip, Force Run    
      ,mj.exec_time      -- 4[실행시각] 0000~2359       
      ,mj.timeout        -- 5[제한시간] 작업 Timeout 시각(알람 설정 시 사용)    
      ,mj.alarm_yn       -- 6[알림여부]    
      ,ms.svr_nm         -- 7[서버명] 서버명                           
      ,ms.ip_addr        -- 8[IP 정보] ipv4                        
      ,ms.db_nm          -- 9[DB 명]                              
      ,ms.back_type      -- 10[백업유형] incr / arch / full / merge   
      ,ms.sh_file_nm     -- 11[쉘 파일명] Real 파일명                    
      ,ms.sh_path        -- 12[쉘 경로] 쉘스크립트 경로                     
      ,moi.ora_sid       -- 13SID     
      ,moi.ora_home      -- 14ORACLE HOME
      ,moi.db_name       -- 15DB명 
      ,tjm.tg_job_mst_id -- 16[일작업ID] 일일 대상 작업 MST ID   
      ,tjm.job_exec_dt   -- 17[작업실행일자] DB 일자 or SYSTEM   
      ,tjd.tg_job_dtl_id -- 18[일작업상세ID]    
      ,tjd.job_id        -- 19[작업ID] JOB ID Unique 
    FROM 
      store.tg_job_mst tjm 
      INNER JOIN 
      store.tg_job_dtl tjd 
      ON ( 
          tjm.tg_job_mst_id = tjd.tg_job_mst_id 
          AND tjd.use_yn='Y' 
          AND tjd.run_type ='Run'
        )
      INNER JOIN 
      master.mst_job mj 
      ON ( 
        mj.use_yn ='Y'
        AND mj.job_id = tjd.job_id        
      )
      INNER JOIN 
      master.mst_shell ms 
      ON (
        ms.use_yn ='Y'
        AND ms.sh_id = mj.sh_id      
      )
      INNER JOIN 
      master.master_svr_info msi 
      ON (msi.svr_id = ms.svr_id )
      INNER JOIN 
      master.master_ora_info moi 
      ON (
        moi.svr_id = msi.svr_id 
        AND moi.ora_id = ms.db_id 
      )  
    WHERE 
      tjm.use_yn ='Y'
     -- AND tjm.job_exec_dt = to_char(now(), 'YYYYMMDD') -- 실행일자로 변경하여 사용   
     -- AND tjm.job_exec_dt = '20201023' -- 실행일자로 변경하여 사용   

    and tjd.job_id  = 13
    """
            print sql
            ret = self.dbms.getRaw(sql)[0]

            job_id = ret[0]
            svr_ip = ret[8]

            shell_type = ret[10]
            shell_name = ret[11]
            shell_path = ret[12]
            ora_home = ret[14]
            ora_sid = ret[13]
            db_name = ret[15]
            job_info = {}
            job_info['job_id'] = job_id
            job_info['svr_ip'] = svr_ip
            job_info['shell_type'] = shell_type
            job_info['shell_name'] = shell_name
            job_info['shell_path'] = shell_path
            job_info['ora_home'] = ora_home
            job_info['db_name'] = db_name
            job_info['ora_sid'] = ora_sid
            job_info['tg_job_mst_id'] = ret[16]
            job_info['job_exec_dt'] = ret[17]
            job_info['tg_job_dtl_id'] = ret[18]
            job_info['job_id'] = ret[19]
            job_info['job_exec_dt'] = ret[1]

            return job_info


    def get_tg_id(self,job_id):
        now = datetime.datetime.now()
        today_str = datetime.datetime.now().strftime('%Y%m%d')
        now_datetime = now.strftime('%Y%m%d%H%M%S')
        tg_job_dtl_id, tg_job_mst_id = '',''
        query = """SELECT
                tg_job_dtl_id, tg_job_mst_id
                FROM
                store.tg_job_dtl
                where
                job_exec_dt = '{EXEC_DT}' and job_id = '{JOB_ID}' order by 1 desc
                """.format(EXEC_DT=today_str, JOB_ID=job_id)

        try:
            ret_set = self.dbms.getRaw(query)
            if len(ret_set) > 0:
                tg_job_dtl_id = ret_set[0][0]
                tg_job_mst_id = ret_set[0][1]
        except:
            pass

        return tg_job_dtl_id,tg_job_mst_id

        # job_info = {}
        # job_info['hs_job_dtl_id'] = hs_job_dtl_id
        # job_info['hs_job_mst_id'] = hs_job_mst_id
        # job_info['rm_bk_stat'] = 'Fail'
        # # job_info['memo'] = 'This job is already running'
        # job_info['use_yn'] = 'Y'
        # job_info['pid'] = ''
        # job_info['mod_usr'] = 'SYS'
        # job_info['mod_dt'] = self.now_datetime
        # job_info['reg_usr'] = 'SYS'
        # job_info['reg_dt'] = self.now_datetime
        # job_info['adtnl_itm_1'] = ''
        # job_info['adtnl_itm_2'] = ''
        # job_info['memo'] = memo
        # job_info_list = [job_info]
        # table_name = 'store.hs_job_log'
        # self.dbms.dbInsertList(job_info_list, table_name)


    def get_job_id(self,tg_job_dtl_id):
        self.set_date()

        query = "SELECT hs_job_dtl_id, hs_job_mst_id, tg_job_mst_id	FROM store.hs_job_dtl where tg_job_dtl_id = '{TG_JOB_DTL_ID}'".format(
            TG_JOB_DTL_ID=tg_job_dtl_id)
        print query
        ret_set = self.dbms.getRaw(query)[0]
        hs_job_dtl_id = ret_set[0]
        hs_job_mst_id = ret_set[1]
        tg_job_mst_id = ret_set[2]
        job_id={}
        job_id['hs_job_dtl_id'] = hs_job_dtl_id
        job_id['hs_job_mst_id'] = hs_job_mst_id
        job_id['tg_job_mst_id'] = tg_job_mst_id
        return job_id

    def job_submit_fila(self,job_id,tg_job_dtl_id,memo):
        memo = memo.replace("'","`")
        self.set_date()

        query = "SELECT hs_job_dtl_id, hs_job_mst_id, tg_job_mst_id	FROM store.hs_job_dtl where tg_job_dtl_id = '{TG_JOB_DTL_ID}'".format(TG_JOB_DTL_ID=tg_job_dtl_id)
        print query
        ret_set = self.dbms.getRaw(query)[0]
        hs_job_dtl_id = ret_set[0]
        hs_job_mst_id = ret_set[1]
        tg_job_mst_id = ret_set[2]


        print hs_job_dtl_id,hs_job_mst_id,tg_job_mst_id


        query = """UPDATE store.hs_job_dtl SET
                
                job_stat ='Fail', 
                rm_bk_stat ='Run Fail', 
                memo = '{memo}',
                mod_dt ='{MOD_DT}'

                WHERE hs_job_dtl_id = '{HS_JOB_DTL_ID}'
        """.format(memo=memo,MOD_DT=self.today_str,HS_JOB_DTL_ID=hs_job_dtl_id)
        print query
        self.dbms.queryExec(query)

        job_info = {}
        job_info['hs_job_dtl_id'] = hs_job_dtl_id
        job_info['hs_job_mst_id'] = hs_job_mst_id
        job_info['rm_bk_stat'] = 'Fail'
        # job_info['memo'] = 'This job is already running'
        job_info['use_yn'] = 'Y'
        job_info['pid'] = ''
        job_info['mod_usr'] = 'SYS'
        job_info['mod_dt'] = self.now_datetime
        job_info['reg_usr'] = 'SYS'
        job_info['reg_dt'] = self.now_datetime
        job_info['adtnl_itm_1'] = ''
        job_info['adtnl_itm_2'] = ''
        job_info['memo'] = memo
        job_info_list = [job_info]
        table_name = 'store.hs_job_log'
        self.dbms.dbInsertList(job_info_list, table_name)
        ret_data = {'FLETA_PASS': 'kes2719!', 'CMD': 'JOB_UPDATE_SUCC', 'ARG': {'result': 'succ'}}
        return ret_data

    def job_aleady_exist(self,job_id,tg_job_dtl_id,memo):
        memo = memo.replace("'", "`")

        now_str=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        print now_str

        query="""UPDATE store.hs_job_dtl SET job_stat='Fail', memo='{}',mod_dt='{}' WHERE tg_job_dtl_id = '{}' """.format(memo,now_str,tg_job_dtl_id)
        print query
        self.dbms.queryExec(query)

        # job_id_info = self.get_job_id(tg_job_dtl_id)
        # hs_job_dtl_id = job_id_info['hs_job_dtl_id']
        # hs_job_mst_id = job_id_info['hs_job_mst_id']
        # tg_job_mst_id = job_id_info['tg_job_mst_id']
        # query = "select hs_job_dtl_id from store.hs_job_dtl where job_id = '{JOB_ID}' and job_exec_dt = '{TODAY}'".format(
        #     JOB_ID=job_id, TODAY=self.today_str)
        # print query
        # try:
        #     ret_set = self.dbms.getRaw(query)
        # except:
        #     pass
        # hs_job_dtl_id = ret_set[0][0]
        #
        # job_info = {}
        # job_info['hs_job_dtl_id'] = hs_job_dtl_id
        # job_info['hs_job_mst_id'] = hs_job_mst_id
        # job_info['rm_bk_stat'] = 'Fail'
        # # job_info['memo'] = 'This job is already running'
        # job_info['use_yn'] = 'Y'
        # job_info['pid'] = ''
        # job_info['mod_usr'] = 'SYS'
        # job_info['mod_dt'] = self.now_datetime
        # job_info['reg_usr'] = 'SYS'
        # job_info['reg_dt'] = self.now_datetime
        # job_info['adtnl_itm_1'] = ''
        # job_info['adtnl_itm_2'] = ''
        # job_info['memo'] = memo
        #
        # job_info_list = [job_info]
        # table_name = 'store.hs_job_log'
        #
        # self.dbms.dbInsertList(job_info_list, table_name)




    def job_fail_proc(self,job_id,memo):
        memo = memo.replace("'", "`")
        self.set_date()
        tg_job_dtl_id,tg_job_mst_id = self.get_tg_id(job_id)

        table_name = 'store.hs_job_mst'
        #memo='This job is already running'
        """
        tg_job_mst_id, job_exec_dt, use_yn, mod_usr, mod_dt, reg_usr, ret_dt
        """
        query = "select count(tg_job_mst_id) from store.tg_job_mst where tg_job_mst_id='{TG_JOB_MST_ID}' and job_exec_dt='{JOB_EXEC_DT}' ".format(TG_JOB_MST_ID=tg_job_mst_id,JOB_EXEC_DT=self.today_str)
        print query
        cnt = self.dbms.getRaw(query)[0][0]
        print 'cnt :',cnt,cnt == 0
        if cnt == 0:
            job_info={}
            job_info['tg_job_mst_id'] =tg_job_mst_id
            job_info['job_exec_dt'] = self.today_str
            job_info['job_stt_dt'] = ''
            job_info['job_end_dt'] = ''
            job_info['use_yn'] = 'Y'
            job_info['mod_usr'] = 'SYS'
            job_info['mod_dt'] = self.now_datetime
            job_info['reg_usr'] = 'SYS'
            job_info['reg_dt'] = self.now_datetime
            job_info_list=[]
            job_info_list.append(job_info)
            table_name = 'store.hs_job_mst'
            self.dbms.dbInsertList(job_info_list,table_name)

        """
        store.hs_job_log(hs_job_dtl_id, hs_job_mst_id, rm_bk_stat, memo
        """
        query = "select hs_job_mst_id from store.hs_job_mst where tg_job_mst_id = '{TG_JOB_MST_ID}'".format(TG_JOB_MST_ID=tg_job_mst_id)
        print query
        try:
            ret_set = self.dbms.getRaw(query)
        except:
            pass
        hs_job_mst_id = ret_set[0][0]




        job_info={}
        job_info['hs_job_mst_id'] = hs_job_mst_id
        job_info['tg_job_dtl_id'] = tg_job_dtl_id
        job_info['tg_job_mst_id'] = tg_job_mst_id
        job_info['job_id'] = job_id
        job_info['job_exec_dt'] = self.today_str
        job_info['job_stt_dt'] = ''
        job_info['job_end_dt'] = ''
        job_info['db_type'] = 'no catalog'
        job_info['run_type'] = ''
        job_info['job_stat'] = 'Fail'
        job_info['memo'] = memo
        job_info['mod_usr'] = 'SYS'
        job_info['mod_dt'] = self.now_datetime
        job_info['reg_usr'] = 'SYS'
        job_info['reg_dt'] = self.now_datetime
        job_info_list = [job_info]
        table_name = 'store.hs_job_dtl'
        self.dbms.dbInsertList(job_info_list, table_name)



        query = "select hs_job_dtl_id from store.hs_job_dtl where job_id = '{JOB_ID}' and job_exec_dt = '{TODAY}'".format(JOB_ID=job_id,TODAY=self.today_str)
        print query
        try:
            ret_set = self.dbms.getRaw(query)
        except:
            pass
        hs_job_dtl_id = ret_set[0][0]

        job_info = {}
        job_info['hs_job_dtl_id']=hs_job_dtl_id
        job_info['hs_job_mst_id'] = hs_job_mst_id
        job_info['rm_bk_stat'] = 'Fail'
        # job_info['memo'] = 'This job is already running'
        job_info['use_yn'] = 'Y'
        job_info['pid'] = ''
        job_info['mod_usr'] = 'SYS'
        job_info['mod_dt'] =  self.now_datetime
        job_info['reg_usr'] = 'SYS'
        job_info['reg_dt'] = self.now_datetime
        job_info['adtnl_itm_1'] = ''
        job_info['adtnl_itm_2'] = ''
        job_info['memo'] = memo

        job_info_list = [job_info]
        table_name = 'store.hs_job_log'

        self.dbms.dbInsertList(job_info_list,table_name)

    def job_update(self, job_status):
        self.set_date()
        job_id = job_status['job_id']
        tg_job_dtl_id = job_status['tg_job_dtl_id']


        query = "SELECT hs_job_dtl_id, hs_job_mst_id, tg_job_mst_id	FROM store.hs_job_dtl where tg_job_dtl_id = '{TG_JOB_DTL_ID}'".format(
            TG_JOB_DTL_ID=tg_job_dtl_id)
        print query
        ret_set = self.dbms.getRaw(query)[0]
        hs_job_dtl_id = ret_set[0]
        hs_job_mst_id = ret_set[1]
        tg_job_mst_id = ret_set[2]



        print 'tg_job_dtl_id :',tg_job_dtl_id
        print 'tg_job_mst_id :', tg_job_mst_id
        print 'hs_job_dtl_id :', hs_job_dtl_id
        print 'hs_job_mst_id :', hs_job_mst_id

        print 'job_update : '

        """
    {'FLETA_PASS': 'kes2719!', 'CMD': 'JOB_STATUS', 'ARG': {'status': 'COMPLETED', 'start_time': '2020-10-25 12:37:00', 'pid': '3335',
    'elapsed_seconds': '803', 'session_recid': '515', 'job_id': '13', 'input_type': 'DB INCR',
    'session_id': '515', 'end_time': '2020-10-25 12:50:23', 'write_bps': '117.98M',
    'session_stamp': '1054730218', 'ora_sid': 'ibrm'}}

        :param job_status:
        :return:
        """
        if 'COMPLETED' in job_status['status']:
            job_st = 'END-OK'
        else:
            job_st = 'Running'

        mod_dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        job_stt_dt = datetime.datetime.strptime(job_status['start_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        job_end_dt = datetime.datetime.strptime(job_status['end_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        ssn_rec_id = job_status['session_recid']
        ssn_stmp = job_status['session_stamp']
        rm_bk_stat = job_status['status']
        prgrs_time = job_status['elapsed_seconds']

        query = """UPDATE store.hs_job_dtl SET
                job_stt_dt ='{JOB_STT_DT}', 
                job_end_dt = '{JOB_END_DT}',
                ssn_rec_id ='{SSN_REC_ID}', 
                ssn_stmp ='{SSN_STMP}', 
                run_type ='Run', 
                job_stat ='{JOB_STATUS}', 
                rm_bk_stat ='{RM_BK_STAT}', 
                prgrs_time ='{PRGRS_TIME}',
                mod_dt ='{MOD_DT}'

                WHERE hs_job_dtl_id = '{HS_JOB_DTL_ID}'
                """.format(JOB_STT_DT=job_stt_dt, JOB_END_DT=job_end_dt, SSN_REC_ID=ssn_rec_id, SSN_STMP=ssn_stmp,
                           JOB_STATUS=job_st, RM_BK_STAT=rm_bk_stat, PRGRS_TIME=prgrs_time, MOD_DT=mod_dt,
                           HS_JOB_DTL_ID=hs_job_dtl_id)
        print query

        self.dbms.queryExec(query)


        # job_info = {}
        # job_info['hs_job_dtl_id'] = hs_job_dtl_id
        # job_info['hs_job_mst_id'] = hs_job_mst_id
        # job_info['rm_bk_stat'] = 'Fail'
        # # job_info['memo'] = 'This job is already running'
        # job_info['use_yn'] = 'Y'
        # job_info['pid'] = ''
        # job_info['mod_usr'] = 'SYS'
        # job_info['mod_dt'] = self.now_datetime
        # job_info['reg_usr'] = 'SYS'
        # job_info['reg_dt'] = self.now_datetime
        # job_info['adtnl_itm_1'] = ''
        # job_info['adtnl_itm_2'] = ''
        # job_info['memo'] = ''
        # job_info_list = [job_info]
        # table_name = 'store.hs_job_log'
        # self.dbms.dbInsertList(job_info_list, table_name)





        ret_data =  {'FLETA_PASS': 'kes2719!', 'CMD': 'JOB_UPDATE_SUCC', 'ARG':{'result':'succ'}}
        return ret_data






    def job_status_fail_update(self,job_id):
        self.set_date()
        hs_job_dtl_id,hs_job_mst_id = self.get_hs_id(job_id)

        query = "SELECT  hs_job_dtl_id,hs_job_mst_id  FROM STORE.HS_JOB_DTL WHERE JOB_ID ='{JOB_ID}' and job_exec_dt='{EXEC_DT}'".format(JOB_ID=job_id,EXEC_DT=self.today_str)
        ret_set = self.dbms.getRaw(query)
        if len(ret_set) > 0:
            hs_job_dtl_id = ret_set[0][0]
            hs_job_mst_id = ret_set[0][1]




        query = """UPDATE store.hs_job_dtl SET
               run_type ='RUN', 
               job_stat ='Fail', 
               mod_dt ='{MOD_DT}'
               memo = ''

               WHERE hs_job_dtl_id = '{HS_JOB_DTL_ID}'
               """.format(MOD_DT=self.now_datetime,HS_JOB_DTL_ID=hs_job_dtl_id)
        print query
        try:
            self.dbms.queryExec(query)
        except:
            pass

        # query = """UPDATE store.hs_job_mst
        #             SET job_stt_dt='{JOB_STT_DT}',
        #             job_end_dt='{JOB_END_DT}'
        # 	    WHERE tg_job_mst_id= '{MST_ID}'
        # 	    """.format(JOB_STT_DT=job_stt_dt, JOB_END_DT=job_end_dt, MST_ID=mst_id)
        # print query
        # try:
        #     self.dbms.queryExec(query)
        # except:
        #     pass

    def main(self):
        job_scheduler.sched().already_past_job()

if __name__=='__main__':
    ibrm_job_stat().main()


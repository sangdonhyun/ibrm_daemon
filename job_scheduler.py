# -*- coding: utf-8 -*-
import ibrm_dbms
import datetime
import os
import ibrm_daemon_send
import ConfigParser
import time
import ibrm_logger
import job_state
import psutil
import job_overtime_monitor

log = ibrm_logger.ibrm_logger().logger('ibrm_server_sched')


class sched():
    def __init__(self):
        self.db = ibrm_dbms.fbrm_db()
        self.cfg = self.get_cfg()
        self.job_prc = job_state.ibrm_job_stat()
        self.ov_monitor = job_overtime_monitor.ov_mon()

    def already_past_job(self):
        dt = datetime.datetime.now() - datetime.timedelta(minutes=5)
        dt_str = dt.strftime('%H%M')
        query = """
        SELECT 
  tjd.job_id        
  ,CASE 
    WHEN exec_time::time >= (NOW() - INTERVAL '5 MINUTE')::TIME THEN 'Y'
    WHEN exec_time::time < (NOW() - INTERVAL '5 MINUTE')::TIME THEN 'N'
    ELSE 'N'      
   END AS EXEC_YN  
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
  AND NOT EXISTS (
      SELECT 1 
      FROM 
        store.hs_job_dtl hjd 
      WHERE 
        hjd.tg_job_mst_id = tjm.tg_job_mst_id 
        AND hjd.tg_job_dtl_id = tjd.tg_job_dtl_id 
  )
  AND tjm.job_exec_dt = to_char(now(), '20201106') -- 실행일자로 변경하여 사용   

  and mj.exec_time  < '{DATETIME}'
        """.format(DATETIME=dt_str)
        print query
        ret = self.db.getRaw(query)
        for job in ret:
            print job
            job_id = job[0]
            memo = 'PASSED BY SCHEDULER'
            print job_id
            self.job_prc.job_fail_proc(job_id, memo)

    def get_cfg(self):
        cfg = ConfigParser.RawConfigParser()
        cfg_name = os.path.join('config', 'config.cfg')
        cfg.read(cfg_name)
        return cfg

    def get_job(self):


        odate = self.get_odate_1()
        today_str = self.get_odate()
        #today_str = datetime.datetime.now().strftime('%Y%m%d')
        sql = """SELECT 
   tgrun.tg_job_mst_id
  ,tgrun.job_exec_dt
  ,tgrun.tg_job_dtl_id
  ,tgrun.run_type
    ,tgrun.target_yn
   ,tgrun.job_stat
   ,tgrun.job_nm
  ,tgrun.rel_exec_type 
  ,tgrun.pre_job_id 
  ,tgrun.post_job_id
  ,tgrun.exec_time
  ,tgrun.timeout
  ,tgrun.alarm_yn
  ,tgrun.svr_nm
  ,tgrun.ip_addr
  ,tgrun.db_nm
  ,tgrun.back_type
  ,tgrun.sh_file_nm
  ,tgrun.sh_path
  ,tgrun.ora_sid
  ,tgrun.ora_home
  ,tgrun.db_name
  ,tgrun.job_id 
  ,tgrun.alarm_tg
FROM 
(
  SELECT 
     tg.tg_job_mst_id 
    ,tg.job_exec_dt  
    ,tg.tg_job_dtl_id
    ,tg.exec_time    
    ,tg.job_stat
    ,tg.run_type     
   ,CASE 
      WHEN 
         TO_TIMESTAMP( tg.job_run_dt || tg.exec_time , 'YYYYMMDDHH24MI')  >= (  NOW() - INTERVAL '5 MINUTE'  )
        AND TO_TIMESTAMP( tg.job_run_dt || tg.exec_time , 'YYYYMMDDHH24MI')  <=   NOW()   
        AND tg.run_type ='RUN' AND tg.job_stat IS NULL
        THEN 'RUN'
      WHEN tg.run_type ='RELEASE' AND tg.job_stat IS NULL THEN 'RUN'
      WHEN tg.run_type IN ('RE-RUN') THEN 'RE-RUN'
      WHEN tg.run_type IN ('PAUSE') THEN 'PAUSE'    
      ELSE 'N'      
     END AS target_yn        
    ,mj.timeout      
    ,mj.alarm_yn     
    ,ms.svr_nm       
    ,ms.ip_addr      
    ,ms.db_nm        
    ,ms.back_type    
    ,ms.sh_file_nm   
    ,ms.sh_path      
    ,moi.ora_sid      
    ,moi.ora_home     
    ,moi.db_name        
    ,tg.job_id       
    ,mj.job_nm
    ,mj.rel_exec_type
    ,mj.pre_job_id 
    ,mj.post_job_id 
    ,mj.alarm_tg
  FROM 
    (
      SELECT
        ROW_NUMBER() OVER (
          PARTITION BY
            tjm.tg_job_mst_id
            , tjd.tg_job_dtl_id              
            , COALESCE(tjdl.tg_job_dtl_id)
            , COALESCE(hjd.hs_job_dtl_id)
          ORDER BY
            tjm.tg_job_mst_id
            , tjd.tg_job_dtl_id
            , tjdl.tg_job_dtl_log_id DESC      
            , hjd.hs_job_dtl_id DESC
        ) AS ord
        ,tjm.tg_job_mst_id 
        ,tjm.job_exec_dt
        ,tjd.job_run_dt 
        ,tjd.tg_job_dtl_id 
        ,tjd.job_id 
        ,COALESCE( tjdl.run_type , tjd.run_type ) AS run_type
        ,COALESCE( tjdl.exec_time , tjd.exec_time ) AS exec_time    
        ,hjd.job_stat
      FROM
        store.tg_job_mst tjm
        INNER JOIN 
        store.tg_job_dtl tjd 
        ON ( 
          tjd.job_exec_dt = tjd.job_exec_dt 
          AND tjd.tg_job_mst_id = tjm.tg_job_mst_id
        )
        LEFT OUTER JOIN   
        store.tg_job_dtl_log tjdl
        ON ( 
          tjdl.job_exec_dt = tjm.job_exec_dt 
          AND tjdl.tg_job_mst_id = tjd.tg_job_mst_id
          AND tjdl.tg_job_dtl_id = tjd.tg_job_dtl_id
        )
        LEFT OUTER JOIN 
        store.hs_job_dtl hjd 
        ON (
            hjd.job_exec_dt = tjm.job_exec_dt 
            AND hjd.tg_job_mst_id = tjm.tg_job_mst_id 
            AND hjd.tg_job_dtl_id = tjd.tg_job_dtl_id                     
            AND tjdl.tg_job_dtl_id = hjd.tg_job_dtl_id 
        )
      WHERE 
      tjm.job_exec_dt >= '{YYYYMMDD}' 
    ) tg  
    INNER JOIN master.mst_job mj 
      ON mj.job_id = tg.job_id
    INNER JOIN master.mst_shell ms 
      ON ms.sh_id = mj.sh_id
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
    tg.ord =1    
) tgrun
WHERE 
    tgrun.target_yn <> 'N'
                        """.format(YYYYMMDD=odate,TODAY=today_str)
        # print sql
        ret = self.db.getRaw(sql)
        job_list = []
        for job in ret:
            job_info = {}
            """
          0	tgrun.tg_job_mst_id
            1	,tgrun.job_exec_dt
            2	,tgrun.tg_job_dtl_id
            3	,tgrun.run_type
            4	  ,tgrun.target_yn
            5	 ,tgrun.job_stat
            6	 ,tgrun.job_nm
            7	,tgrun.rel_exec_type 
            8	,tgrun.pre_job_id 
            9	,tgrun.post_job_id
            10	,tgrun.exec_time
            11	,tgrun.timeout
            12	,tgrun.alarm_yn
            13	,tgrun.svr_nm
            14	,tgrun.ip_addr
            15	,tgrun.db_nm
            16	,tgrun.back_type
            17	,tgrun.sh_file_nm
            18	,tgrun.sh_path
            19	,tgrun.ora_sid
            20	,tgrun.ora_home
            21	,tgrun.db_name
            22	,tgrun.job_id
            23  ,tgrun.alarm_tg

            """
            job_info['tg_job_mst_id'] = job[0]
            job_info['job_exec_dt'] = job[1]
            job_info['tg_job_dtl_id'] = job[2]
            job_info['run_type'] = job[3]
            job_info['target_yn'] = job[4]
            job_info['job_stat'] = job[5]
            job_info['job_nm'] = job[6]
            job_info['rel_exec_type'] = job[7]
            job_info['pre_job_id'] = job[8]
            job_info['post_job_id'] = job[9]
            job_info['exec_time'] = job[10]
            job_info['timeout'] = job[11]
            job_info['alarm_yn'] = job[12]
            job_info['svr_nm'] = job[13]
            job_info['svr_ip'] = job[14]
            job_info['db_nm'] = job[15]
            job_info['shell_type'] = job[16]
            job_info['shell_name'] = job[17]
            job_info['sh_path'] = job[18]
            job_info['ora_sid'] = job[19]
            job_info['ora_home'] = job[20]
            job_info['db_name'] = job[21]
            job_info['job_id'] = job[22]
            job_info['alarm_tg'] = job[23]

            job_list.append(job_info)

        return job_list
    def get_odate_1(self):
        try:
            ndate = self.cfg.get('COMMON', 'new_day_datetime')
        except:
            ndate = '0800'
        now = datetime.datetime.now()
        hm = now.strftime('%H%m')
        md = now.strftime('%d%m')
        if hm < ndate:
            odate = now - datetime.timedelta(days=2)
        else:
            odate = now - datetime.timedelta(days=1)
        return odate.strftime('%Y%m%d')

    def get_odate(self):
        try:
            ndate = self.cfg.get('COMMON', 'new_day_datetime')
        except:
            ndate = '0800'
        now = datetime.datetime.now()
        hm = now.strftime('%H%m')
        md = now.strftime('%d%m')
        if hm < ndate:
            odate = now - datetime.timedelta(days=1)
        else:
            odate = now
        return odate.strftime('%Y%m%d')

    def get_one_job(self):
        #         to_day = datetime.datetime.now().strftime('%Y%m%d')
        #         sql = """
        # SELECT
        #   tjm.tg_job_mst_id  -- 0[일작업ID] 일일 대상 작업 MST ID
        #   ,tjm.job_exec_dt   -- 1[작업실행일자] DB 일자 or SYSTEM
        #   ,tjd.tg_job_dtl_id -- 2[일작업상세ID]
        #   ,tjd.run_type      -- 3[실행유형] Run, Stop, ReRun, Skip, Force Run
        #   ,mj.exec_time      -- 4[실행시각] 0000~2359
        #
        #   ,mj.timeout        -- 5[제한시간] 작업 Timeout 시각(알람 설정 시 사용)
        #   ,mj.alarm_yn       -- 6[알림여부]
        #   ,ms.svr_nm         -- 7[서버명] 서버명
        #   ,ms.ip_addr        -- 8[IP 정보] ipv4
        #   ,ms.db_nm          -- 9[DB 명]
        #   ,ms.back_type      -- 10[백업유형] incr / arch / full / merge
        #   ,ms.sh_file_nm     -- 11[쉘 파일명] Real 파일명
        #   ,ms.sh_path        -- 12[쉘 경로] 쉘스크립트 경로
        #   ,moi.ora_sid       -- 13SID
        #   ,moi.ora_home      -- 14ORACLE HOME
        #   ,moi.db_name       -- 15DB명
        #   ,tjm.tg_job_mst_id -- 16[일작업ID] 일일 대상 작업 MST ID
        #   ,tjm.job_exec_dt   -- 17[작업실행일자] DB 일자 or SYSTEM
        #   ,tjd.tg_job_dtl_id -- 18[일작업상세ID]
        #   ,tjd.job_id        -- 19[작업ID] JOB ID Unique
        #   ,CASE
        #     WHEN mj.exec_time::time >= (NOW() - INTERVAL '5 MINUTE')::TIME THEN 'Y'
        #     WHEN mj.exec_time::time < (NOW() - INTERVAL '5 MINUTE')::TIME THEN 'N'
        #     ELSE 'N'
        #    END AS EXEC_YN
        # FROM
        #   store.tg_job_mst tjm
        #   INNER JOIN
        #   store.tg_job_dtl tjd
        #   ON (
        #       tjm.tg_job_mst_id = tjd.tg_job_mst_id
        #       AND tjd.use_yn='Y'
        #       AND tjd.run_type ='RUN'
        #     )
        #   INNER JOIN
        #   master.mst_job mj
        #   ON (
        #     mj.use_yn ='Y'
        #     AND mj.job_id = tjd.job_id
        #   )
        #   INNER JOIN
        #   master.mst_shell ms
        #   ON (
        #     ms.use_yn ='Y'
        #     AND ms.sh_id = mj.sh_id
        #   )
        #   INNER JOIN
        #   master.master_svr_info msi
        #   ON (msi.svr_id = ms.svr_id )
        #   INNER JOIN
        #   master.master_ora_info moi
        #   ON (
        #     moi.svr_id = msi.svr_id
        #     AND moi.ora_id = ms.db_id
        #   )  --order by 1 desc
        # --WHERE
        # --  tjm.use_yn ='Y'
        #  -- AND NOT EXISTS (
        #  --     SELECT 1
        #  --     FROM
        #  --       store.hs_job_dtl hjd
        #  --     WHERE
        #  --       hjd.tg_job_mst_id = tjm.tg_job_mst_id
        #  --       AND hjd.tg_job_dtl_id = tjd.tg_job_dtl_id
        #  -- )
        #   AND tjm.job_exec_dt = to_char(now(), '{YYYYMMDD}')  -- 실행일자로 변경하여 사용
        #   --AND tjm.job_exec_dt = '20201023' -- 실행일자로 변경하여 사용
        #
        # --where tjd.job_id  = 17
        # order by 5
        # """.format(YYYYMMDD=to_day)

        odate = self.get_odate()
        sql = """SELECT 
    tgrun.tg_job_mst_id
  ,tgrun.job_exec_dt
  ,tgrun.tg_job_dtl_id
  ,tgrun.run_type
  ,tgrun.exec_time
  ,tgrun.timeout
  ,tgrun.alarm_yn
  ,tgrun.svr_nm
  ,tgrun.ip_addr
  ,tgrun.db_nm
  ,tgrun.back_type
  ,tgrun.sh_file_nm
  ,tgrun.sh_path
  ,tgrun.ora_sid
  ,tgrun.ora_home
  ,tgrun.db_name
  ,tgrun.job_id
  ,tgrun.target_yn
  ,tgrun.job_stat  
FROM 
(
  SELECT 
     tg.tg_job_mst_id 
    ,tg.job_exec_dt  
    ,tg.tg_job_dtl_id
    ,tg.exec_time    
    ,tg.job_stat
    ,tg.run_type     
    ,CASE 
      WHEN tg.exec_time::time >= (NOW() - INTERVAL '5 MINUTE')::TIME AND tg.run_type IN ('RUN', 'RELEASE') AND tg.job_stat IS NULL THEN 'RUN'
      WHEN tg.run_type IN ('RE-RUN') THEN 'RE-RUN'
      WHEN tg.run_type IN ('PAUSE') THEN 'PAUSE'    
      ELSE 'N'      
     END AS target_yn        
    ,mj.timeout      
    ,mj.alarm_yn     
    ,ms.svr_nm       
    ,ms.ip_addr      
    ,ms.db_nm        
    ,ms.back_type    
    ,ms.sh_file_nm   
    ,ms.sh_path      
    ,moi.ora_sid      
    ,moi.ora_home     
    ,moi.db_name        
    ,tg.job_id       
  FROM 
    (
      SELECT
        ROW_NUMBER() OVER (
          PARTITION BY
            tjm.tg_job_mst_id
            , tjd.tg_job_dtl_id              
            , COALESCE(tjdl.tg_job_dtl_id)
            , COALESCE(hjd.hs_job_dtl_id)
          ORDER BY
            tjm.tg_job_mst_id
            , tjd.tg_job_dtl_id
            , tjdl.tg_job_dtl_log_id DESC      
            , hjd.hs_job_dtl_id DESC
        ) AS ord
        ,tjm.tg_job_mst_id 
        ,tjm.job_exec_dt
        ,tjd.tg_job_dtl_id 
        ,tjd.job_id 
        ,COALESCE( tjdl.run_type , tjd.run_type ) AS run_type
        ,COALESCE( tjdl.exec_time , tjd.exec_time ) AS exec_time    
        ,hjd.job_stat
      FROM
        store.tg_job_mst tjm
        INNER JOIN 
        store.tg_job_dtl tjd 
        ON ( 
          tjd.job_exec_dt = tjd.job_exec_dt 
          AND tjd.tg_job_mst_id = tjm.tg_job_mst_id
        )
        LEFT OUTER JOIN   
        store.tg_job_dtl_log tjdl
        ON ( 
          tjdl.job_exec_dt = tjm.job_exec_dt 
          AND tjdl.tg_job_mst_id = tjd.tg_job_mst_id
          AND tjdl.tg_job_dtl_id = tjd.tg_job_dtl_id
        )
        LEFT OUTER JOIN 
        store.hs_job_dtl hjd 
        ON (
            hjd.job_exec_dt = tjm.job_exec_dt 
            AND hjd.tg_job_mst_id = tjm.tg_job_mst_id 
            AND hjd.tg_job_dtl_id = tjd.tg_job_dtl_id                     
            AND tjdl.tg_job_dtl_id = hjd.tg_job_dtl_id 
        )
      WHERE 
      tjm.job_exec_dt >= '{YYYYMMDD}' 
    ) tg  
    INNER JOIN master.mst_job mj 
      ON mj.job_id = tg.job_id
    INNER JOIN master.mst_shell ms 
      ON ms.sh_id = mj.sh_id
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
    tg.ord =1    
) tgrun
WHERE 
    tgrun.target_yn <> 'N'
        """.format(YYYYMMDD=odate)
        # print sql
        ret = self.db.getRaw(sql)
        job_list = []
        for job in ret:

            job_info = {}
            """
            0	 tgrun.tg_job_mst_id
            1	  ,tgrun.job_exec_dt
            2	  ,tgrun.tg_job_dtl_id
            3	  ,tgrun.run_type
            4	  ,tgrun.exec_time
            5	  ,tgrun.timeout
            6	  ,tgrun.alarm_yn
            7	  ,tgrun.svr_nm
            8	  ,tgrun.ip_addr
            9	  ,tgrun.db_nm
            10	  ,tgrun.back_type
            11	  ,tgrun.sh_file_nm
            12	  ,tgrun.sh_path
            13	  ,tgrun.ora_sid
            14	  ,tgrun.ora_home
            15	  ,tgrun.db_name
            16	  ,tgrun.job_id
            17	  ,tgrun.target_yn
            """
            job_info['svr_ip'] = job[8]
            job_info['shell_type'] = job[10]
            job_info['shell_name'] = job[11]
            job_info['shell_path'] = job[12]
            job_info['ora_home'] = job[14]
            job_info['db_name'] = job[15]
            job_info['ora_sid'] = job[13]
            job_info['tg_job_mst_id'] = job[0]
            job_info['job_exec_dt'] = job[1]
            job_info['tg_job_dtl_id'] = job[2]
            job_info['job_id'] = job[16]
            job_info['job_exec_time'] = job[4]
            job_info['job_yn'] = job[17]
            job_info['job_stat'] = job[18]

            job_list.append(job_info)

        return job_list

    def job_submit(self, job_info):
        print 'JOB START'


        HOST = job_info['svr_ip']
        PORT = 53001

        ss = ibrm_daemon_send.SocketSender(HOST, PORT)

        ss.jos_excute(job_info)
        # log.info('submit job')
        # log.info(str(job_info))

    def check_date(self, exec_time):
        now = datetime.datetime.now()
        nowhm = now.strftime('%H%M')
        limit = now - datetime.timedelta(minutes=30)
        limitnw = limit.strftime('%H%M')
        if exec_time < nowhm and exec_time >= limitnw:
            return True
        else:
            return False

    def to_day_job_cnt(self):
        yyyymmdd = datetime.datetime.now().strftime('%Y%m%d')
        query = "select count(*) from store.tg_job_dtl  where job_exec_dt='{YYYYMMDD}'".format(YYYYMMDD=yyyymmdd)
        today_cnt = self.db.getRaw(query)[0][0]
        return today_cnt

    def submit_test(self):
        job = self.get_one_job()[0]
        job['shell_type'] = 'INCR'
        self.job_submit(job)

    def submit_test1(self):
        job_info = {'db_name': 'IBRM', 'tg_job_dtl_id': 445, 'svr_ip': '121.170.193.200', 'job_yn': 'Y',
                    'Run_type': 'Run', 'job_id': 73, 'shell_name': 'IBRM_Archive.sh',
                    'shell_path': '/u01/SCRIPTS/Database/IBRM/RMAN/SCHEDULE',
                    'ora_home': '/u01/app/oracle/product/18.0.0/dbhome_1', 'job_exec_time': '0925',
                    'job_exec_dt': '20201116', 'shell_type': 'ARCH', 'ora_sid': 'ibrm', 'tg_job_mst_id': 32}
        job_info['Run_type'] = 'Run'

        print 'JOB START'
        print job_info

        HOST = job_info['svr_ip']
        PORT = 53001

        ss = ibrm_daemon_send.SocketSender(HOST, PORT)
        self.job_prc.job_start_setup(job_info)
        ss.jos_excute(job_info)

    def get_today_job_msg(self):
        today = self.to_day_job_cnt()

    def get_pause_status(self,job):
        ex_bit = True
        job_id = job['job_id']
        return ex_bit

    def set_start_job_alarm(self,job):
        pass

    def main(self):

        job_list = self.get_job()
        # print job_list
        now = datetime.datetime.now()

        date_range = now - datetime.timedelta(minutes=5)
        limit_date = date_range.strftime('%H%M')
        now_date = now.strftime('%H%M')

        print '-' * 50
        print 'total job :', len(job_list)
        print 'today job :', self.to_day_job_cnt()

        for job in job_list:


            print job
            print job['job_id']
            print job['tg_job_dtl_id']
            ex_bit = (job['exec_time'] == now_date) or (
                        int(job['exec_time']) in range(int(limit_date), int(now_date)))

            print ex_bit
            if job['run_type'] in ['RE-RUN','RELEASE'] :
                ex_bit = True
                # 1> tg_job_dtl_log insert
                print job['job_id'],job['tg_job_dtl_id']
                self.job_prc.set_tg_job_dtl_log(job['job_id'],job['tg_job_dtl_id'])

                if job['run_type'] == 'RE-REUN':
                    self.job_prc.set_hs_job_dtl_udt(job['job_id'],job['tg_job_dtl_id'])
                    # hs_job_dtl update (upd_stat = 'Y', use_yn= 'N')

            if job['run_type'] == 'PAUSE':
                # ex_bit = self.get_pause_status(job)
                # tg_job_dtl_log insert
                if ex_bit:
                    self.job_prc.set_tg_job_dtl_log(job['job_id'],job['tg_job_dtl_id'])
                    # tg_job_dtl_log insert

            if job['pre_job_id'] > 0:
                print 'pre_job_id :',job['pre_job_id']
                yyyymmdd = datetime.datetime.now().strftime('%Y%m%d')
                query = """SELECT job_stat, rm_bk_stat   FROM store.hs_job_dtl where  job_exec_dt = '{YYYYMMDD}' and job_id = '{PRE_JOB_ID}' """.format(
                    YYYYMMDD=yyyymmdd, PRE_JOB_ID=job['pre_job_id'])
                print query

                ret = self.db.getRaw(query)
                if len(ret) > 0:
                    ret_set = ret[0]
                    job_stat = ret_set[0]
                    rm_bk_stat = ret_set[1]
                    print 'ret_set :',ret_set
                    if not job_stat == 'End-OK':
                        ex_bit = False
                        self.job_prc.set_pause(job['job_id'])
                    else:
                        ex_bit = True
                else:
                    ex_bit = False

            # print job['job_exec_time'],now_date
            # print range(int(limit_date),int(now_date))

            # print job['shell_name'],job['job_exec_time'],limit_date, ex_bit
            print 'ex_bit :',ex_bit
            if ex_bit:

                self.job_prc.job_start_setup(job)
                submit_job_info = {}
                submit_job_info['job_id'] = job['job_id']
                submit_job_info['shell_name'] = job['shell_name']
                submit_job_info['shell_type'] = job['shell_type']
                submit_job_info['db_name'] = job['db_name']
                submit_job_info['ora_sid'] = job['ora_sid']
                submit_job_info['tg_job_dtl_id'] = job['tg_job_dtl_id']
                submit_job_info['svr_ip'] = job['svr_ip']
                print job
                print submit_job_info
                print job['run_type']
                self.job_submit(submit_job_info)
                try:

                    self.job_submit(submit_job_info)
                    s,e,t = self.ov_monitor.get_set_status(job['tg_job_dtl_id'])
                    if s=='S':
                        self.ov_monitor.evt_send(job['tg_job_dtl_id'],'s')
                except Exception as e:
                    print str(e)

if __name__ == '__main__':
    print 'iBRM Schduller START'
    while True:
        print '=' * 50
        try:
            sched().main()
        except Exception as e:
            print str(e)

        print datetime.datetime.now()
        msg = "memory size :" + str(dict(psutil.virtual_memory()._asdict())['percent'])
        print msg
        try:
            log.info(msg)
        except Exception as e:
            print str(e)
        time.sleep(30)

    # sched().already_past_job()


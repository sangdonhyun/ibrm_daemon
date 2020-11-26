import os
import time
import datetime
import logging
loggers = {}
class ibrm_logger :

    def logger(self,name='ibrm_srver_log'):
        print 'name : ',name
        # if a logger exists, return that logger, else create a new one
        global loggers

        if name in loggers.keys():
            return loggers[name]
        else:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            now = datetime.datetime.now()
            handler = logging.FileHandler(os.path.join('logs','ibrm_server_log_'+ now.strftime("%Y-%m-%d") +'.log'))
            formatter = logging.Formatter("%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            loggers.update(dict(name=logger))
            return logger

if __name__=='__main__':

    for i in range(10):
        s = ibrm_logger().logger('ibrm_server_log')
        s.info("Info%s"%i)
        print 'loggers :',loggers

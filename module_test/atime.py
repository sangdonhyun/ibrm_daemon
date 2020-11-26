import datetime
import time
import glob
import os

slist=glob.glob('*.py')
print slist

for s in slist:
    a_time =  time.ctime(os.path.getatime(s))
    c_time = time.ctime(os.path.getatime(s))
    m_time = time.ctime(os.path.getatime(s))
    atime_obj = datetime.datetime.strptime(a_time,'%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
    ctime_obj = datetime.datetime.strptime(c_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
    mtime_obj = datetime.datetime.strptime(m_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')

    print atime_obj
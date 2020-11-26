#-*- coding: utf-8 -*-

from flask import Flask
import glob
import os
import time
import datetime
app = Flask(__name__)
shell_path=os.path.join('C:\PycharmProjects','ibrm_daemon','SHELL')

@app.route('/shell_list')
def shell_list():

    pylist=glob.glob(os.path.join(shell_path,'*.sh'))
    shell_list=[]
    for s in pylist:

        shell_dict={}
        name = os.path.basename(s)
        a_time = time.ctime(os.path.getatime(s))
        c_time = time.ctime(os.path.getatime(s))
        m_time = time.ctime(os.path.getatime(s))
        atime_obj = datetime.datetime.strptime(a_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
        ctime_obj = datetime.datetime.strptime(c_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
        mtime_obj = datetime.datetime.strptime(m_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
        shell_dict['name'] = name
        shell_dict['a_time'] = atime_obj
        shell_dict['c_time'] = ctime_obj
        shell_dict['m_time'] = mtime_obj
        shell_list.append(shell_dict)
    return {'shell_list':shell_list}


@app.route('/shell/<shell_name>')
def hello_user(shell_name):

    with open(os.path.join(shell_path,shell_name)) as f:
        shell_detail = f.read()

    return {'shell_detail':shell_detail}


if __name__ == "__main__":
    app.run(host="121.170.193.196",port=53002)

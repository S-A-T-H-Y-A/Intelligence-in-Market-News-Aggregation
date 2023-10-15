# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 23:05:35 2020

@author: prady
"""

from ftplib import FTP 
import os
import fileinput
import schedule
import time
def loop():
        config_host='ftp.rasoftwares.com'
        config_username='news@news.rablion.com'
        config_password='RA@4231'
        config_port=21
        config_local_folder = 'F:/flaskapp/newsaggV1/index.html'
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(config_host, config_port) 
        ftp.login(config_username, config_password)
        ftp.cwd('/')
        fileName = config_local_folder
        fp = open(fileName, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(fileName), fp, 1024)
        fp.close()

schedule.every(5).minutes.do(loop)
while 1:
    schedule.run_pending()
    time.sleep(1)  

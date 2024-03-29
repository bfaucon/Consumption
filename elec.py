#!/usr/bin/python
# -*- coding: utf-8 -*-
 
#=========================================================================
#              elec.py
#-------------------------------------------------------------------------
# Original sources by JahisLove - 2014, june
# version 0.1 2014-06-16
#-------------------------------------------------------------------------
# Modifications done by Bruno Faucon - 2015, Augustus
# version 0.2 2015-08-21
#-------------------------------------------------------------------------
# Modifications done by Bruno Faucon - 2018, Augustus
# version 0.3 2018-01-28#
# Add a 3rd counter for Wash machines.
#-------------------------------------------------------------------------
# This script read the counter on 1 s2423 on the 1wire
# compare the old values to the new one and save the values in a MySQL database
# this also calculate if we are in night or day mode.
#
# tested with python on Raspberry pi distribution: Raspbian GNU/Linux 7 (wheezy) 
# and Server Apache/2.2.22 (Debian) MySQL: 5.5.43
#-------------------------------------------------------------------------
# CREATE TABLE IF NOT EXISTS `PiElec` (
#  `id` int(11) NOT NULL AUTO_INCREMENT,
#  `date` datetime NOT NULL,
#  `HP1` decimal(10,2) DEFAULT NULL,
#  `HC1` decimal(10,2) DEFAULT NULL,
#  `HP2` decimal(10,2) DEFAULT NULL,
#  `HC2` decimal(10,2) DEFAULT NULL,
#  PRIMARY KEY (`id`),
#  KEY `date` (`date`)
#  ) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23346 ;
# ;
# 
#===================================================================
 
#----------------------------------------------------------#
#             package importation                          #
#----------------------------------------------------------#
import os
import time
import datetime
import MySQLdb   # MySQLdb must be installed by yourself
from threading import Timer
#import sqlite3
 
#-----------------------------------------------------------------#
#  constants : use your own values / utilisez vos propres valeurs #
#-----------------------------------------------------------------#
PATH_THERM = "/home/pi/consumption/" #path to this script
PATH_LOG = "/home/pi/consumption/log" #path to this script

DB_SERVER ='192.168.2.10'  # MySQL : IP server (localhost if mySQL is on the same machine)
DB_USER='conso'     # MySQL : user
DB_PWD='********************'            # MySQL : password
DB_BASE='consumption'     # MySQL : database name
DB_PORT=3307

 
# vous pouvez ajouter ou retirer des sondes en modifiant les 5 lignes ci dessous
# ainsi que la derniere ligne de ce script : querydb(....
counter1 = "/mnt/1wire/1D.C5600F000000/counter.A"
counter2 = "/mnt/1wire/1D.C5600F000000/counter.B"
counter3 = "/mnt/1wire/1D.B2D50D000000/counter.A"
counter4 = "/mnt/1wire/1D.B2D50D000000/counter.B"
counters = [counter1, counter2, counter3, counter4]
counter_value = [0, 0, 0, 0]
old1 = "/home/pi/consumption/oldcountA"
old2 = "/home/pi/consumption/oldcountB"
old3 = "/home/pi/consumption/oldcountE"
old4 = "/home/pi/consumption/oldcountF"
olds = [old1, old2, old3, old4]
old_value = [0, 0, 0, 0]
 
#----------------------------------------------------------#
#             Variables                                    #
#----------------------------------------------------------#

#----------------------------------------------------------#
#     definition : database query                          #
#----------------------------------------------------------#
def query_db(sql):
    db = MySQLdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_BASE, DB_PORT)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close() 

#----------------------------------------------------------#
#     definition : new query for sonde                     #
#----------------------------------------------------------#
def read_counter(counter):
    try:
        f = open(counter, 'r')
        lines = f.readlines()
        f.close()
        c = int(lines[0])
    except:
        print "Elec Counter not reachable please take action"
        c = '0'
    finally:
        return c

#----------------------------------------------------------#
#     definition : calculate delta between old and new     #
#                  counter                                 #
#----------------------------------------------------------#
def get_delta(counter,newvalue):
    try:
        delta = 0
        if not os.path.exists(counter):
           target = open(counter, 'w')
           target.write(str(newvalue))
           target.close()
           delta = newvalue 
        else:
           target = open(counter, 'r')
           lines = target.readlines()
           oldvalue = int(lines[0])
           target.close()
           target = open(counter, 'w+')
           target.write(str(newvalue))
           target.close()
           delta = newvalue - oldvalue 
    except:
        print "issue with delta calculation"
        return '0'
    finally:
        return delta

#----------------------------------------------------------#
#             code principal                               #
#----------------------------------------------------------#
 
# initialize Raspberry GPIO and DS18B20
#os.system('sudo /sbin/modprobe w1-gpio')
#os.system('sudo /sbin/modprobe w1-therm')
#time.sleep(2)

d1 = datetime.datetime.now()
d2 = d1.replace(minute=5*(d1.minute // 5))
startHP = d2.replace(hour=07, minute=02, second=0, microsecond=0)
startHC = d2.replace(hour=22, minute=02, second=0, microsecond=0)
datebuff = d2.strftime('%Y-%m-%d %H:%M:00') #formating date for mySQL
 
for (i, counter) in enumerate(counters):
    newvalue = read_counter(counter)
    delta = get_delta(olds[i],newvalue)
    counters[i] = delta
# ecriture dans la base
if (d2.weekday() >= 5) or (d2 < startHP) or (d2 > startHC):
    sql="INSERT INTO PiElec (date, HC1, HP1, HC2, HP2, HC3, HP3, HC4, HP4) VALUES ('" + datebuff + "','" + str(counters[0]) + "','0','"+ str(counters[1]) + "','0','"+ str(counters[2]) + "','0','"+ str(counters[3]/2) + "','0')"
else:
    sql="INSERT INTO PiElec (date, HP1, HC1, HP2, HC2, HP3, HC3, HP4, HC4) VALUES ('" + datebuff + "','" + str(counters[0]) + "','0','"+ str(counters[1]) + "','0','"+ str(counters[2]) + "','0','"+ str(counters[3]/2) + "','0')"
query_db(sql) # on INSERT dans la base


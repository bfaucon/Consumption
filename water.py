#!/usr/bin/python
# -*- coding: utf-8 -*-
 
#=========================================================================
#              water.py
#-------------------------------------------------------------------------
# by JahisLove - 2014, june
# version 0.1 2014-06-16
# Modifications done by Bruno Faucon - 2020
# version 0.3 2020-05-06
# connection au sql synology
# version 0,4 2022-04-20
# Cleaning code
#-------------------------------------------------------------------------
# Script reading value of 2 1Wire counter linked to RaspberryPi and save in MySQL
#-------------------------------------------------------------------------
#
# Table in database must have this structure
#
# CREATE TABLE `PiWater` (
#  `id` int(11) NOT NULL AUTO_INCREMENT,
#  `date` datetime NOT NULL,
#  `W1` decimal(3,1) NOT NULL, 
#  `W2` decimal(3,1) NOT NULL,
#  PRIMARY KEY (`id`)
#) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
#
# W1 = Eau froide seule
# W2 = Eau Chaude seule 
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
DB_PWD='**********'            # MySQL : password
DB_BASE='consumption'     # MySQL : database name
DB_PORT=3307     # MySQL : database port


# vous pouvez ajouter ou retirer des sondes en modifiant les 5 lignes ci dessous
# ainsi que la derniere ligne de ce script : querydb(....
counter1 = "/mnt/1wire/1D.AEB40D000000/counter.A"
counter2 = "/mnt/1wire/1D.AEB40D000000/counter.B"
counters = [counter1, counter2]
counter_value = [0, 0]
old1 = "/home/pi/consumption/oldcountC"
old2 = "/home/pi/consumption/oldcountD"
olds = [old1, old2]
old_value = [0, 0]
 
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
        print "Water Counter not reachable please take action"
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
#             Primary Code                                 #
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
#    print newvalue
#    print olds[i]
    delta = get_delta(olds[i],newvalue)
    counters[i] = delta
#ecriture dans la base
sql="INSERT INTO PiWater (date, W1, W2) VALUES ('" + datebuff + "','" + str(counters[0]) + "','"+ str(counters[1]) + "')"
#sql="INSERT INTO PiWater (date, W1, W2) VALUES ('" + datebuff + "','" + str(counters[0]) + "','0')"

#print (sql)
query_db(sql) # on INSERT dans la base


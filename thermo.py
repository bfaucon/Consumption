#!/usr/bin/python
# -*- coding: utf-8 -*-
 
#=========================================================================
#              thermo.py
#-------------------------------------------------------------------------
# Original sources by JahisLove - 2014, june
# version 0.1 2014-06-16
#-------------------------------------------------------------------------
# Modifications done by Bruno Faucon - 2015, Augustus
# version 0.2 2015-08-21
#-------------------------------------------------------------------------
# This script read the temperatures of 3 ds18b20 probes on the 1wire
# and save the values in a MySQL database
#
#
# tested with python on Raspberry pi distribution: Raspbian GNU/Linux 7 (wheezy) 
# and Server Apache/2.2.22 (Debian) MySQL: 5.5.43
#-------------------------------------------------------------------------#
# la base de données doit avoir cette structure:
#CREATE TABLE `PiTemp` (
#  `id` int(11) NOT NULL AUTO_INCREMENT,
#  `date` datetime NOT NULL,
#  `sonde1` decimal(3,1) NOT NULL,
#  `sonde2` decimal(3,1) NOT NULL,
#  `sonde3` decimal(3,1) NOT NULL,
#  PRIMARY KEY (`id`)
#) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;
 
#===================================================================
 
#----------------------------------------------------------#
#             package importation                          #
#----------------------------------------------------------#
import os
import time
import datetime
import MySQLdb   # MySQLdb must be installed by yourself
#import sqlite3
 
#-----------------------------------------------------------------#
#  constants : use your own values / utilisez vos propres valeurs #
#-----------------------------------------------------------------#
PATH_THERM = "/home/pi/consumption/" #path to this script
PATH_LOG = "/home/pi/consumption/log" #path to this script
DB_SERVER ='localhost'  # MySQL : IP server (localhost if mySQL is on the same machine)
DB_USER='root'     # MySQL : user
DB_PWD='Kate0130'            # MySQL : password
DB_BASE='consumption'     # MySQL : database name
 
# vous pouvez ajouter ou retirer des sondes en modifiant les 5 lignes ci dessous
# ainsi que la derniere ligne de ce script : querydb(....
sonde1 = "/mnt/1wire/28.C7C65D060000/temperature"
sonde2 = "/mnt/1wire/28.B83370060000/temperature"
sonde3 = "/mnt/1wire/28.0CCA5D060000/temperature"
sondes = [sonde1, sonde2, sonde3]
sonde_value = [0, 0, 0]
 
#----------------------------------------------------------#
#             Variables                                    #
#----------------------------------------------------------#
backup_row = 0
backup_mode = 0

#----------------------------------------------------------# 
def query_db(sql):
    global backup_mode
    global backup_row
    db = MySQLdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_BASE) 
    cursor = db.cursor() # creation du curseur
    if backup_mode == 0:
        cursor.execute(sql) #execution de la requete
        db.commit()
        db.close() 

#----------------------------------------------------------#
def read_file(sonde):
    try:
        f = open(sonde, 'r')
        lines = f.readlines()
        f.close()
    except:
        print "Temp Probe not reachable please take action"
        lines = '0'        
    finally:
        return lines 

#----------------------------------------------------------#
#             code principal                               #
#----------------------------------------------------------#
 
d1 = datetime.datetime.now()
d2 = d1.replace(minute=5*(d1.minute // 5))
datebuff = d2.strftime('%Y-%m-%d %H:%M:00') #formating date for mySQL
 
for (i, sonde) in enumerate(sondes):
    lines = read_file(sonde)
    sonde_value[i] = round(float(lines[0]),2)


 
#ecriture dans la base
query_db("""INSERT INTO PiTemp (date, sonde1, sonde2, sonde3) VALUES ('%s','%s','%s','%s')
         """ % (datebuff, sonde_value[0], sonde_value[1], sonde_value[2]))


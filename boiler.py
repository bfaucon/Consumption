#!/usr/bin/python
# -*- coding: utf-8 -*-
 
#=========================================================================
#              boiler.py
#-------------------------------------------------------------------------
# by Bruno Faucon - 201, june
# version 0.1 2015-06-18
#-------------------------------------------------------------------------
#
#-------------------------------------------------------------------------
#
#===================================================================
 
#----------------------------------------------------------#
#             package importation                          #
#----------------------------------------------------------#
import os
import time
import datetime
import MySQLdb   # MySQLdb must be installed by yourself
import RPi.GPIO as GPIO
from threading import Timer
 
#-----------------------------------------------------------------#
#  constants : use your own values / utilisez vos propres valeurs #
#-----------------------------------------------------------------#
PATH_THERM = "/home/pi/consumption/" #path to this script
PATH_LOG = "/home/pi/consumption/log" #path to this script
DB_SERVER ='localhost'  # MySQL : IP server (localhost if mySQL is on the same machine)
DB_USER='root'     # MySQL : user
DB_PWD='Kate0130'            # MySQL : password
DB_BASE='consumption'     # MySQL : database name
STATE = 0     # conteint RED_LED ou GREEN_ en fonction de la LED Actuellement allumée
LOG_LEVEL = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
BOILER = 21
GPIO.setup(BOILER, GPIO.OUT)


#----------------------------------------------------------#
#             Variables                                    #
#----------------------------------------------------------#

#----------------------------------------------------------#
#     definition : database query                          #
#----------------------------------------------------------#
def query_db(sql):
    db = MySQLdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_BASE)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    row = cursor.fetchone()
    result = row[0]
    cursor.close
    db.close() 
    return result

def IsHolidays():
    sql = "select count(*) as H from PiBoilerHollidays where start <= current_date and end >= current_date"
    result = query_db(sql)
    return result

def IsOn():
    sql = "SELECT count(*) FROM `PiBoilerProg` WHERE day = weekday(current_date())+1 AND start <= current_time and end >= current_time"
    result = query_db(sql)
    return result

def IsForced():
    sql  = "SELECT count(*) FROM `PiBoilerProg` WHERE day = 0 AND start <= current_time and end >= current_time"
    result = query_db(sql) 
    return result

def EraseForced():
    sql  = "Delete FROM `PiBoilerProg` WHERE day = 0"
    db = MySQLdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_BASE)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close
    db.close()

def PrintLog(log):
    global LOG_LEVEL  
    if LOG_LEVEL == 1:
      print log

#----------------------------------------------------------#
#             code principal                               #
#----------------------------------------------------------#
 
#ecriture dans la base
if (IsForced() == 1):
    PrintLog('BOILER FORCED')
    GPIO.output(BOILER, True)
elif (IsHolidays() == 1):
    PrintLog('Holidays')
    PrintLog('BOILER OFF')
    GPIO.output(BOILER, False)
    PrintLog('Errase Forcing')
    EraseForced()
elif (IsOn() == 1):
    PrintLog('BOILER ON')
    GPIO.output(BOILER, True)
else:
    PrintLog('BOILER OFF')
    GPIO.output(BOILER, False)
    PrintLog('Errase Forcing')
    EraseForced()
   

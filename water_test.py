#!/usr/bin/python
# -*- coding: utf-8 -*-
 
#=========================================================================
#              water_test.py
#-------------------------------------------------------------------------
# by JahisLove - 2014, june
# version 0.1 2014-06-16
# Modifications done by Bruno Faucon - 2020
# version 0.3 2020-05-06
# connection au sql synology
# Modifications done by Bruno Faucon - 2022
# version 0.4 2022-04-20
# test console + Email for alerting
#-------------------------------------------------------------------------
# Script checking the water consumption in last interval of time.
# If greeter than treashold, then send an Email for warning
#
# tested with python 2.7 on Raspberry pi (wheezy) and MariaDB 5.5.34 on NAS Synology DS411J (DSM 5)
#
#-------------------------------------------------------------------------
#
# la base de données doit avoir cette structure:
# CREATE TABLE `PiWater` (
#  `id` int(11) NOT NULL AUTO_INCREMENT,
#  `date` datetime NOT NULL,
#  `W1` decimal(3,1) NOT NULL,
#  `W2` decimal(3,1) NOT NULL,
#  PRIMARY KEY (`id`)
#) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
 
#===================================================================
 
#----------------------------------------------------------#
#             package importation                          #
#----------------------------------------------------------#
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
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
DB_PWD='*************'            # MySQL : password
DB_BASE='consumption'     # MySQL : database name
DB_PORT=3307     # MySQL : database port
EMAIL_SMTP='smtp.famillefaucon.be'
EMAIL_PORT=587
EMAIL_LOGIN='brfa@famillefaucon.be'
EMAIL_PWD='lufa45mail'
EMAIL_FROM='rpi@one2care.be'
EMAIL_TO='bruno.faucon@one2care.be'
ALERT_LIMIT = 100 
ALERT_TIME = 10

#----------------------------------------------------------#
#             Variables                                    #
#----------------------------------------------------------#
conso=0.00

#----------------------------------------------------------#
#     definition : database query                          #
#----------------------------------------------------------#
def query_db(sql):
    db = MySQLdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_BASE, DB_PORT)
    cursor = db.cursor()
    cursor.execute(sql)
    a = cursor.fetchone()  
    t = int(a[0])
    return t
    db.close() 

#----------------------------------------------------------#
#     Send Email                                           #
#----------------------------------------------------------#
def send_mail(EMAIL_SUBJECT, EMAIL_TEXT, EMAIL_TO):
   #print "send mail"
   msg = MIMEMultipart()
   msg['From'] = 'rpi@one2care.be'
   msg['To'] = EMAIL_TO
   msg['Subject'] = EMAIL_SUBJECT
   message = EMAIL_TEXT
   msg.attach(MIMEText(message))
   mailserver = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
   mailserver.ehlo()
   mailserver.starttls()
   mailserver.ehlo()
   mailserver.login(EMAIL_LOGIN, EMAIL_PWD)
   mailserver.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
   mailserver.quit()



#----------------------------------------------------------#
#     Primary code                                         #
#----------------------------------------------------------#
#Lecture de la consommation sur le dernier intervale
sql="SELECT sum(W1) as W1 FROM `PiWater` WHERE date > NOW() - INTERVAL " + str(ALERT_TIME) + " MINUTE"
#print (sql)
conso = query_db(sql)
# test forcer conso = ALERT_LIMIT + 10
#print conso
if conso > ALERT_LIMIT:
   #print "Alerte consommation d'eau"
   EMAIL_SUBJECT = "ALerte consommation d'eau"
   #print EMAIL_SUBJECT
   EMAIL_TEXT = "La consommation sur les 15 denrieres minutes est anormales (" + str(conso) + "L), merci de verifier s'il n'y a pas un robinet ouvert."
   #print EMAIL_TEXT
   EMAIL_TO = "bruno.faucon@one2care.be"
   #print EMAIL_TO
   a = send_mail(EMAIL_SUBJECT, EMAIL_TEXT, EMAIL_TO)



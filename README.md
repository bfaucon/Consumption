=========================================================================
              consumption
-------------------------------------------------------------------------
 by Bruno Faucon - 2015, Augustus
 version 0.3 2015-08-21
-------------------------------------------------------------------------
 This project aims to monitor water, electricity and temperature in a 
 house using a raspberry py and some probes connected via 1wire 

 Temperature 19 May 2015
 DS18B20

 Electricity consumption 31 May 2015
 probe: DS2423 counter 1 wire buy on hobby board 
 http://www.hobby-boards.com/store/products.php?product=Dual-Counter

 3nd adding water consumption 07 Aug 2015
 pulse probe by on http://www.compteur-energie.com/`

 Adding Nest temperature Dec 2015
 
#-------------------------------------------------------------------------
# Install Raspberry
#-------------------------------------------------------------------------
start with raspberry pi
http://blog.idleman.fr/tutoriel-02-brancher-et-installer-le-raspberry-pi/

configure Wlan & Ethernet
sudo nano /etc/network/interfaces

#-------------------------------------------------------------------------
# Configure Dynhost
#-------------------------------------------------------------------------
Copy all directory for DynHost dans /home/pi
changer les droits: 
		chmod -c 775 dynhost.sh
		chmod -c 775 dynhost.s

Install Lynx
		sudo apt-get install linx
Automate the script to run every 5 Minutes…
sudo crontab -e
	Add lines:

#-------------------------------------------------------------------------
# Date automation
#-------------------------------------------------------------------------
sudo apt-get install ntpdate
Automate the script to run every hour…
sudo crontab -e
	add lines

#-------------------------------------------------------------------------
# Configure OWFS
#-------------------------------------------------------------------------

https://www.abelectronics.co.uk/owfs-and-compi/info.aspx
Start OWFS at the boot of Raspberry:
I have file /etc/init.d/onewire. It contains:
#!/bin/sh
mkdir /media/1wire
/opt/owfs/bin/owfs --allow_other -u /media/1wire

make it executable: chmod a+x onewire

and to make it start on startup, then do:
update-rc.d onewire defaults

		sudo /opt/owfs/bin/owfs --i2c=ALL:ALL --allow_other /mnt/1wire/

#-------------------------------------------------------------------------
# Changing security to be done.
#-------------------------------------------------------------------------
http://www.penguintutor.com/linux/raspberrypi-webserver

#-------------------------------------------------------------------------
# configure apache, php et mysql
#-------------------------------------------------------------------------
http://www.tropfacile.net/doku.php/raspberry-pi/comment-installer-un-serveur-web-lamp
+ sudo apt-get install mysql-server python-mysqldb
	
#-------------------------------------------------------------------------
# Reading Temperature
#-------------------------------------------------------------------------
Copier thermo.py
chmod -c 775 thermotest.py
Adapter les adresse des capteurs température
Tester 


		sudo apt-get install apache2 php5 mysql-server libapache2-mod-php5 php5-mysql

#-------------------------------------------------------------------------
# Installer Raspcontrol
#-------------------------------------------------------------------------
http://www.tropfacile.net/doku.php/raspberry-pi/comment-monitorer-son-raspberry

#-------------------------------------------------------------------------
# Backup SD
#-------------------------------------------------------------------------
Install RSYNC
sudo apt-get install rsync
install ntfs
sudo apt-get install ntfs-3g 
list disk:
sudo fdisk -l

install rpi-clone
http://www.framboise314.fr/clonez-la-carte-sd-de-votre-raspberry-pi/
sudo wget https://github.com/billw2/rpi-clone/archive/master.zip
unzip master.zip
		cd rpi-clone-master
		sudo cp rpi-clone /usr/local/sbin

		sudo rpi-clone sda


#-------------------------------------------------------------------------
# custom http 404
#-------------------------------------------------------------------------
#edit .htaccess
sudo nano localized-error-pages
adding link to error page
reload config:
		sudo /etc/init.d/apache2 reload

#-------------------------------------------------------------------------
# install Mail
#-------------------------------------------------------------------------
http://www.sbprojects.com/projects/raspberrypi/exim4.php
	sudo apt-get install ssmtp mailutils mpack
Now edit the file /etc/ssmtp/ssmtp.conf as root and add the next lines. Please note that some of the lines already exist and may need to be changed. Others don't exist yet and need to be added to the end of the file. 
Testing
mail -s "This is the subject line" someone@example.com < body.txt  cat body.txt | mail -s "This is the subject line" someone@example.com


#-------------------------------------------------------------------------
# install Nest Library
#-------------------------------------------------------------------------
http://www.smbaker.com/a-python-api-for-the-nest-learning-thermostat
https://github.com/smbaker/pynest

Adding crontab
4,9,14,19,24,29,34,39,44,49,54,59 * * * * python /home/pi/pynest/nest_brfa.py --user bruno@famillefaucon.be --password Kate013. curtemp >/home/pi/pynest/temp
*/5 * * * * python /home/pi/pynest/nest_brfa.py --user bruno@famillefaucon.be --password Kate013. save
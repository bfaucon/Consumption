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
iface lo inet loopback
#iface eth0 inet dhcp
iface eth0 inet static
address 192.168.2.11
netmask 255.255.255.0
gateway 192.168.2.1

#allow-hotplug wlan0
#iface wlan0 inet manual
#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet dhcp

allow-hotplug wlan0
iface wlan0 inet static
address 192.168.2.12
netmask 255.255.255.0
gateway 192.168.2.1

wpa-ssid "WiFi-2.4-b97a"
#wpa-ssid "devolo-rdc"
wpa-psk "366A3E94DD"

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

#Check IP every 5 minutes and update dns ovh in case of change.
*/5 * * * * /home/pi/DynHost/dynhost.sh

#-------------------------------------------------------------------------
# Date automation
#-------------------------------------------------------------------------
sudo apt-get install ntpdate
Automate the script to run every hour…
sudo crontab -e
	add lines
#Update Time Every hours
0 */1 * * * ntpdate -u pool.ntp.org

#-------------------------------------------------------------------------
# Configure OWFS
#-------------------------------------------------------------------------

You first need to activate I2C in raspi-config
sudo raspi-config
Go to 
8 Advanced Options           Configure advanced settings
Go to 
A7 I2C 
Enable I2C.

Install from https://www.abelectronics.co.uk/owfs-and-compi/info.aspx

Modules: Ensure that the i2c-bus module is not included in the blacklist file:
sudo nano /etc/modprobe.d/raspi-blacklist.conf
You need to add “#” before this line: blacklist i2c-bcm2708
Save your changes Ensure that the i2c-dev module is included in /etc/modules
sudo nano /etc/modules
Add "i2c-dev" on it's own row in the file and save your changes.
Installation of the OWFS (One Wire File System) First you need to install the following packages:
sudo apt-get update
sudo apt-get install automake autoconf autotools-dev gcc-4.7 libtool libusb-dev libfuse-dev swig python2.6-dev tcl8.4-dev php5-dev i2c-tools
If promoted answer Yes on any questions during the install. Download the latest version of OWFS to your usr/src directory
cd /usr/src
sudo wget -O owfs-latest.tgz http://sourceforge.net/projects/owfs/files/latest/download
Unpack with the following command:
sudo tar xzvf owfs-latest.tgz
Next you must configure OWFS: (replace X.XXXX with the version number you downloaded)
cd owfs-X.XXXX
sudo ./configure
If everything is correct, you should get a result like this:
Current configuration: Deployment location: /opt/owfs Compile-time options: Caching is enabled USB is DISABLED
etc.
Next you need to compile OWFS which will take approx. 30 minutes with the following command:
sudo make
Next install OWFS which will take a few minutes
sudo make install
Once the installation has completed you need to create a mountpoint for the 1wire folder:
sudo mkdir /mnt/1wire
In order to use the 1wire devices without root privileges you have to change the FUSE settings, edit the fuse configuration file with:
sudo nano /etc/fuse.conf
Update this line: #user_allow_other and remove the # from the start, then save your changes
You can now start using OWFS to access your i2c devices and any connected sensors:
sudo /opt/owfs/bin/owfs --i2c=ALL:ALL --allow_other /mnt/1wire/
Using a terminal window navigate to the /mnt/1wire/ directory and use the ls command to list all connected devices.
If you have a temperature sensor connected you should have a folder starting with 10.xxxxxx
cd into this folder and then enter cat temperature to read the temperature of the sensor.

Start OWFS at the boot of Raspberry:

I have file /etc/init.d/onewire. It contains:
#!/bin/sh
mkdir /media/1wire
/opt/owfs/bin/owfs --allow_other -u /media/1wire

make it executable: chmod a+x onewire

and to make it start on startup, then do:
update-rc.d onewire defaults

		sudo /opt/owfs/bin/owfs --i2c=ALL:ALL --allow_other /mnt/1wire/

Automate this to run at startup
sudo crontab -e
	add lines
# init 1 Wire at startup
@reboot /home/pi/consumption/init1wire.sh

		
		

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
<<<<<<< HEAD
http://www.sbprojects.com/projects/raspberrypi/exim4.php
	sudo apt-get install ssmtp mailutils mpack
Now edit the file /etc/ssmtp/ssmtp.conf as root and add the next lines. Please note that some of the lines already exist and may need to be changed. Others don't exist yet and need to be added to the end of the file. 
Testing
mail -s "This is the subject line" someone@example.com < body.txt  cat body.txt | mail -s "This is the subject line" someone@example.com
=======
http://www.smbaker.com/a-python-api-for-the-nest-learning-thermostat
https://github.com/smbaker/pynest

Adding crontab
4,9,14,19,24,29,34,39,44,49,54,59 * * * * python /home/pi/pynest/nest_brfa.py --user bruno@famillefaucon.be --password Kate013. curtemp >/home/pi/pynest/temp
*/5 * * * * python /home/pi/pynest/nest_brfa.py --user bruno@famillefaucon.be --password Kate013. save
>>>>>>> Nest

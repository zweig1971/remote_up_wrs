#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import subprocess
import time

# hilfe
def help_txt():
    print "\nThis tool copy all relevant files for updating a wrs and make a reboot for install"
    print "Arguments :"
    print "-i --ip IP of the WRS to update"
    print "-p --path the path to the wrs-update files inlude the wrs_date\n"

# -------------------------- main ------------------------------

wrs_on = False

wrs_ip=0;
wrs_username = "root"
wrs_passwd = ""

files_path	= ""
file_wrs_firm   = "wrs-firmware.tar"
file_wrs_init   = "wrs-initramfs.gz"
file_ers_zImage = "zImage"
file_wrs_date	= "wr_date.conf"

dir_up_wrs_firmware  = "/update"
dir_up_wrs_initramfs = "/boot"
dir_up_wrs_date      = "/wr/etc"
file_up_wrs_restart  = "/sbin/reboot"

file_known_hosts     = "/home/bel/zweig/lnx/.ssh/known_hosts"


# arguments einlesen
try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:p:",["ip=","path="])
except getopt.GetoptError, err:
    print str(err)
    help_txt()
    sys.exit(2)

for opt, arg in opts:

    if opt == "-h":
	help_txt()
	sys.exit()
    elif opt in ("-i","--ip"):
        wrs_ip = arg
    elif opt in ("-p","--path"):
	files_path = arg 
    else:
        help_txt()

if len(sys.argv) != 5:
    help_txt()
    sys.exit(2)

# copy the wrs-firmaware.tar to the WRS /update
print"\ncopy the wrs-firmaware.tar to the WRS /update"
try:
    subprocess.call(["scp",files_path+file_wrs_firm,":".join([wrs_username+"@"+wrs_ip, dir_up_wrs_firmware])])
except Exception:
	sys.exit("Failure !")


# copy the wrs-initramfs.gz to the WRS /boot
print "\n----------------"
print "copy the wrs-initramfs.gz to the WRS /boot"
try:
    subprocess.call(["scp",files_path+file_wrs_init,":".join([wrs_username+"@"+wrs_ip, dir_up_wrs_initramfs])])
except Exception:
        sys.exit("Failure !")


# copy the zImage to the WRS to the WRS /boot
print "\n----------------"
print "copy the zImage to the WRS to the WRS /boot"
try:
    subprocess.call(["scp",files_path+file_ers_zImage,":".join([wrs_username+"@"+wrs_ip, dir_up_wrs_initramfs])])
except Exception:
        sys.exit("Failure !")


# restart the WRS 
print "\n----------------"
print "restart the switch"
try:
    subprocess.call(["ssh", wrs_username+"@"+wrs_ip, file_up_wrs_restart])
except Exception:
        sys.exit("Failure !")


# wait if wrs restarted
print "\n----------------"
print "wait for the switch take a few minutes..."
time.sleep(60)

while not wrs_on:
	response = os.system("ping -c 1 " + wrs_ip)
	if response == 0:
		wrs_on = True
	else:
		wrs_on = False
		
	time.sleep(10)

time.sleep(5)


# delete the known hosts
print "\n----------------"
print "delete known_hosts"
try:
    subprocess.call(["rm",file_known_hosts])
except Exception:
        sys.exit("Failure !")


# copy w_date
print "\n----------------"
print "copy wr_date to the WRS"
try:
    subprocess.call(["scp",files_path+file_wrs_date,":".join([wrs_username+"@"+wrs_ip, dir_up_wrs_date])])
except Exception:
        sys.exit("Failure !")


# restart the WRS 
print "\n----------------"
print "restart the switch"
try:
    subprocess.call(["ssh", wrs_username+"@"+wrs_ip, file_up_wrs_restart])
except Exception:
        sys.exit("Failure !")



print "\n\n\n...READY\n"


#!/usr/bin/python3

import os
import glob
import time
import paho.mqtt.client as mqtt #import the client1
from datetime import datetime

broker_address="10.29.30.155" 
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("poolpi") #create new instance
client.connect(broker_address) #connect to broker


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
now = str(datetime.now())
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

filetemp=open("temp.log","w")  


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        now = str(datetime.now())
        return temp_f,now
	
while True:
#	print(read_temp()) 	
        temp=str(read_temp())
        client.publish("poolpi", payload=temp, qos=0, retain=True)
        filetemp.write(temp)
        time.sleep(10)

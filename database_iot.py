from cloudant.client import Cloudant
username = "32fdead6-0500-4b2c-83fa-cc3f3ad0d8c4-bluemix"
password = "4ceeead77ba62584ae42ab343dfe1aeb0b1ac7595d326f6b3e98a8fe1a69c849"
Url = "https://32fdead6-0500-4b2c-83fa-cc3f3ad0d8c4-bluemix:4ceeead77ba62584ae42ab343dfe1aeb0b1ac7595d326f6b3e98a8fe1a69c849@32fdead6-0500-4b2c-83fa-cc3f3ad0d8c4-bluemix.cloudantnosqldb.appdomain.cloud"
dbname = "raspberryiot"

client = Cloudant(username,password,url=Url,connect=True,auto_renew=True)

mydb = client[dbname]


import RPi.GPIO as GPIO
import dht11
import time
import sys
import ibmiotf.application
import ibmiotf.device
from os.path import join,dirname
from os import environ
from pprint import pprint
from mcp3208 import MCP3208
#Provide your IBM Watson Device Credentials
organization = "y05zja"
deviceType = "raspberry"
deviceId = "praddy"
authMethod = "token" #dont change this
authToken = "l_BA7-dL&+bVRFTV2L"
# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16,GPIO.OUT)
GPIO.setup(15, GPIO.IN)

SensorInstance = dht11.DHT11(pin = 15)


# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions) #connect to ibmiotf platform
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit() #terminate program

def mycommandCallback(cmd):
                print ("command received: %s "  % cmd.data['command'])
                s=str(cmd.data['command'])
                print s
                if(s=="LIGHTON"):
                        GPIO.output(16,True)
                elif(s=="LIGHTOFF"):
                        GPIO.output(16,False)
                

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
while True:
    SensorData = SensorInstance.read()
    if SensorData.is_valid():
        T = SensorData.temperature
        H = SensorData.humidity
        data = { 'Temperature' : T, 'Humidity': H}
        mydoc = mydb.create_document(data)
        for doc in mydb:
            print doc
        def myOnPublishCallback():
            print "Published Temperature = %s C" % T, "Humidity = %s %%" % H, "Rainfall = %s" %d,"to IBM Watson"
        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback) #send data to cloud
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)

    else:
        print "SensorData Invalid"
        
    deviceCli.commandCallback=mycommandCallback
        

                
           
        
# Disconnect the device and application from the cloud
deviceCli.disconnect()

import RPi.GPIO as GPIO
import dht11
import time
import sys
import ibmiotf.application
import ibmiotf.device
from threading import*
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay
from os.path import join,dirname
from os import environ
from pprint import pprint
from mcp3208 import MCP3208

#Provide your IBM Watson Device Credentials
organization = "zxwdc4"
deviceType = "sasyaveda"
deviceId = "sasyaveda"
authMethod = "token" #dont change this
authToken = "I_m)1FkQKCa6y4wYmn"
# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
#dht11 pins
GPIO.setup(15, GPIO.IN)
GPIO.setup(14, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

SensorInstance1 = dht11.DHT11(pin = 15)
SensorInstance2 = dht11.DHT11(pin = 14)
SensorInstance3 = dht11.DHT11(pin = 18)
SensorInstance4 = dht11.DHT11(pin = 23)
SensorInstance5 = dht11.DHT11(pin = 24)
#ldr pins
delayt=0.1
value1 = 0 # this variable will be used to store the ldr value
ldr1 = 21
value2 = 0 # this variable will be used to store the ldr value
ldr2 = 2
value3 = 0 # this variable will be used to store the ldr value
ldr3 = 3
value4 = 0 # this variable will be used to store the ldr value
ldr4 = 20


# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq2_dpin = 26
mq2_apin = 1
#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(mq2_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions) #connect to ibmiotf platform
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit() #terminate program

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
class DHT11(Thread):
    def run(self):
        while True:
            
            SensorData1 = SensorInstance1.read()
            if SensorData1.is_valid():
                T = SensorData1.temperature
                H = SensorData1.humidity
                data = { 'Temperature' : T, 'Humidity': H}
                def myOnPublishCallback():
                    print "Published Temperature_1 = %s C" % T, "Humidity_1 = %s %%" % H,"to IBM Watson"
                success = deviceCli.publishEvent("DHT11-1", "json", data, qos=0, on_publish=myOnPublishCallback) #send data to cloud
                if not success:
                    print("Not connected to IoTF")
                time.sleep(2)
            SensorData2 = SensorInstance2.read()
            if SensorData2.is_valid():
                T = SensorData2.temperature
                H = SensorData2.humidity
                data = { 'Temperature' : T, 'Humidity': H}
                #print("hi2")
                def myOnPublishCallback():
                    print "Published Temperature_2 = %s C" % T, "Humidity_2 = %s %%" % H,"to IBM Watson"
                success = deviceCli.publishEvent("DHT11-2", "json", data, qos=0, on_publish=myOnPublishCallback) #send data to cloud
                if not success:
                    print("Not connected to IoTF")
                time.sleep(2)
            SensorData3 = SensorInstance3.read()
            if SensorData3.is_valid():
                T = SensorData3.temperature
                H = SensorData3.humidity
                data = { 'Temperature' : T, 'Humidity': H}
                #print("hi2")
                def myOnPublishCallback():
                    print "Published Temperature_3 = %s C" % T, "Humidity_3 = %s %%" % H,"to IBM Watson"
                success = deviceCli.publishEvent("DHT11-3", "json", data, qos=0, on_publish=myOnPublishCallback) #send data to cloud
                if not success:
                    print("Not connected to IoTF")
                time.sleep(2)
            SensorData4 = SensorInstance4.read()
            if SensorData4.is_valid():
                T = SensorData4.temperature
                H = SensorData4.humidity
                data = { 'Temperature' : T, 'Humidity': H}
                #print("hi2")
                def myOnPublishCallback():
                    print "Published Temperature_4 = %s C" % T, "Humidity_4 = %s %%" % H,"to IBM Watson"
                success = deviceCli.publishEvent("DHT11-4", "json", data, qos=0, on_publish=myOnPublishCallback) #send data to cloud
                if not success:
                    print("Not connected to IoTF")
                time.sleep(2)
            SensorData5 = SensorInstance5.read()
            if SensorData5.is_valid():
                T = SensorData5.temperature
                H = SensorData5.humidity
                data = { 'Temperature' : T, 'Humidity': H}
                #print("hi2")
                def myOnPublishCallback():
                    print "Published Temperature_5 = %s C" % T, "Humidity_5 = %s %%" % H,"to IBM Watson"
                success = deviceCli.publishEvent("DHT11-5", "json", data, qos=0, on_publish=myOnPublishCallback) #send data to cloud
                if not success:
                    print("Not connected to IoTF")
                time.sleep(2)
            
class Soil(Thread):
    
    
    def run(self):
        while True:
            channel=0
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture':data}
            def myvalue():
                print "Mosture=%s" %data
            success=deviceCli.publishEvent("Moisture","json",data1,qos=0,on_publish=myvalue)
            channel=1
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture1':data}
            def myvalue():
                print "Mosture1=%s" %data
            success=deviceCli.publishEvent("Moisture1","json",data1,qos=0,on_publish=myvalue)
            channel=2
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture2':data}
            def myvalue():
                print "Mosture2=%s" %data
            success=deviceCli.publishEvent("Moisture2","json",data1,qos=0,on_publish=myvalue)
            channel=3
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture3':data}
            def myvalue():
                print "Mosture3=%s" %data
            success=deviceCli.publishEvent("Moisture3","json",data1,qos=0,on_publish=myvalue)
   
"""class LDR(Thread):
                def rc_time (ldr1):
                    count = 0
                 
                    #Output on the pin for
                    GPIO.setup(ldr1, GPIO.OUT)
                    GPIO.output(ldr1, False)
                    time.sleep(delayt)
                 
                    #Change the pin back to input
                    GPIO.setup(ldr1, GPIO.IN)
                 
                    #Count until the pin goes high
                    while (GPIO.input(ldr1) == 0):
                        count += 1
                 
                    return count
                while True:
                    print("Ldr1 Value:")
                    value1 = rc_time(ldr1)
                    print(value1)
                    #print(data)
                    sleep(2)
                    data1={'ldr1':value1}
                    def myvalue():
                        print "ldr1=%s" %value1
                    success=deviceCli.publishEvent("ldr1","json",data1,qos=0,on_publish=myvalue)
                    break """                

class MQ(Thread):
        def run(self):
             init()
             while True:
                      COlevel=readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                      cop=((COlevel/1024.)*100)
                      cov=((COlevel/1024.)*3.3)
                      sleep(2)
                      def myvalue():
                          #print("Gas leakage")
                          print("Current CO density is:" +str("%.2f"%((COlevel/1024.)*100))+" %")
                          #print"Current Gas AD vaule = " +str("%.2f"%((COlevel/1024.)*3.3))+" V"
                          time.sleep(0.5)
                      success=deviceCli.publishEvent("CO density","json",cop,qos=0,on_publish=myvalue)

t3=DHT11()
t2=Soil()
#t1=LDR()
t1=MQ()
#t1.start()
sleep(2)
t2.start()
t3.start()
t1.start()

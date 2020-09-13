import RPi.GPIO as GPIO
import dht11
import time
import sys
from firebase import firebase as fb
from pprint import pprint
from numpy import interp
from threading import*
import spidev # To communicate with SPI devices
from time import sleep  # To add delay
import pyrebase, random
from mcp3208 import MCP3208
config = {
  "apiKey": "AIzaSyBnjuCeauIsqcYUO6eQ2RPlVxeYLpl9Nfw",
  "authDomain": "sasyaveda-e9863.firebaseapp.com",
  "databaseURL": "https://sasyaveda-e9863.firebaseio.com",
  "storageBucket": "sasyaveda-e9863.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(14, GPIO.IN)

SensorInstance = dht11.DHT11(pin = 14)
'''delayt=0.1
value1 = 0 # this variable will be used to store the ldr value
ldr1 = 3
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
def rc_time ():
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
                 
    return count'''
#Initialize the fire base
firebase1= fb.FirebaseApplication('https://sasyaveda-data.firebaseio.com/')
class Hello(Thread):
    def run(self):
        while True:
            
            SensorData = SensorInstance.read()
            if SensorData.is_valid():
                T = SensorData.temperature
                H = SensorData.humidity
                db.child("pi").child("TEMP").set(T)
                db.child("pi").child("humi").set(H)

                '''thevalue = db.child("pi").child("pi_value1").get().val()'''
                data = { 'Temperature' : T, 'Humidity': H}
                print(data)
                db.child("pi").child("DATA").set(data)
                thevalue = db.child("pi").child("DATA").get().val()
                print ("Pi Value 1: ", thevalue)
                time.sleep(2)
                result1 = firebase1.post('DHT11',data)
                print(result1)

'''class Soil(Thread):
    def run(self):
        while True:
            channel=2
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            time.sleep(2)
            data1={'Moisture':data}
            print(data1)
            result2 = firebase.post('Moisture',data1)
            print(result2)
        
class LDR(Thread):
    def run(self):
        while True:
            print("Ldr1 Value:")
            value1 = rc_time()
            print(value1)
                                    #print(data)
            sleep(2)
            data1={'ldr1':value1}
            print(data1)
            result2 = firebase.post('ldr',data1)
            print(result2)
                
class MQ(Thread):
        def run(self):
             init()
             while True:
                      COlevel=readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                      cop=((COlevel/1024.)*100)
                      cov=((COlevel/1024.)*3.3)
                      time.sleep(2)
                      print("COlevel",cop)
                      result3 = firebase.post('COlevel',cop)
                      print(result3)'''
t1=Hello()
'''t2=Soil()
t3=MQ()
t4=LDR()'''
t1.start()
'''sleep(2)
t2.start()
sleep(2)
t3.start()
sleep(2)
t4.start()'''

import RPi.GPIO as GPIO
import dht11
import time
import sys
import pyrebase
from firebase import firebase as fb
from pprint import pprint
from threading import*
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay
from mcp3208 import MCP3208

#Initialize the fire base
firebase1= fb.FirebaseApplication('https://sasyaveda-data.firebaseio.com/')
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
ldr1 = 4
value2 = 0 # this variable will be used to store the ldr value
ldr2 = 2
value3 = 0 # this variable will be used to store the ldr value
ldr3 = 3
value4 = 0 # this variable will be used to store the ldr value
ldr4 = 17
value5 = 0 # this variable will be used to store the ldr value
ldr5 = 27

# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,1)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq2_dpin = 26
mq2_apin = 4

def rc_time1 ():
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
def rc_time2 ():
    count2 = 0
                 
                    #Output on the pin for
    GPIO.setup(ldr2, GPIO.OUT)
    GPIO.output(ldr2, False)
    time.sleep(delayt)
                 
                    #Change the pin back to input
    GPIO.setup(ldr2, GPIO.IN)
                 
                    #Count until the pin goes high
    while (GPIO.input(ldr2) == 0):
        count2 += 1
                 
    return count2
def rc_time3 ():
    count3 = 0
                 
                    #Output on the pin for
    GPIO.setup(ldr3, GPIO.OUT)
    GPIO.output(ldr3, False)
    time.sleep(delayt)
                 
                    #Change the pin back to input
    GPIO.setup(ldr3, GPIO.IN)
                 
                    #Count until the pin goes high
    while (GPIO.input(ldr3) == 0):
        count3 += 1
                 
    return count3
def rc_time4 ():
    count4 = 0
                 
                    #Output on the pin for
    GPIO.setup(ldr4, GPIO.OUT)
    GPIO.output(ldr4, False)
    time.sleep(delayt)
                 
                    #Change the pin back to input
    GPIO.setup(ldr4, GPIO.IN)
                 
                    #Count until the pin goes high
    while (GPIO.input(ldr4) == 0):
        count4 += 1
                 
    return count4
def rc_time5 ():
    count5 = 0
                 
                    #Output on the pin for
    GPIO.setup(ldr5, GPIO.OUT)
    GPIO.output(ldr5, False)
    time.sleep(delayt)
                 
                    #Change the pin back to input
    GPIO.setup(ldr5, GPIO.IN)
                 
                    #Count until the pin goes high
    while (GPIO.input(ldr5) == 0):
        count5 += 1
                 
    return count5
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


class DHT11(Thread):
       
    def run(self):
        while True:
            
            SensorData1 = SensorInstance1.read()
            if SensorData1.is_valid():
                T = SensorData1.temperature
                H = SensorData1.humidity
                data1 = { 'Temperature' : T, 'Humidity': H}
                result1 = firebase1.post('DHT11-1',data1)
                db.child("DHT11").child("D-DATA-1").set(data1)
                print("dht1",data1)
                time.sleep(2)
                
            SensorData2 = SensorInstance2.read()
            if SensorData2.is_valid():
                T = SensorData2.temperature
                H = SensorData2.humidity
                data2 = { 'Temperature' : T, 'Humidity': H}
                result1 = firebase1.post('DHT11-2',data2)
                db.child("DHT11").child("D-DATA-2").set(data2)
                print("dht2",data2)
                time.sleep(2)
            SensorData3 = SensorInstance3.read()
            if SensorData3.is_valid():
                T = SensorData3.temperature
                H = SensorData3.humidity
                data3 = { 'Temperature' : T, 'Humidity': H}
                result1 = firebase1.post('DHT11-3',data3)
                db.child("DHT11").child("D-DATA-3").set(data3)
                print("dht3",data3)
                time.sleep(2)
                
            SensorData4 = SensorInstance4.read()
            if SensorData4.is_valid():
                T = SensorData4.temperature
                H = SensorData4.humidity
                data4 = { 'Temperature' : T, 'Humidity': H}
                result1 = firebase1.post('DHT11-4',data4)
                db.child("DHT11").child("D-DATA-4").set(data4)
                print("dht4",data4)
                time.sleep(2)
            T = (SensorData1.temperature+SensorData2.temperature+SensorData3.temperature+SensorData4.temperature)/4
            H = (SensorData1.humidity+SensorData2.humidity+SensorData3.humidity+SensorData4.humidity)/4
            DATA = { 'Temperature' : T, 'Humidity': H}
            result1 = firebase1.post('DHT11-AVG',DATA)
            db.child("DHT11").child("D-DATA-AVG").set(DATA)
            print('data-avg:',DATA)
                
            SensorData5 = SensorInstance5.read()
            if SensorData5.is_valid():
                T = SensorData5.temperature
                H = SensorData5.humidity
                data = { 'Temperature' : T, 'Humidity': H}
                result1 = firebase1.post('DHT11-5',data)
                db.child("DHT11").child("D-DATA-5").set(data)
                print("dht-AVG",data)
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
            data1={'Moisture1':data}
            result1 = firebase1.post('Moisture-1',data1)
            db.child("Moisture").child("M-DATA-1").set(data1)
            print("Moisture1",data1)
            time.sleep(2)
            

            channel=1
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture2':data}
            result1 = firebase1.post('Moisture-2',data1)
            db.child("Moisture").child("M-DATA-2").set(data1)
            print("Moisture2",data1)
            time.sleep(2)
            

            channel=2
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture3':data}
            result1 = firebase1.post('Moisture-3',data1)
            db.child("Moisture").child("M-DATA-3").set(data1)
            print("Moisture3",data1)
            time.sleep(2)
            

            channel=3
            spi.max_speed_hz = 1350000
            adc = spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            data=interp(data,[0,1023],[100,0])
            data=int(data)
            print(data)
            sleep(2)
            data1={'Moisture4':data}
            result1 = firebase1.post('Moisture-4',data1)
            db.child("Moisture").child("M-DATA-4").set(data1)
            print("Moisture4",data1)
            time.sleep(2)
            
class LDR1(Thread):
    def run(self):
        while True:
            print("Ldr1 Value:")
            value1 = rc_time1()
            data1={'ldr1':value1}
            result1 = firebase1.post('ldr-1',data2)
            db.child("LDR").child("L-DATA-1").set(data1)
            print(data1)
            sleep(2)

            
class LDR2(Thread):
    '''def run1(self):
        while True:
            print("Ldr1 Value:")
            value1 = rc_time1()
            data1={'ldr1':value1}
            result1 = firebase1.post('ldr-1',data1)
            db.child("LDR").child("L-DATA-1").set(data1)
            print(data1)
            sleep(2)
    def run4(self):
        while True:
            print("Ldr4 Value:")
            value4 = rc_time4()
            data4={'ldr4':value4}
            result1 = firebase1.post('ldr-4',data4)
            db.child("LDR").child("L-DATA-4").set(data4)
            print(data4)
            sleep(2)
    def run3(self):
        while True:
            print("Ldr3 Value:")
            value3 = rc_time3()
            data3={'ldr3':value3}
            result1 = firebase1.post('ldr-3',data3)
            db.child("LDR").child("L-DATA-3").set(data3)
            print(data3)
            sleep(2)
    def run5(self):
        while True:
            print("Ldr5 Value:")
            value5 = rc_time5()
            data5={'ldr5':value5}
            result1 = firebase1.post('ldr-5',data5)
            db.child("LDR").child("L-DATA-5").set(data5)
            print(data5)
            sleep(2)  '''
    def run(self):
        while True:
            print("Ldr2 Value:")
            value2 = rc_time2()
            data2={'ldr2':value2}
            result1 = firebase1.post('ldr-2',data2)
            db.child("LDR").child("L-DATA-2").set(data2)
            print(data2)
            sleep(2)

class LDR3(Thread):
    def run(self):
        while True:
            print("Ldr3 Value:")
            value3 = rc_time3()
            data3={'ldr3':value3}
            result1 = firebase1.post('ldr-3',data3)
            db.child("LDR").child("L-DATA-3").set(data3)
            print(data3)
            sleep(2)

class LDR4(Thread):
    def run(self):
        while True:
            print("Ldr4 Value:")
            value4 = rc_time4()
            data4={'ldr4':value4}
            result1 = firebase1.post('ldr-4',data4)
            db.child("LDR").child("L-DATA-4").set(data4)
            print(data4)
            sleep(2)
            
class LDR5(Thread):
    def run(self):
        while True:
            print("Ldr5 Value:")
            value5 = rc_time5()
            data5={'ldr5':value5}
            result1 = firebase1.post('ldr-5',data5)
            db.child("LDR").child("L-DATA-5").set(data5)
            print(data5)
            sleep(2)  
class MQ(Thread):
        def run(self):
             init()
             while True:
                      COlevel=readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                      cop=((COlevel/1024.)*100)
                      cov=((COlevel/1024.)*3.3)
                      time.sleep(2)
                      result1 = firebase1.post('CO-DATA',cop)
                      db.child("CO-LEVEL").child("CO-DATA").set(cop)
                      print("CO level",cop)
                      
t1=DHT11()
t2=Soil()
t3=MQ()
t4=LDR2()
t5=LDR1()
t6=LDR3()
t7=LDR4()
t8=LDR5()
t1.start()
sleep(2)
t2.start()
sleep(2)
t3.start()
sleep(2)
t4.start()
sleep(2)
t5.start()
sleep(2)
t6.start()
sleep(2)
t7.start()
sleep(2)
t8.start()





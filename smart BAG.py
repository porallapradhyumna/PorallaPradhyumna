import RPi.GPIO as GPIO
import time
import dht11
import serial
import os, time
import string
import pynmea2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
chanel0=0
chanel1=1
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.OUT)
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(chanel0,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
def init1():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(chanel1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

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
GPIO.setmode(GPIO.BCM)

#define the pin that goes to the circuit
pin_to_circuit = 16

def rc_time (pin_to_circuit):
    count = 0

    #Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count
#main ioop
def main():

         init()
         init1()
         print("please wait...")
         time.sleep(2)
         while True:
                  #heart beat
                  COlevel=readadc(chanel0, SPICLK, SPIMOSI, SPIMISO, SPICS)
                  rate=(COlevel/1024.)*100
                  rate1=int(rate)
                  if(rate1<=60):
                      print("heart=",rate1+10)
                  elif(rate1<=50):
                      print("heart beat not found")
                  else:
                      print("heart=",rate1)
                  #lm35
                  COlevel1=readadc(chanel1, SPICLK, SPIMOSI, SPIMISO, SPICS)
                  volts = (COlevel1*3.3)/1024
                  temperature = volts/(10.0 / 1000)
                  print("temperature=",temperature)
                  #force
                  force=rc_time(pin_to_circuit)-20000+20000
                  print("force=",force)
                  #push
                  GPIO.setup(21, GPIO.IN)
                  circit = GPIO.input(21)
                  '''if circuit==False:
                      print "Button Pressed"
                      GPIO.output(20, GPIO.HIGH)
                  elif circuit==True:
                      print "Not Pressed"
                      GPIO.output(20, GPIO.LOW)'''
                  count=0
                  while(circit == False):
                      count=count+1
                  print(count)
                  if(count >= 3s):
                      while True:
                          GPIO.output(20, GPIO.HIGH)
                          if(circit == False):
                              return main()
                          else:
                              continue
                  elif (((force <= 70) and (circit == False) and (rate1 >= 69)) or ((force <= 70) and (circit == False) and (temperature <= 32)) or ((rate1 >= 69) and (circit == False) and (temperature <= 32))):
                      print("hi")
                      GPIO.output(20, GPIO.HIGH)
                      port1 = "/dev/ttyAMA0"
                      ser = serial.Serial(port1, baudrate=9600, timeout=0.5)
                      dataout = pynmea2.NMEAStreamReader()
                      newdata = ser.readline()
                      if newdata[0:6] == "$GPRMC":
                          newmsg = pynmea2.parse(newdata)
                          lat = newmsg.latitude
                          lng = newmsg.longitude
                          gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
                          print(gps)

                      port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

                      # Transmitting AT Commands to the Modem
                      # '\r\n' indicates the Enter key

                      port.write('AT' + '\r\n')
                      rcv = port.read(10)
                      print (rcv)
                      time.sleep(1)

                      port.write('ATE0' + '\r\n')  # Disable the Echo
                      rcv = port.read(10)
                      print (rcv)
                      time.sleep(1)

                      port.write('AT+CMGF=1' + '\r\n')  # Select Message format as Text mode
                      rcv = port.read(10)
                      print (rcv)
                      time.sleep(1)

                      port.write('AT+CNMI=2,1,0,0,0' + '\r\n')  # New SMS Message Indications
                      rcv = port.read(10)
                      print (rcv)
                      time.sleep(1)

                      # Sending a message to a particular Number

                      port.write('AT+CMGS="+919010163166"' + '\r\n')
                      rcv = port.read(10)
                      print (rcv)
                      time.sleep(1)

                      port.write('Hello Pradhyumma' + str(lat) + ' ' + str(lng) + '\r\n')  # Message
                      rcv = port.read(10)
                      print (rcv)

                      port.write("\x1A")  # Enable to send SMS
             584694         for i in range(10):
                          rcv = port.read(10)
                          print (rcv)
                      time.sleep(5)
                      while True:
                          GPIO.output(20, GPIO.HIGH)
                          if(circit == False):
                              return main()
                          else:
                              continue
                  time.sleep(5)
                  elif(((force<=70)and(circit==False))or((rate1>=69)and(force<=70))or((force<=70)and(temperature<=32))or((circit==False)and(rate1>=69))or((circit==False)and(temperature<=32))or((rate1>=69)and(temperature<=32))):
                        print "on"
                        port1="/dev/ttyAMA0"
                        ser=serial.Serial(port1, baudrate=9600, timeout=0.5)
                        dataout = pynmea2.NMEAStreamReader()
                        newdata=ser.readline()
                        if newdata[0:6] == "$GPRMC":
                             newmsg=pynmea2.parse(newdata)
                             lat=newmsg.latitude
                             lng=newmsg.longitude
                             gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
                             print(gps)

                        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

                        # Transmitting AT Commands to the Modem
                        # '\r\n' indicates the Enter key

                        port.write('AT'+'\r\n')
                        rcv = port.read(10)
                        print (rcv)
                        time.sleep(1)

                        port.write('ATE0'+'\r\n')      # Disable the Echo
                        rcv = port.read(10)
                        print (rcv)
                        time.sleep(1)

                        port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode
                        rcv = port.read(10)
                        print (rcv)
                        time.sleep(1)

                        port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
                        rcv = port.read(10)
                        print (rcv)
                        time.sleep(1)

                        # Sending a message to a particular Number

                        port.write('AT+CMGS="+919010163166"'+'\r\n')
                        rcv = port.read(10)
                        print (rcv)
                        time.sleep(1)

                        port.write('Hello Pradhyumma'+str(lat)+' '+str(lng)+'\r\n')  # Message
                        rcv = port.read(10)
                        print (rcv)

                        port.write("\x1A") # Enable to send SMS
                        for i in range(10):
                            rcv = port.read(10)
                            print (rcv)
                        time.sleep(5)
                        GPIO.output(20, GPIO.HIGH)







main()
GPIO.cleanup()



import RPi.GPIO as GPIO
import smtplib
import time
import sys
import ibmiotf.application
import ibmiotf.device
from os.path import join,dirname
from os import environ
from pprint import pprint

organization = "6qlbt7"
deviceType = "bin"
deviceId = "bindrop"
authMethod = "token" #dont change this
authToken = "q8qJjsB_q!?)An?LIZ"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
print ("Distance Measurement In Progress")
SERVO=21
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.setup(SERVO,GPIO.OUT)
#GPIO.output(TRIG, False)
GPIO.setup(17,GPIO.IN) #GPIO 2 -> Left IR out
GPIO.setup(27,GPIO.IN) #GPIO 3 -> Right IR out
                                    #print(17,IO.IN)
GPIO.setup(7,GPIO.OUT) #GPIO 4 -> Motor 1 terminal A
GPIO.setup(8,GPIO.OUT) #GPIO 14 -> Motor 1 terminal B
GPIO.setup(9,GPIO.OUT) #GPIO 17 -> Motor Left terminal A
GPIO.setup(10,GPIO.OUT) #GPIO 18 -> Motor Left terminal B
print ("Waiting For Sensor To Settle")
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
                if(s=="drop"):
                    motor()
                        



                elif(s=="dontdrop"):
                        GPIO.output(7,False)
                        GPIO.output(8,False)
                        GPIO.output(9,False)
                        GPIO.output(10,False)
                        

deviceCli.connect()
def motor():
        while True:
                                    
                if(GPIO.input(17)==True and GPIO.input(27)==True): #both while move forward
                        GPIO.output(7,True) #1A+
                        GPIO.output(8,False) #1B-
                        GPIO.output(9,True) #2A+
                        GPIO.output(10,False) #2B-
                                #GPIO.output(21,False)
                elif(GPIO.input(17)==False and GPIO.input(27)==True): #turn right  
                        GPIO.output(7,True) #1A+
                        GPIO.output(8,True) #1B-
                        GPIO.output(9,True) #2A+
                        GPIO.output(10,False) #2B-
                                #GPIO.output(21,False)
                elif(GPIO.input(17)==True and GPIO.input(27)==False): #turn left                            
                        GPIO.output(7,True) #1A+
                        GPIO.output(8,False) #1B-
                        GPIO.output(9,True) #2A+
                        GPIO.output(10,True) #2B-
                                #GPIO.output(21,False)
                elif(GPIO.input(17)==False and GPIO.input(27)==False):
                        servo=21
                        GPIO.setwarnings(False)
                        GPIO.setup(servo,GPIO.OUT)
                        pwm=GPIO.PWM(servo,50)
                        pwm.start(7)
                        def SetAngle(angle):
                                duty=angle/18+2
                                GPIO.output(servo,True)
                                pwm.ChangeDutyCycle(duty)
                                time.sleep(1)
                                GPIO.output(servo,False)
                                pwm.ChangeDutyCycle(0)
                        while True:
                                SetAngle(10)
                                time.sleep(2)    
                                SetAngle(120)

                                time.sleep(5)#SetAngle(0)
                                SetAngle(10)     
                            
                                pwm.stop()
                                    #GPIO.cleanup() 
while True:
    def distance():
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == False:
            StartTime = time.time()
     
        while GPIO.input(GPIO_ECHO) == True:
            StopTime = time.time()

            TimeElapsed = StopTime - StartTime
            distance = TimeElapsed * 17150
            distance = round(distance, 2)
            distance = distance*100/200
        return distance


         
    if __name__ == '__main__':
        try:
            while True:
                dist = distance()
                print ("Measured Distance = %.1f cm" % dist)
                time.sleep(1)
                data = {'distance':dist}
                def myOnPublishCallback():
                    print "Published distance = %s" % dist, "to IBM Watson"
                success = deviceCli.publishEvent("Level", "json", data, qos=0, on_publish=myOnPublishCallback) 
                if not success:
                    print("Not connected to IoTF")
                time.sleep(2)
                deviceCli.commandCallback=mycommandCallback
                if (dist<=10) :
                
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()                    
                    server.login('porallap@gmail.com','9849933793' )
                    server.sendmail('porallap@gmail.com','porallap@gmail.com','TEMP IS HIGH https://bindrop.eu-gb.mybluemix.net/ui/')
                    server.quit()
                  
                    
        except KeyboardInterrupt:
                print("Measurement stopped by User")
GPIO.cleanup()
deviceCli.disconnect()


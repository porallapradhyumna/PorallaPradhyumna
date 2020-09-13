# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 21:00:11 2020

@author: PRADHYUMNA
"""

import numpy as np
import pandas as pd
import platform,os
from datetime import datetime
import speech_recognition as sr
from playsound import playsound
from Recive_Response import SpeechAndReply as s



dataset = pd.read_csv('Talkbot.csv')
x = dataset.iloc[:, 0].values
y = dataset.iloc[:, 3].values
x = x.tolist()
y = y.tolist()

for n,i in enumerate(x):
    x[n]=i.lower()
for n,i in enumerate(y):
    y[n]=i.lower()
    
    
def Talkbot(text):    
    if "medicine" in text  :        
        while True:
            playsound("intialising.mp3")
            r = sr.Recognizer()
            text = s.Recogniser(r)
            try:
                if text in x:
                    idx = x.index(text.lower())
                    s.Reply(y[idx])
                elif "time" in text or "date" in text:
                    time=datetime.now()
                    idx = "Today date is"+str(time.day)+","+str(time.month)+","+str(time.year)+"and time now is"+str(time.hour)+"hours"+str(time.minute)+"minutes"
                    s.Reply(idx)
                elif "end" in text or "exit" in text:
                    playsound("havegreatday.mp3")
                    break
                elif "system" in text:
                    uname=platform.uname()
                    idx = " system "+uname.system+" node "+uname.node+" release "+uname.release+" version "+str(uname.version)+" machine "+str(uname.machine)+" processor "+str(uname.processor)
                    s.Reply(idx)
                else:
                    s.Reply("Sorry ! I am still learning")
                    break
            except:
                s.Reply("Something went wrong")
            
r = sr.Recognizer()
text = s.Recogniser(r)
Talkbot(text)
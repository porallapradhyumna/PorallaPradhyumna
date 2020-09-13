# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 16:48:00 2020

@author: PRADHYUMNA
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode

#img = cv2.imread('')

class QRCode:
    def QRCodeScaner(cap):
        cap.set(3,640)
        cap.set(4,480)
        while True:
            ret,img=cap.read()
            
            for barcode in decode(img):
                #print(barcode.data)
                mydata= barcode.data.decode('utf-8')
                print(mydata)
                #return mydata
                cv2.imshow("result",img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
"""
qr = QRCode
cap = cv2.VideoCapture(0)


qr.QRCodeScaner(cap)
"""
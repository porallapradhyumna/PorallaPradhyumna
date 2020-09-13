# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 19:31:48 2020

@author: PRADHYUMNA
"""

import cv2
import face_recognition 
import numpy as np
import os
class FaceRecognition:
    
    file ="final_project"
    images = []
    person_precense = []
    classNames = []
    all_images = os.listdir(file)
            
    for img in all_images:
        images.append(img)
        person_precense.append(img.upper())
        curImg = cv2.imread(f'{file}/{img}')
        classNames.append(os.path.splitext(img)[0])
           
        
        #all_images,classNames,file=intiatisation()
        #all_images,classNames,file=intiatisation()
        def train_face(faces,file):
            """
        

            Parameters
            ----------
            faces : Image array which is already in the class with the variable (ci)
    
            Returns
            -------
            encode_img :Tensor array
                DESCRIPTION.
    
            """
            encode_img = []
            for en in faces:
                train = face_recognition.load_image_file(f'{file}/{en}')
                train = cv2.cvtColor(train,cv2.COLOR_BGR2RGB)
                encode_train = face_recognition.face_encodings(train)[0]
                encode_img.append(encode_train)
            return encode_img

    trainImages = train_face(all_images,file)

    #trainImages = FaceRecognition.train_face(all_images,file)

    def Recognizer(cap):
        """
        

        Parameters
        ----------
        cap : capture Element or camera value cap = cv2.VideoCapture(0)
            DESCRIPTION.

        Returns
        -------
        Person name 

        """
        ci = FaceRecognition.trainImages
        while True:
            source,image = cap.read()
            frame = cv2.resize(image,(0,0),None,0.25,0.25)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            frameloc = face_recognition.face_locations(frame)
            frameencode = face_recognition.face_encodings(frame,frameloc)
            
            for encodeFace,faceLoc in zip(frameencode,frameloc):
                matches = face_recognition.compare_faces(ci,encodeFace)
                faceDis = face_recognition.face_distance(ci,encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis)
         
                if matches[matchIndex]:
                    name = FaceRecognition.classNames[matchIndex].upper()
                    #print(name)
                    y1,x2,y2,x1 = faceLoc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(image,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(image,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    return True,name
                else:
                    return False,""
                
                
"""fr = FaceRecognition
cap = cv2.VideoCapture(0)
fr.Recognizer(cap)"""
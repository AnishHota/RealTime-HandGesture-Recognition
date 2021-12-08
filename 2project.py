#TO-DO:
# Two rectangles
# Prediction
# Text to speech
# Model train
#Import libraries
from keras.models import load_model
import cv2
import copy
import numpy as np
from gtts import gTTS
import os
import urllib.request

#Global Variables
x1,y1 = 20,80
x2,y2 = 400,80
w = 200
numbers = ["+","0","1","2","3","4","5"]
count_frames = 0
number = ""
old_pred = None
new_pred = None
def draw_rect(frame):
    cv2.rectangle(frame,(x1,y1),(x1+w,y1+w),(255,0,0),5)
    cv2.rectangle(frame,(x2,y2),(x2+w,y2+w),(255,0,0),5)

    return frame

#Preprocessing of Region of Interest
def preprocess(roi):
    #Converting RGB image to Gray(Binary)
    roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    #Gaussian Blur
    roi = cv2.GaussianBlur(roi,(7,7),3)
    #Adaptive Gaussian Thresholding + Binary Inverse
    roi = cv2.adaptiveThreshold(roi,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    #Binary Inverse + OTSU Thresholding
    ret,roi_new = cv2.threshold(roi,25,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return roi_new

if __name__ == "__main__":
    global x1,y1,x2,y2
    model = load_model('digit_model.h5')
    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        _, window = capture.read()
        window = cv2.flip(window,1)
        frame = copy.deepcopy(window)
        frame = draw_rect(frame)
        roi1 = frame[y1:y1+w,x1:x1+w]
        roi2 = frame[y2:y2+w,x2:x2+w]
        roi1 = preprocess(roi1)
        roi1 = cv2.resize(roi1,(300,300))
        cv2.imshow("roi1",roi1)
        roi2 = preprocess(roi2)
        roi2 = cv2.resize(roi2,(300,300))
        cv2.imshow("roi2",roi2)
        img1 = np.float32(roi1)/255.
        img1 = np.expand_dims(img1,axis=0)
        img1 = np.expand_dims(img1,axis=-1)
        img2 = np.float32(roi2)/255.
        img2 = np.expand_dims(img2,axis=0)
        img2 = np.expand_dims(img2,axis=-1)
        pred1 = numbers[np.argmax(model.predict(img1)[0])]
        pred2 = numbers[np.argmax(model.predict(img2)[0])]
        if pred1=="+" or pred2 == "+":
            cv2.putText(frame,'Operation:+',(x1,y1+w+50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
        else:
            cv2.putText(frame,'Count:'+str(int(pred1)+int(pred2)),(x1,y1-50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        if((pred1!="+" and pred2!="+") and not(pred1=="0" and pred2=="0")):
            if(old_pred==None):
                old_pred = int(pred1)+int(pred2)
            elif(new_pred==None):
                new_pred = int(pred1)+int(pred2)
            elif(new_pred==old_pred and count_frames<10):
                count_frames+=1
            else:
                count_frames=0
                if new_pred==10:
                    number += "0"
                else:
                    number += str(new_pred)
                old_pred=None
                new_pred=None

        cv2.putText(frame,"Number: "+number,(x1,y1+w+100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

        cv2.imshow("Live Feed",frame)

        pressed_key = cv2.waitKey(1)
        if pressed_key == 27:
            break
        elif pressed_key == ord('i'):
            y2 = max(y2-5,0)
        elif pressed_key == ord('j'):
            x2 = max(x2-5,0)
        elif pressed_key == ord('k'):
            y2 = min(y2+5,window.shape[0]-w)
        elif pressed_key == ord('l'):
            x2 = min(x2+5,window.shape[1]-w)
        elif pressed_key == ord('w'):
            y1 = max(y1-5,0)
        elif pressed_key == ord('a'):
            x1 = max(x1-5,0)
        elif pressed_key == ord('s'):
            y1 = min(y1+5,window.shape[0]-w)
        elif pressed_key == ord('d'):
            x1 = min(x1+5,window.shape[1]-w)
    cv2.destroyAllWindows()
    capture.release()

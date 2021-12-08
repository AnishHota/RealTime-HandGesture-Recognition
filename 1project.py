
#Import libraries
from keras.models import load_model
import cv2
import copy
import numpy as np
import os
import urllib.request

#Global Variables
x1,y1 = 20,80
x2,y2 = 400,80
w = 200
numbers = [0,1,2,3,4,5]

def draw_rect(frame):
    cv2.rectangle(frame,(x1,y1),(x1+w,y1+w),(0,250,0),5)
    cv2.rectangle(frame,(x2,y2),(x2+w,y2+w),(0,250,0),5)

    return frame

def preprocess(roi):
    roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("bgr2gray",roi)
    roi = cv2.GaussianBlur(roi,(7,7),3)
    #cv2.imshow("gaussianblur",roi)
    roi = cv2.adaptiveThreshold(roi,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    #cv2.imshow("gaussian threshold",roi)
    ret,roi_new = cv2.threshold(roi,25,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #cv2.imshow("otsu threshold",roi_new)
    return roi_new

if __name__ == "__main__":
    global x1,y1,x2,y2
    model = load_model('model_6cat.h5')
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

        cv2.putText(frame,'Count:'+str(pred1+pred2),(20,30),cv2.FONT_HERSHEY_TRIPLEX,1,(0,250,0),2)

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

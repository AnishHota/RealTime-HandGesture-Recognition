
#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2
import os


dataColor = (0,255,0)
font = cv2.FONT_HERSHEY_SIMPLEX
fx, fy, fh = 10, 50, 45
takingData = 0
className = 'NONE'
count = 0
showMask = 0

classes = 'ZERO ONE TWO THREE FOUR FIVE ADD SUBTRACT'.split()

def initClass(name):
    global className, count
    className = name
    os.system('mkdir -p data/%s' % name)
    count = len(os.listdir('data/%s' % name))

def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7,7), 3)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    _, new = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return new

def main():
    global font, size, fx, fy, fh
    global takingData, dataColor
    global className, count
    x0, y0, width = 380, 140, 200
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        window = copy.deepcopy(frame)
        cv2.rectangle(window, (x0,y0), (x0+width-1,y0+width-1), dataColor, 5)

        if takingData:
            dataColor = (0,0,250)
            cv2.putText(window, 'Taking Data: ON', (fx,fy), font, 1.2, dataColor, 2, 1)
        else:
            dataColor = (0,250,102)
            cv2.putText(window, 'Taking Data: OFF', (fx,fy), font, 1.2, dataColor, 2, 1)
        cv2.putText(window, 'Class Name: %s (%d)' % (className, count), (fx,fy+fh), font, 1.0, (245,210,65), 2, 1)

            # get region of interest
        roi = frame[y0:y0+width,x0:x0+width]
        roi = preprocess(roi)
        roi = cv2.resize(roi,(300,300))

        if takingData:
            cv2.imwrite('data/{0}/{0}_{1}.png'.format(className, count), roi)
            count += 1

        cv2.imshow('Original', window)
        key = cv2.waitKey(10)
        if key == 27:
            break
        # Toggle data taking
        elif key == ord('s'):
            takingData = not takingData
        # Toggle class
        elif key == ord('0'):
            initClass('ZERO')
        elif key == ord('1'):
            initClass('ONE')
        elif key == ord('2'):
            initClass('TWO')
        elif key == ord('3'):
            initClass('THREE')
        elif key == ord('4'):
            initClass('FOUR')
        elif key == ord('5'):
            initClass('FIVE')
        elif key == ord('+'):
            initClass('ADD')
        elif key == ord('-'):
            initClass('SUBTRACT')
        elif key == ord('u'):
            initClass('OKAY')
        elif key == ord('d'):
            initClass('DOWN')
        # adjust the position of window
        elif key == ord('i'):
            y0 = max((y0 - 5, 0))
        elif key == ord('k'):
            y0 = min((y0 + 5, window.shape[0]-width))
        elif key == ord('j'):
            x0 = max((x0 - 5, 0))
        elif key == ord('l'):
            x0 = min((x0 + 5, window.shape[1]-width))

    cam.release()


if __name__ == '__main__':
    initClass('NONE')
    main()

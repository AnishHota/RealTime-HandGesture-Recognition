#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import *
from tkinter.ttk import Frame, Button, Label, Style, Menubutton
from random import randint
from tkinter import ttk
import pickle
import imageio
from skimage import transform
from scipy import misc
from PIL import Image
import numpy as np
import PIL
import pandas as pd
import pyscreenshot as ImageGrab


try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from PIL import Image, ImageTk
import pyscreenshot as ImageGrab

from subprocess import call


stri = "         Output-> "
chosen_option = "NO OPTION SELECTED"
choices = ['Team Members', '1505361', '1505205', '1505232', '1505137', '1505095']

class Application(Frame):

    def __init__(self,master):
        super().__init__(master)
        self.toolsThickness = 20
        self.rgb = "#%02x%02x%02x" % (255, 255, 255)
        self.cv = tk.Canvas(self)
        self.initUI()



    def initUI(self):

        self.frame = Frame(self,)
        self.master.title("Digit Recognition")
        self.pack(fill=BOTH, expand = True)
        #root.iconbitmap("Logo of Digit Recognition.ico")
        self.myCanvas = tk.Canvas(self, width = 800,height = 500,bg="black", borderwidth=5)
        self.myCanvas.grid(rowspan = 500,columnspan = 800)
        self.myCanvas.bind("<B1-Motion>", self.draw)
        self.myCanvas.bind("<Button-1>", self.setPreviousXY)

        self.img = tk.PhotoImage(file = "images/button.png")
        self.Button1 = Button(self, text = "Predict", width=30, command = self.Predict, image = self.img)
        self.Button1.grid(row = 80, column = 802)

        self.img2 = tk.PhotoImage(file = "images/button2.png")
        self.Button2 = Button(self, text = "Clear Screen", width=30, command=self.deleteAll, image = self.img2)
        self.Button2.grid(row = 120, column = 802)


        self.label2 = Label(self,width =20, text = stri, font=("Times New Roman", 16,"bold"))
        self.label2.grid(row = 160, column = 802)


        self.var = StringVar(self)
        self.var.set("Team Members:")

        self.box = ttk.Combobox(self, text = "Team:", values = choices, state = "readonly")
        self.box.set("Team members:")
        self.box.grid(row = 260, column = 802)

        self.button5 = Button(self,text = "Go", command = self.click)
        self.button5.grid(row =265,column = 802)

        self.label_chosen_variable= Label(self, text = chosen_option)
        self.label_chosen_variable.grid(row = 270, column = 802)

        self.img3 = PhotoImage(file = 'images/Final digit.png')
        self.label = Label(self, image = self.img3)
        self.label.grid(row = 50, column = 802)

    def click(self):
        chosen_option = self.box.get()
        if chosen_option == "1505205":
            chosen_option = "Name : CHAMPAK SINHA\nRoll no. : 1505205\nSection : CS3"
        elif chosen_option == "1505137":
            chosen_option = "Name : RISHAB\nRoll no. : 1505137\nSection : CS2"
        elif chosen_option == "1505232":
            chosen_option = "Name : PRANESH BISWAS\nRoll no. : 1505232\nSection : CS3"
        elif chosen_option == "1505095":
            chosen_option = "Name : ANISH HOTA\nRoll no. : 1505095\nSection : CS2"
        elif chosen_option == "1505361":
            chosen_option = "Name : ANAND KUMAR\nRoll no. : 1505361\nSection : CS5"

        self.label_chosen_variable.config(text = chosen_option)

    def setThickness(self, event):
        print("Thickness is set to 20")
        self.toolsThickness = 20

    def setPreviousXY(self, event):
            print("now")
            self.previousX = event.x
            self.previousY = event.y

    def draw(self, event):
        #line 2
        self.myCanvas.create_oval(event.x - self.toolsThickness,
                                  event.y - self.toolsThickness,
                                  event.x + self.toolsThickness,
                                  event.y + self.toolsThickness,
                                  fill = self.rgb, outline =""
                                  )

    def SAVE(self):
        print('\n def SAVECanvas(self):')
        canvas = self._canvas()  # Get Window Coordinates of Canvas
        self.grabcanvas = ImageGrab.grab(bbox=canvas).save("out_snapsave.jpg")
        print('Screenshot tkinter canvas and saved as "out_snapsave.jpg w/o displaying screenshot."')

    def _canvas(self):
        print('  def _canvas(self):')
        print('self.cv.winfo_rootx() = ', root.winfo_rootx())
        print('self.cv.winfo_rooty() = ', root.winfo_rooty())
        print('self.cv.winfo_x() =', root.winfo_x())
        print('self.cv.winfo_y() =', root.winfo_y())
        print('self.cv.winfo_width() = 1000')
        print('self.cv.winfo_height() =', root.winfo_height())
        x=root.winfo_rootx()+5
        y=root.winfo_rooty()+5
        x1=x+805
        y1=y+root.winfo_height()-11
        box=(x,y,x1,y1)
        print('box = ', box)
        return box

    def deleteAll(self):
        self.myCanvas.delete("all")
    
    def Predict(self):
        self.SAVE()
        custom_image_classification()
        file = open("output.txt","r")
        stri = "         Output-> " + file.read()
        print (stri)
        file.close()
        self.label2.config(text = stri)

def custom_image_classification():
    img = imageio.imread('out_snapsave.jpg')
    img = transform.resize(img, (28,28))
    img = img.astype(features_dtype)
    img = misc.bytescale(img)
    x_test = []
    for eachRow in img:
        for eachPixel in eachRow:
            x_test.append(eachPixel)
    x_test = np.array(x_test)
    #Binarization
    x_test[x_test<225]=0
    x_test[x_test>=225]=255
    #Removing rows
    x_test = x_test.reshape((28,28))
    del_arr=[]
    for i in range(len(x_test)):
        if 255 not in x_test[i]:
            del_arr.append(i)
    x_test = np.delete(x_test,del_arr,0)
    #Removing Columns
    x_test=x_test.T
    del_arr=[]
    for i in range(len(x_test)):
        if 255 not in x_test[i]:
            del_arr.append(i)
    x_test = np.delete(x_test,del_arr,0)
    x_test = x_test.T
    misc.imsave('error.jpg',x_test)
    img2 = Image.open('error.jpg')
    wpercent = (28/float(img2.size[0]))
    hsize = int((float(img2.size[1])*float(wpercent)))
    img3 = img2.resize((28,28),PIL.Image.ANTIALIAS)
    img3.save('error3.jpg',img2.format)

    img = imageio.imread('error3.jpg')
    img = transform.resize(img,(28,28))
    img = img.astype(features_dtype)
    img = misc.bytescale(img)
    img_test = []
    for eachRow in img:
        for eachPixel in eachRow:
            img_test.append(eachPixel)
    img_test = np.array(img_test)
    img_test = img_test.reshape([1,784])
    img_test[img_test<np.mean(img_test)]=0
    img_test[img_test>=np.mean(img_test)]=255
    file = open("output.txt","w+")
    file.write(str(int(classifier_model.predict(img_test)[0])))
    file.close()

if __name__ == '__main__':
    features_dtype = pd.Series.from_csv('features_dtypes.csv')
    classifier_model = pickle.load(open('final_model.sav','rb'))
    root = Tk()
    root.geometry("1055x514+300+300")
    root.resizable(width=False,height=False)    
    app = Application(root)
    root.mainloop()

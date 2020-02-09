from tkinter import *
from tkinter import ttk,filedialog
import cv2
from PIL import Image
import numpy
import os

ALFA = 0.0
frame_array=[]
newV = []
size=()
height, width, layers=0,0,0
imgURL=''
window = Tk() 
window.title("Procesamiento de imagenes")
window.geometry('380x240')
vidcap=''
count=1

def openVideo():
    global vidcap
    window.filename =  filedialog.askopenfilename(initialdir = "/Users/PC1/videos/",title = "Select file",filetypes = (("video files","*.mp4"),("all files","*.*")))
    imgURL= window.filename
    vidcap = cv2.VideoCapture(imgURL)
    print(window.filename)


def procesar():
    global count
    ALFA=float(entry.get())
    sec = 0
    frameRate = 0.4 #//it will capture image in each 0.2 second
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    FuncionFondo()
    convert_frames_to_video()

def getFrame(sec):
    global size
    global vidcap
    global count
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        name = './data/image'+str(count)+'.jpg'
        cv2.imwrite(name, image)     # save frame as JPG file
        img = cv2.imread(name)
        #print(img)
        frame_array.append(img)
        height, width, layers = img.shape
        size = (width,height)
    else: 
        success=False
        vidcap.release()
        print("Se acabaron las imagenes")
    return hasFrames

def convert_frames_to_video(): 
    global size
    pathOut = 'x.mp4'
    fps = 4
    print(size)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(newV)):
        # writing to a image array
        out.write(newV[i])
    out.release() 

def FuncionFondo():
    img = None
    for i in range(len(frame_array)):
        if i == 0:
            img = frame_array[i]
        else:
            ii = numpy.uint8(numpy.dot(img,(1-ALFA)))
            fi = numpy.uint8(numpy.dot(frame_array[i-1],ALFA))
            img = cv2.add(ii,fi)
            newV.append(img)
    c_array = numpy.asarray(img)
    imgx = Image.fromarray(img, 'RGB')
    imgx.save('my3.png')
    imgx.show()

lbl = Label(window, text="Introduce ALFA")
lbl.place(x=0, y=0)
entry = ttk.Entry(window)
entry.place(x=90, y=0)
btn = Button(window, text="Selecciona video",command=openVideo)
btn.place(x=260, y=0)



btn2 = Button(window, text="Procesar video",command=procesar)
btn2.place(x=160, y=80)

if __name__ == "__main__":
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')
    window.mainloop()
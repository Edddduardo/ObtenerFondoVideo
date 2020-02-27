from tkinter import *
from tkinter import ttk,filedialog
from time import time
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
cont2 = 0
initx = 0
inity = 0
names=[]
medidas=None
fragmento = None


def openVideo():
    global vidcap
    window.filename =  filedialog.askopenfilename(initialdir = "/Users/PC1/videos/",title = "Select file",filetypes = (("video files","*.mp4"),("all files","*.*")))
    imgURL= window.filename
    vidcap = cv2.VideoCapture(imgURL)
    print(window.filename)

def procesarDinamico():
    global cont2
    ALFA=float(entry.get())
    sec = 0
    frameRate = 0.5 #//it will capture image in each 0.2 second
    count=0
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    fragmento = getting_cut()
    ind = 0
    for im in frame_array:
        if ind == 0:
            ant = im
            ind+=1
        else:
            ps = get_background(im,fragmento)
            print("xs=",im.shape[1]," ys=", im.shape[0])
            print("de la imagen recortada x=",initx," y=",inity)
            print("de la imagen x=",ps[1]," y=",ps[0])
            x= initx-ps[1]
            y= inity-ps[0]
            m = numpy.float32([[1,0,x],[0,1,y]])
            dst = cv2.warpAffine(im,m,(im.shape[1],im.shape[0]))
            print("desplazamiento x=",x, " y = ",y)
            # align_image = alinear(im,x,y)
            ant = fondo(ant,dst)

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
    pathOut = 'videoEst.mp4'
    fps = 2
    print(size)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(newV)):
        # writing to a image array
        out.write(newV[i])
    out.release() 

def convert_frames_to_video2(): #Fondo dinamico 
    global size
    pathOut = './video/align.mp4'
    fps = 4
    print(size)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(newV)):
        # writing to a image array
        if i < 19:
            out.write(newV[i])
    out.release()

def get_background(image,fragmento): #sad
    x = 0
    y = 0
    difx = image.shape[1] - fragmento.shape[1]
    dify = image.shape[0] - fragmento.shape[0]
    print(difx)
    print(dify)
    cond = 99**99
    pos =[]
    for imy in range(image.shape[0] - fragmento.shape[0]):
        for imx in range(image.shape[1] - fragmento.shape[1]):
            result = 0
            #print(imx,imy)
            img = cutImage(image,imy,imx) #correlación
            #result = numpy.sum(numpy.abs(fragmento-img))
            result = numpy.sum((numpy.subtract(img,fragmento))**2)
            if result < cond:
                pos = imx,imy
                cond = result
            
    #print("x=",x,"  y=",y)
    return pos

def cutImage(imageN,ry,rx):  #Fondo dinamico
    global fragmento
    return imageN[int(ry):int(ry+fragmento.shape[0]),int(rx):int(rx+fragmento.shape[1])]
    
def alinear(imagen,x,y): #Fondo dinamico
    if x > 0:
        for d in range(x):
            imagen = numpy.delete(imagen,imagen.shape[1]-1,axis=1)
            imagen = numpy.insert(imagen,0,0,1)
    elif x < 0:
        for s in range(abs(x)):
            imagen = numpy.delete(imagen,0,axis=1)
            imagen = numpy.insert(imagen,imagen.shape[1]-1,0,1)
    if y > 0:
        for d in range(y):
            imagen = numpy.delete(imagen,imagen.shape[0]-1,axis=0)
            imagen = numpy.insert(imagen,0,0,0)
    elif y < 0:
        for s in range(abs(y)):
            imagen = numpy.delete(imagen,0,axis=0)
            imagen = numpy.insert(imagen,imagen.shape[0]-1,0,0)
    return imagen

def fondo(lastimg,image): #Fondo dinamico
    global cont2
    ii = numpy.uint8(numpy.dot(lastimg,(1-ALFA)))
    fi = numpy.uint8(numpy.dot(image,ALFA))
    img = cv2.add(ii,fi)
    newV.append(img)
    name = './ssd/image'+str(cont2)+'.jpg'
    qwerty = cv2.imwrite(name,img)
    cont2+=1
    print("imagen ", cont2)
    return img

def ValidaCorte(cut):  #Fondo dinamico
        x = cut[2]
        y = cut[3]
        if(x%2==0):
            x+=1
        if(y%2==0):
            y+=1
        return x,y

def CrearCorte(lastimg,xinitial,xfinish,yinitial,yfinish):  #Fondo dinamico
    return lastimg[int(yinitial):int(yinitial+yfinish),int(xinitial):int(xinitial+xfinish)]

def getting_cut(): #Fondo dinamico
    global initx, inity
    cut = cv2.selectROI(frame_array[0])
    cv2.destroyAllWindows()
    xy = ValidaCorte(cut)
    print(cut)
    initx = cut[1]
    inity = cut[0]
    fragmento = CrearCorte(frame_array[0],cut[0],xy[0],cut[1],xy[1])
    return fragmento

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
btn2 = Button(window, text="Procesar video estático",command=procesar)
btn2.place(x=160, y=80)
btn3 = Button(window, text="Procesar video dinámico",command=procesar)
btn3.place(x=160, y=120)

if __name__ == "__main__":
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')
    window.mainloop()
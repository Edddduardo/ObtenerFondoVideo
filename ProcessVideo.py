import cv2
from PIL import Image
import numpy
ALFA = 0.97
vidcap = cv2.VideoCapture('segs.mp4')
frame_array=[]
size=()
height, width, layers=0,0,0
def getFrame(sec):
    global size
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    
    if hasFrames:
        name = './data/image'+str(count)+'.jpg'
        cv2.imwrite(name, image)     # save frame as JPG file
        img = cv2.imread(name)
        frame_array.append(img)
        height, width, layers = img.shape
        size = (width,height)
    else: 
        vidcap.release()
        print("Se acabaron las imagenes")
    return hasFrames

def convert_frames_to_video(): 
    global size
    pathOut = 'video2.avi'
    fps = 4
    print(size)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release() 

def FuncionFondo():
    for i in range(len(frame_array)+1):
        if i < len(frame_array)-1: 
            I0 = numpy.array(frame_array[i-1],dtype=numpy.uint8)
            Ii = numpy.array(frame_array[i],dtype=numpy.uint8)
            Fi = (ALFA*I0) + ((1-ALFA)*Ii)
            if i == 1: 
                img = Image.fromarray(Fi, 'RGB')
                img.save('my.png')
                img.show()
            
        


if __name__ == "__main__": 
    sec = 0
    frameRate = 0.2 #//it will capture image in each 0.2 second
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    FuncionFondo()
    #convert_frames_to_video()

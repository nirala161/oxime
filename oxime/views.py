from django.shortcuts import render
from .models import Visitor
# Importing all necessary libraries
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from django.core.files.storage import FileSystemStorage

def change(request):
    return render(request,'oxime/maintain.html')

def framegenerate(video_name):

    cam = cv2.VideoCapture(video_name)
    #frames = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    #fps = int(cam.get(cv2.CAP_PROP_FPS))
    # calculate dusration of the video
    #seconds = int(frames / fps)
    #print(f"Video Duration ={seconds} sec")
    #try:
	    # creating a folder named data
	    #if not os.path.exists('data'):
		    #os.makedirs('data')
    # if not created then raise error
    #except OSError:
	    #print ('Error: Creating directory of data')
    # frame
    RED=np.array([])
    BLUE=np.array([])
    while(True):
	    # reading from frame
	    ret,frame = cam.read()
	    if ret:
                pic = frame
                a,b=0,0
                x=pic.shape[0]//2
                y=pic.shape[1]//2
                for i in range(x-10,x+10):
                    for j in range(y-10,y+10):
                        a=a+pic[i,j][0]
                        b=b+pic[i,j][2]
                t=400
                RED=np.append(RED,a/t)
                BLUE=np.append(BLUE,b/t)
	    else:
		    break
    a=100
    b=0.5
    ac_red=np.std(RED)
    dc_red=np.mean(RED)
    ac_blue=np.std(BLUE)
    dc_blue=np.mean(BLUE)
    #print(ac_red,dc_red,ac_blue,dc_blue)
    plt.plot(RED[10:])
    if os.path.exists("static/plot.jpg"):
        os.remove("static/plot.jpg")
    plt.savefig('static/plot.jpg')
    plt.close()
    pick=find_peaks(RED,distance = 13,height=dc_red-5)
    #print("picks at: ",pick[0])
    count=len(pick[0])
    #print("count =",count)
    #inplace seconds=20
    heart_beat=int((count*60)/20)
    #print("Pulse Rate =",heart_beat)

    if ac_blue==0:
        return "video is not prefect for spo2 detection",heart_beat
    spo2=(a-(b*((ac_red/dc_red)/(ac_blue/dc_blue))))
    #print("spo2 level =",spo2)
    cam.release()
    #cv2.destroyAllWindows()
    return spo2,heart_beat

def index(request):
    return render(request,'oxime/index.html',{'name':'raushan'})

# Create your views here.


def upload_data(request):
    process1=False
    process2=False
    if request.method == 'POST':

        uploaded_file = request.FILES['video']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        process1=True
        name=request.POST['name']
        spo2,pulse=framegenerate('media/'+uploaded_file.name)
        try:
            q=Visitor(name=name,spo2=spo2,pulse=pulse)
            q.save()
        except:
            pass
        process2=True
        context={'process1':process1,'process2':process2,'name':name,'spo2':spo2,'pulse':pulse}

        dir = 'media'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        return render(request,'oxime/final.html',context)

    return render(request,'oxime/detail.html')


def display(request):

    d = Visitor.objects.all()
    context ={
        'data':d,
    }
    return render(request,'oxime/data.html',context)


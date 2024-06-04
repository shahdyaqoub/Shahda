import cv2
import pickle
import cvzone
import numpy as np

#The Video
cap = cv2.VideoCapture('video/vid1.mp4')

with open('CarParkPos', 'rb') as f:  # rb is read binary
    posList = pickle.load(f)

width,height=72,17

def checkParkingSpace(imgProc):
    
    counterSpace=0
    
    for pos in posList:
        x,y=pos
        
        imgCrop=imgProc[y:y+height,x:x+width]
    #cv2.imshow("imgCropped",imgCrop) #يعرض صورة مكان المصف مقصوصة
        ###cv2.imshow(str(x*y),imgCrop) #يعرض كل الأماكن المحددة
        #cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 1)  # img,start,end,color,thickness
        countOfPix =cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(countOfPix),(x,y+height-2),
                           colorR=(0,0,0),scale=0.7,thickness=1,offset=0) #أوفسيت لتحريك النص لليمين والأسفل موجب ولليسار والأعلى سالب 
        
        if countOfPix<145:
            color = (0,255,0)  #Green
            thickness=2
            counterSpace+=1
        else:
            color = (0,0,255)    #Red
            thickness=1 
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)  # img,start,end,color,thickness
    #cvzone.putTextRect(img,str(counterSpace),(40,80),
                       #colorR=(0,79,0),scale=3,thickness=2,offset=12) #أوفسيت لتحريك النص لليمين والأسفل موجب ولليسار والأعلى سالب 
    cvzone.putTextRect(img,f'Free Spaces : {counterSpace} from {len(posList)}',(40,80),
                       colorR=(0,79,0),scale=3,thickness=2,offset=12) #أوفسيت لتحريك النص لليمين والأسفل موجب ولليسار والأعلى سالب 

        


while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    
    
    success,img=cap.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(1,1),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,  #max. value increase more white not gray
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16) #box size
    imgMedian = cv2.medianBlur(imgThreshold,3) #3 is Kernal like (1,1) #للتصفية الصورة وإزالة النقاط البيضاء الزائدة
    kernel = np.ones((3,3),np.uint8)
    imgDilation = cv2.dilate(imgMedian,kernel,iterations=1)  #سمك الحدود
    #for pos in posList:
        #cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 1)  # img,start,end,color,thickness


    checkParkingSpace(imgMedian)
    
    #for pos in posList:
     #   cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 1)  # img,start,end,color,thickness

    
    cv2.imshow('video', img)
    ###cv2.imshow('Image BLur', imgBlur)
    ###cv2.imshow('Image Threshold', imgThreshold)
    ###cv2.imshow('Image Median',imgMedian)
    ###cv2.imshow('Image Dilation',imgDilation)

    cv2.waitKey(3) #if waitkey     & 0xFF == ord('q'):    #كلما زاد waitkey يبطء الفيديو
                        #break

cap.release()
cv2.destroyAllWindows()


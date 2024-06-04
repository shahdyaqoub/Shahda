import cv2
import pickle   # pickle for store the position of the spaces


img = cv2.imread('Photos/img2.jpeg')

width,height=57,14

try:

    with open('CarParkPos', 'rb') as f:  # rb is read binary
        posList = pickle.load(f)
except:
    posList = []  #allspaces


def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:  # create pos
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)

    with open('CarParkPos','wb') as f :    # wb is write binry
        pickle.dump(posList,f)





while True:

    #cv2.rectangle(img,(260,423),(326,443),(255,0,255),2) #img,start,end,color,thickness

    img = cv2.imread('Photos/img2.jpeg')

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 1)  # img,start,end,color,thickness

    cv2.imshow("image",img)
    cv2.setMouseCallback("image",mouseClick)
    cv2.waitKey(1)
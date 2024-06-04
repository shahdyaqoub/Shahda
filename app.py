import cv2
import pickle
import cvzone
import numpy as np
from flask import Flask, Response

my_app = Flask(__name__)  # تمرير اسم الوحدة الحالية إلى كائن Flask

# Load the video
cap = cv2.VideoCapture('video/vid1.mp4')

# Load the car park positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 72, 17

def checkParkingSpace(imgProc, img):
    counterSpace = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgProc[y:y+height, x:x+width]
        countOfPix = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(countOfPix), (x, y+height-2),
                           colorR=(0, 0, 0), scale=0.7, thickness=1, offset=0)
        if countOfPix < 145:
            color = (0, 255, 0)  # Green
            thickness = 2
            counterSpace += 1
        else:
            color = (0, 0, 255)  # Red
            thickness = 1
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)
    cvzone.putTextRect(img, f'Free Spaces : {counterSpace} from {len(posList)}', (40, 80),
                       colorR=(0, 79, 0), scale=3, thickness=2, offset=12)

def generate_frames():
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        if not success:
            break
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (1, 1), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255,
                                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 3)
        kernel = np.ones((3, 3), np.uint8)
        imgDilation = cv2.dilate(imgMedian, kernel, iterations=1)
        checkParkingSpace(imgDilation, img)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@my_app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    my_app.run(debug=True)

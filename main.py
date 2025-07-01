# main.py
import cv2
import numpy as np
from HandTrackingModule import HandDetector
from VoiceModule import listen_command
from shapes import draw_shape
 
 
drawing_shape = False
shape_start = (0, 0)
selected_shape = None  # "rectangle", "circle", etc.

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.85)
drawColor = (255, 0, 255)  # Purple
brushThickness = 15
eraserThickness = 50
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

import threading

def voice_thread():
    global drawColor, selected_shape
    while True:
        cmd = listen_command()
        if "red" in cmd:
            drawColor = (0, 0, 255)
        elif "blue" in cmd:
            drawColor = (255, 0, 0)
        elif "green" in cmd:
            drawColor = (0, 255, 0)
        elif "purple" in cmd:
            drawColor = (255, 0, 255)
        elif "erase" in cmd or "eraser" in cmd:
            drawColor = (0, 0, 0)
        elif "circle" in cmd:
            selected_shape = "circle"
        elif "rectangle" in cmd:
            selected_shape = "rectangle"
        elif "save" in cmd:
            cv2.imwrite("canvas.jpg", imgCanvas)
            print("✅ Voice command saved canvas")

threading.Thread(target=voice_thread, daemon=True).start()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip

        fingers = []
        # Tip is higher than lower joint
        if lmList[8][2] < lmList[6][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        if lmList[12][2] < lmList[10][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Selection Mode – Two fingers up
        if fingers[0] and fingers[1]:
            xp, yp = 0, 0
            if y1 < 100:
                if 250 < x1 < 450:
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    drawColor = (0, 0, 0)  # Eraser

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[0] and not fingers[1]:
            if selected_shape:
               if not drawing_shape:
                  shape_start = (x1, y1)
            drawing_shape = True
        else:
            draw_shape(imgCanvas, selected_shape, shape_start, (x1, y1), drawColor, brushThickness)
            selected_shape = None
            drawing_shape = False
    else:
        cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
        if xp == 0 and yp == 0:
            xp, yp = x1, y1
        if drawColor == (0, 0, 0):
            cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
        else:
            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
        xp, yp = x1, y1


    # Merge canvas with video feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Draw header (toolbar)
    cv2.rectangle(img, (250, 0), (450, 100), (255, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (550, 0), (750, 100), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (800, 0), (950, 100), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (1050, 0), (1200, 100), (0, 0, 0), cv2.FILLED)

    cv2.imshow("Painter", img)
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

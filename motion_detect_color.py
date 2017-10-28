import cv2
import os.path
import time
import numpy as np
import imutils
import serial

ser = serial.Serial('/dev/ttyACM0',9600);
cam = cv2.VideoCapture(0)
#old_img_path = "old_image.png"
#cv2.namedWindow("Original")
#cv2.namedWindow("Color detection")
lower_range = np.array([100, 150, 0], dtype=np.uint8)
upper_range = np.array([140, 255, 255], dtype=np.uint8)
while(True):
    #cv2.imwrite(old_img_path, img_new)
    ret, img_new = cam.read()#capture
    hsv = cv2.cvtColor(img_new, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, None, iterations=2)
    res = cv2.bitwise_and(img_new, img_new, mask= mask)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.dilate(mask, None, iterations=3)


    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    if len(cnts) != 0:
        # compute the center of the contour
        c = max(cnts, key = cv2.contourArea)

        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        if (cv2.contourArea(c) > 2600):
            cv2.drawContours(img_new, [c], -1, (0, 255, 0), 2)
            cv2.circle(img_new, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(img_new, "center", (cX - 20, cY - 20),
            	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            width, height = mask.shape[:2]
            middle = width /2
            center_feutre = cX-80
            if(center_feutre-middle > 50):
                ser.write('1')
            elif(middle-center_feutre > 50):
                ser.write('2')
        else:
            print("0")


    #    if not ret:
    #        print "No ret\n"
        cv2.imshow("Original", img_new)
        cv2.imshow("Threshold", mask)
        cv2.imshow("Color detection", res)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cam.release()
cv2.destroyAllWindows()

import cv2 as cv
import numpy as np


class ColorDetector:
    def __init__(self):

        self.yellow = 25
        self.green = 45
        self.blueS = 105
        self.blueL = 94
        self.pink = 169
        self.purple = 139

    def DameValores(self):
        return self.yellow, self.green, self.blueS, self.blueL, self.pink, self.purple

    def TomaValores(self):
        self.yellow = int(self.yellowtmp)
        self.green = int(self.greentmp)
        self.blueS = int(self.blueStmp)
        self.blueL = int(self.blueLtmp)
        self.pink = int(self.pinktmp)
        self.purple = int(self.purpletmp)

    def MarkFrameForCalibration(self, frame):
        x1, x2, x3 = 105, 315, 525
        y1, y2 = 120, 360
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        self.yellowtmp = hsv[y1, x1][0]
        self.greentmp = hsv[y1, x2][0]
        self.blueStmp = hsv[y1, x3][0]
        self.blueLtmp = hsv[y2, x1][0]
        self.pinktmp = hsv[y2, x2][0]
        self.purpletmp = hsv[y2, x3][0]

        cv.circle(frame, (x1, y1), 100, (0, 255, 255), 3)
        cv.putText(
            img=frame,
            text=str(self.yellowtmp),
            org=(x1 - 50, y1),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=2,
            color=(255, 255, 255),
            thickness=1,
        )

        cv.circle(frame, (x2, y1), 100, (0, 255, 0), 3)
        cv.putText(
            img=frame,
            text=str(self.greentmp),
            org=(x2 - 50, y1),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=2,
            color=(255, 255, 255),
            thickness=1,
        )

        cv.circle(frame, (x3, y1), 100, (240, 106, 23), 3)
        cv.putText(
            img=frame,
            text=str(self.blueStmp),
            org=(x3 - 50, y1),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=2,
            color=(255, 255, 255),
            thickness=1,
        )

        cv.circle(frame, (x1, y2), 100, (250, 240, 30), 3)
        cv.putText(
            img=frame,
            text=str(self.blueLtmp),
            org=(x1 - 50, y2),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=2,
            color=(255, 255, 255),
            thickness=1,
        )

        cv.circle(frame, (x2, y2), 100, (139, 1, 240), 3)
        cv.putText(
            img=frame,
            text=str(self.pinktmp),
            org=(x2 - 50, y2),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=2,
            color=(255, 255, 255),
            thickness=1,
        )

        cv.circle(frame, (x3, y2), 100, (240, 29, 140), 3)
        cv.putText(
            img=frame,
            text=str(self.purpletmp),
            org=(x3 - 50, y2),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=2,
            color=(255, 255, 255),
            thickness=1,
        )
        return frame

    def DetectColor(self, frame):

        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        print (hsv[240,315][0])
        marge = 5

        # define range of colors in HSV
        lowerYellow = np.array([self.yellow - marge, 50, 50])
        upperYellow = np.array([self.yellow + marge, 255, 255])

        lowerGreen = np.array([self.green - marge, 50, 50])
        upperGreen = np.array([self.green + marge, 255, 255])

        lowerBlueS = np.array([self.blueS - marge, 50, 50])
        upperBlueS = np.array([self.blueS + marge, 255, 255])

        lowerBlueL = np.array([self.blueL - marge, 50, 50])
        upperBlueL = np.array([self.blueL + marge, 255, 255])

        lowerPink = np.array([self.pink - marge, 50, 50])
        upperPink = np.array([self.pink + marge, 255, 255])

        lowerPurple = np.array([self.purple - marge, 50, 50])
        upperPurple = np.array([self.purple + marge, 255, 255])

        detectedColour = "none"

        # ignore selected contour with area less that this
        minimumSize = 0

        areaBiggestContour = 0

        # for each color:
        #   find contours of this color
        #   get the biggest contour
        #   check if the contour is within the target rectangle (if area = 'small')
        #   check if the contour has the minimun area
        #   keet this contour if it is the biggest by the moment

        mask = cv.inRange(hsv, lowerYellow, upperYellow)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        if len(contours) > 0:
            cyellow = max(contours, key=cv.contourArea)
            if cv.contourArea(cyellow) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cyellow)
                detectedColour = "yellow"
        mask = cv.inRange(hsv, lowerGreen, upperGreen)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        if len(contours) > 0:
            cGreen = max(contours, key=cv.contourArea)

            if cv.contourArea(cGreen) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cGreen)
                detectedColour = "green"

        mask = cv.inRange(hsv, lowerBlueS, upperBlueS)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        if len(contours) > 0:
            cBlueS = max(contours, key=cv.contourArea)

            if cv.contourArea(cBlueS) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cBlueS)
                detectedColour = "blueS"

        mask = cv.inRange(hsv, lowerBlueL, upperBlueL)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        if len(contours) > 0:
            cBlueL = max(contours, key=cv.contourArea)

            if cv.contourArea(cBlueL) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cBlueL)
                detectedColour = "blueL"

        mask = cv.inRange(hsv, lowerPink, upperPink)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        if len(contours) > 0:
            cPink = max(contours, key=cv.contourArea)

            if cv.contourArea(cPink) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cPink)
                detectedColour = "pink"

        mask = cv.inRange(hsv, lowerPurple, upperPurple)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        if len(contours) > 0:
            cPurple = max(contours, key=cv.contourArea)

            if cv.contourArea(cPurple) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cPurple)
                detectedColour = "purple"

        if detectedColour != "none" and areaBiggestContour > minimumSize:
            cv.putText(
                img=frame,
                text=detectedColour,
                org=(50, 50),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=2,
                color=(255, 255, 255),
                thickness=1,
            )
        return frame, detectedColour

import math

import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

path = "Videos/vid (4).mp4"
# initialize
cap = cv2.VideoCapture(path)

# create the color finder object
my_color_finder = ColorFinder(False)  # True - find color; False - run mode

# hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 255, 'smax': 255, 'vmax': 255}
hsv_vals = {'hmin': 0, 'smin': 130, 'vmin': 95, 'hmax': 17, 'smax': 255, 'vmax': 255}

# variables
pos_list_x, pos_list_y = [], []
x_list = [item for item in range(0, 1300)]  # width
# a, b, c = 0, 0, 0

while True:
    # grab image
    ret, img = cap.read()

    # loop video
    if not ret:
        cap = cv2.VideoCapture(path)
        ret, img = cap.read()
        pos_list_x.clear()
        pos_list_y.clear()

    # img for find color
    # img = cv2.imread("Ball.png")

    # crop the image
    img = img[0:900, :]

    # find the ball's color
    img_color, mask = my_color_finder.update(img, hsv_vals)

    # find contours
    img, contours = cvzone.findContours(img, mask, minArea=500)

    if contours:
        # biggest contours
        pos_list_x.append(contours[0]["center"][0])
        pos_list_y.append(contours[0]["center"][1])

    if pos_list_x:
        # polynomial regression y = ax^2 + bx + c
        # find coefficients
        a, b, c = np.polyfit(pos_list_x, pos_list_y, 2)  # (list_x, list_y, order)

        # draw points and line
        for i, (pos_x, pos_y) in enumerate(zip(pos_list_x, pos_list_y)):
            pos = (pos_x, pos_y)
            cv2.circle(img, pos, 10, (0, 255, 0), cv2.FILLED)
            if not i == 0:
                cv2.line(img, pos, (pos_list_x[i - 1], pos_list_y[i - 1]), (255, 0, 0), 5)

        for x in x_list:
            y = int(a * x ** 2 + b * x + c)
            cv2.circle(img, (x, y), 2, (0, 0, 0), cv2.FILLED)

        # prediction
        # x val = 330 to 430
        # y = 590

        c = c - 590

        x = -b - math.sqrt(b ** 2 - (4 * a * c)) / (2 * a)

        if 330 < x < 430:
            print("basket")
        else:
            print("no basket")

    # display
    img = cv2.resize(img, (0, 0), None, 0.7, 0.7)
    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(100) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

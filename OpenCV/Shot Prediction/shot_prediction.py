import math

import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

path = "Videos/vid (1).mp4"
# initialize
cap = cv2.VideoCapture(path)

# create the color finder object
my_color_finder = ColorFinder(False)  # True - find color; False - run mode

# hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 255, 'smax': 255, 'vmax': 255}
hsv_vals = {'hmin': 0, 'smin': 130, 'vmin': 95, 'hmax': 17, 'smax': 255, 'vmax': 255}

# variables
pos_list_x, pos_list_y = [], []
x_list = [item for item in range(0, 1300)]  # width
prediction = ""
colorT, colorR = (0, 0, 0), (0, 0, 0)
cnt = 1

while True:
    # grab image
    ret, img = cap.read()

    # loop video
    if not ret:
        if cnt >= 7:
            cnt = 1
        else:
            cnt += 1
        path = f'Videos/vid ({cnt}).mp4'
        cap = cv2.VideoCapture(path)
        ret, img = cap.read()
        pos_list_x.clear()
        pos_list_y.clear()
        print(path)

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

        if len(pos_list_x) < 10:  # predict only in the first 9 frames

            # prediction
            # x val = 330 to 430
            # y = 590

            c = c - 590

            x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
            # print(x)

            if 320 < x < 430:
                prediction = "BASKET"
                colorT = (255, 255, 255)
                colorR = (0, 200, 0)
                # cvzone.putTextRect(img, "BASKET", (50, 150), 5, 5, colorT=(255, 255, 255), colorR=(0, 200, 0),
                #                    offset=20)
                # print("basket")
            else:
                prediction = "NO BASKET"
                colorT = (255, 255, 255)
                colorR = (0, 0, 200)
                # cvzone.putTextRect(img, "NO BASKET", (50, 150), 5, 5, colorT=(255, 255, 255), colorR=(0, 0, 200),
                #                    offset=20)
                # print("no basket")

        cvzone.putTextRect(img, prediction, (50, 150), 5, 5, colorT, colorR,
                           offset=20)

        if len(pos_list_x) == 10:
            cv2.waitKey()

    # display
    cvzone.putTextRect(img, path, (50, 850), 1, 1, (0, 0, 0), (255, 255, 255),
                       offset=10)
    img = cv2.resize(img, (0, 0), None, 0.7, 0.7)
    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(100) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

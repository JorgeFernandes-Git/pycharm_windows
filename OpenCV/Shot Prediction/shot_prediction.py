import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

path = "Videos/vid (3).mp4"
# initialize
cap = cv2.VideoCapture(path)

# create the color finder object
my_color_finder = ColorFinder(False)  # True - find color; False - run mode

# hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 255, 'smax': 255, 'vmax': 255}
hsv_vals = {'hmin': 0, 'smin': 130, 'vmin': 95, 'hmax': 17, 'smax': 255, 'vmax': 255}

# variables
pos_list = []

while True:
    # grab image
    ret, img = cap.read()

    # loop video
    if not ret:
        cap = cv2.VideoCapture(path)
        ret, img = cap.read()
        pos_list.clear()

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
        pos_list.append(contours[0]["center"])

    for i, pos in enumerate(pos_list):
        cv2.circle(img, pos, 5, (0, 255, 0), cv2.FILLED)
        if not i == 0:
            cv2.line(img, pos, pos_list[i - 1], (255, 0, 0), 1)


    # display
    img = cv2.resize(img, (0, 0), None, 0.7, 0.7)
    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(100) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

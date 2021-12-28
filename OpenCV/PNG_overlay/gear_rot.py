import cv2
import cvzone
import numpy as np

angle = 0

fps = cvzone.FPS()


def empty(a):
    pass


cv2.namedWindow("image")
cv2.resizeWindow("image", 640, 100)
cv2.createTrackbar("speed", "image", 1, 25, empty)

while True:
    img_back = np.ones((500, 800, 3), np.uint8) * 255
    img_front = cv2.imread("gear.png", cv2.IMREAD_UNCHANGED)
    img_front_copy = img_front.copy()

    speed = cv2.getTrackbarPos("speed", "image")

    img_front = cvzone.rotateImage(img_front, angle+23)
    img_front_copy = cvzone.rotateImage(img_front_copy, -angle)

    angle += speed

    img_result = cvzone.overlayPNG(img_back, img_front, [125, 100])
    img_result = cvzone.overlayPNG(img_result, img_front_copy, [400, 100])
    _, img_result = fps.update(img_result)

    cv2.imshow("image", img_result)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

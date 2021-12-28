import cv2
import cvzone
import numpy as np

img_back = cv2.imread("nature.jpg")
# img_back = np.ones((480, 640, 3), np.uint8)*255  # black without *255
img_front = cv2.imread("gear.png", cv2.IMREAD_UNCHANGED)
img_front = cv2.resize(img_front, (0, 0), None, 0.5, 0.5)

img_result = cvzone.overlayPNG(img_back, img_front, [150, 150])

cv2.imshow("image", img_result)
cv2.waitKey(0)

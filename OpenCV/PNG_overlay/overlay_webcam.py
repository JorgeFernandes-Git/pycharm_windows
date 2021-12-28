import cv2
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
_, img = cap.read()

img_front = cv2.imread("logo.png", cv2.IMREAD_UNCHANGED)
img_front = cv2.resize(img_front, (0, 0), None, 0.25, 0.25)

hf, wf, cf = img_front.shape
hb, wb, cb = img.shape

fps = cvzone.FPS()

while True:
    _, img = cap.read()

    img_result = cvzone.overlayPNG(img, img_front, [0, hb-hf])
    _, img_result = fps.update(img_result)
    cv2.imshow("image", img_result)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

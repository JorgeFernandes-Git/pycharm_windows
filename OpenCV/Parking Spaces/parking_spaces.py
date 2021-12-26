import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture("carPark.mp4")

with open("CarParkPos", "rb") as f:
    pos_list = pickle.load(f)

width, height = 107, 48  # 157-50, 240-192


def check_space():
    for pos in pos_list:
        x, y = pos

        img_crop = img[y:y + height, x:x + width]
        cv2.imshow(str(x * y), img_crop)


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 25, 16)

    check_space()

    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("image", img)
    cv2.imshow("blur", blur)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture("carPark.mp4")

with open("CarParkPos", "rb") as f:
    pos_list = pickle.load(f)

width, height = 107, 48  # 157-50, 240-192


def check_space(img_process):
    for pos in pos_list:
        x, y = pos

        img_crop = img_process[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), img_crop)
        count = cv2.countNonZero(img_crop)  # number of pixels in the area
        cvzone.putTextRect(img, str(count), (x, y + height - 5), scale=1.2, offset=0, thickness=1)


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    _, img = cap.read()

    # grab cars in space
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(median, kernel, 1)

    check_space(dilate)

    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("image", img)
    # cv2.imshow("blur", blur)
    # cv2.imshow("thresh", threshold)
    # cv2.imshow("median", median)
    # cv2.imshow("dilate", dilate)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

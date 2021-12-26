import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture("carPark.mp4")

with open("CarParkPos", "rb") as f:
    pos_list = pickle.load(f)

width, height = 107, 48  # 157-50, 240-192


def empty(a):
    pass


# trackbars
cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)


def check_space(img_process):
    space_cnt = 0
    for pos in pos_list:
        x, y = pos

        img_crop = img_process[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), img_crop)
        count = cv2.countNonZero(img_crop)  # number of pixels in the area

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            text = (0, 0, 0)
            space_cnt += 1
        else:
            color = (0, 0, 255)
            thickness = 2
            text = (255, 255, 255)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 5),
                           scale=1.2, offset=0, thickness=1, colorR=color, colorT=text)

    cvzone.putTextRect(img, f'free: {str(space_cnt)}/{len(pos_list)}', (100, 50),
                       scale=4, offset=20, thickness=5, colorR=(0, 200, 0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    _, img = cap.read()

    # grab cars in space
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1

    threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, val1, val2)
    median = cv2.medianBlur(threshold, val3)
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(median, kernel, 1)

    check_space(dilate)

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

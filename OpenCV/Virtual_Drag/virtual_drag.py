import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import os


class DragImage:
    def __init__(self, path, pos_origin, type):
        self.path = path
        self.pos_origin = pos_origin
        self.type = type

        if self.type == "png":
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.img = cv2.resize(self.img, (273, 286))  # resize images
        self.size = self.img.shape[:2]  # only the first 2 parameters

    def update(self, cursor):
        ox, oy = self.pos_origin
        h, w = self.size

        #         # check if cursor is in image region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.pos_origin = cursor[0] - w // 2, cursor[1] - h // 2


cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
detector = HandDetector(detectionCon=0.8)

# img_move = cv2.imread("Images/linux.png", cv2.IMREAD_UNCHANGED)
# img_move = cv2.resize(img_move, (273, 286))
# ox, oy = 200, 200

path = 'Images'
my_list = os.listdir(path)
# print(my_list)

img_list = []
for i, path_img in enumerate(my_list):
    if "png" in path_img:
        img_type = "png"
    else:
        img_type = "jpg"
    img_list.append(DragImage(f'{path}/{path_img}', [i * 200 + 50, 50], img_type))

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    # h, w, _ = img_move.shape

    # hand detection
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lm_list = hands[0]["lmList"]

        length, info, img = detector.findDistance(lm_list[8], lm_list[12], img)
        # print(length)

        if length < 50:  # check is click
            cursor = lm_list[8]
            for img_obj in img_list:
                img_obj.update(cursor)

    try:

        for img_obj in img_list:
            h, w = img_obj.size
            ox, oy = img_obj.pos_origin

            if img_obj.type == "png":
                # PNG images
                img = cvzone.overlayPNG(img, img_obj.img, [ox, oy])
            else:
                # JPG images
                img[oy:oy + h, ox:ox + w] = img_obj.img

    except ValueError:
        pass

    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

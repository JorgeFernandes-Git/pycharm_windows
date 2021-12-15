import cv2
from cvzone.HandTrackingModule import HandDetector

# mediapipe 0.8.7
# cvzone 1.4.1

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (255, 0, 255),
                      cv2.FILLED)
        cv2.putText(img, self.text, (self.pos[0] + 20, self.pos[1] + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "/"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "-"]]

btn_list = []
for x in range(0, 10):  # ten horizontal keys
    for y in range(0, 3):  # three rows
        btn_list.append(Button([200 * x + 50, 100*y+150], keys[y][x]))

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lm_list, bbox_info = detector.findPosition(img)

    for btn in btn_list:
        img = btn.draw(img)

    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

import cv2
from cvzone.HandTrackingModule import HandDetector

# cvzone 1.5.3
# mediapipe 0.8.9.1


class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

    def draw(self, img):
        overlay = img.copy()
        cv2.rectangle(overlay, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (255, 0, 255),
                      cv2.FILLED)
        alpha = 0.4
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)  # add transparency
        cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (0, 0, 0),
                      2)
        cv2.putText(img, self.text, (self.pos[0] + 20, self.pos[1] + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img

    def click_check(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.size[0] and self.pos[1] < y < self.pos[1] + self.size[1]:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (0, 255, 0),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (0, 0, 0),
                          2)
            cv2.putText(img, self.text, (self.pos[0] + 20, self.pos[1] + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
            return True
        else:
            return False

    def over_key(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.size[0] and self.pos[1] < y < self.pos[1] + self.size[1]:
            cv2.rectangle(img, (self.pos[0], self.pos[1]), (self.pos[0] + self.size[0], self.pos[1] + self.size[1]),
                          (175, 0, 175),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (0, 0, 0),
                          2)
            cv2.putText(img, btn.text, (self.pos[0] + 20, self.pos[1] + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)


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
        btn_list.append(Button([100 * x + 150, 100 * y + 100], keys[y][x]))

# ------------------------------- variables
delay_cnt = 0
write_text = ""

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 0 - x, 1 - y

    # hand detection
    hands, img = detector.findHands(img, flipType=False)

    # ------------------------------- draw buttons
    for btn in btn_list:
        img = btn.draw(img)

    # create write area
    overlay = img.copy()
    cv2.rectangle(overlay, (150, 600), (150 + 1000, 600 + 85), (255, 0, 255), cv2.FILLED)
    alpha = 0.4
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)  # add transparency
    cv2.rectangle(img, (150, 600), (150 + 1000, 600 + 85), (0, 0, 0), 2)

    # ------------------------------- check for hand
    if hands:
        lm_list = hands[0]["lmList"]
        length, _, img = detector.findDistance(lm_list[8], lm_list[12], img)  # dist between index and middle fingertips
        fingers = detector.fingersUp(hands[0])
        # print(*fingers)

        x_tip, y_tip = lm_list[8]  # locations of the tip in x_tip and y
        # print(length)

        if length < 40:
            for btn in btn_list:
                if btn.click_check(x_tip, y_tip) and delay_cnt == 0:  # true from the method
                    my_value = btn.text  # get the clicked key in the list
                    # print(my_value)
                    write_text += my_value
                    delay_cnt = 1  # delay to avoid duplication
        else:
            for btn in btn_list:
                btn.over_key(x_tip, y_tip)

        # clear text -- close hand
        if fingers == [0, 0, 0, 0, 0]:
            write_text = ""

        # add space -- index and pinky finger up \m/
        if fingers == [0, 1, 0, 0, 1] and delay_cnt == 0:
            write_text += " "
            delay_cnt = 1

    # ------------------------------- avoid duplication
    if not delay_cnt == 0:
        delay_cnt += 1
        if delay_cnt > 10:
            delay_cnt = 0

    # ------------------------------- display text
    cv2.putText(img, write_text, (160, 650), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    # ------------------------------- display image
    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

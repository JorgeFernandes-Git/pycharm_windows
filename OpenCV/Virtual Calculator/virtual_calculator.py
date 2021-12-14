import cv2
from cvzone.HandTrackingModule import HandDetector


# class for creating the buttons
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 35, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 2)

    def click_check(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),
                        5)
            return True
        else:
            return False


# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# hand object from cvzone library
detector = HandDetector(detectionCon=0.8, maxHands=1)  # one hand with high confidence

# ------------------------------- create buttons
button_list_values = [["7", "8", "9", "*"],
                      ["4", "5", "6", "-"],
                      ["1", "2", "3", "+"],
                      ["0", ".", "/", "="]]

button_list = []
for x in range(4):
    for y in range(4):
        x_pos = x * 100 + 800
        y_pos = y * 100 + 150
        button_list.append(Button((x_pos, y_pos), 100, 100, button_list_values[y][x]))

# ------------------------------- variables
my_equation = ""
delay_cnt = 0

# ------------------------------- loop
while True:
    # get image
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 0 - x, 1 - y

    # hand detection
    hands, img = detector.findHands(img, flipType=False)

    # ------------------------------- draw buttons
    # results box
    cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 70), (800 + 400, 70 + 150), (50, 50, 50), 3)

    # clear box
    cv2.rectangle(img, (800, 550), (800 + 400, 550 + 50), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 550), (800 + 400, 550 + 50), (50, 50, 50), 3)
    cv2.putText(img, "CLEAR", (800 + 125, 550 + 40), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # numbers and signs boxes
    for button in button_list:
        button.draw(img)

    # ------------------------------- check for hand
    if hands:  # hands are from the method findHands
        lm_list = hands[0]["lmList"]
        length, _, img = detector.findDistance(lm_list[8], lm_list[12], img)  # dist between index and middle fingertips

        # print(length)
        x, y = lm_list[8]  # locations of the tip in x and y

        # clear box location
        x_clear = 800
        y_clear = 550

        # click mode
        if length < 40:

            # check button
            for i, button in enumerate(button_list):
                if button.click_check(x, y) and delay_cnt == 0:  # true from the method
                    my_value = (button_list_values[int(i % 4)][int(i / 4)])  # get the clicked number in the list

                    if my_value == "=":
                        try:
                            my_equation = str(eval(my_equation))  # eval is a method to do the math in the parenthesis
                            # print(eval("5+5"))  # this is an example of eval method
                        except:
                            my_equation = "ERROR"
                    else:
                        my_equation += my_value
                    delay_cnt = 1  # delay to avoid duplication

            # clear
            if x_clear < x < x_clear + 400 and y_clear < y < y_clear + 50:
                my_equation = ""
                cv2.rectangle(img, (800, 550), (800 + 400, 550 + 50), (255, 0, 0), cv2.FILLED)
                cv2.rectangle(img, (800, 550), (800 + 400, 550 + 50), (50, 50, 50), 3)
                cv2.putText(img, "CLEAR", (800 + 125, 550 + 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # ------------------------------- avoid duplication
    if not delay_cnt == 0:
        delay_cnt += 1
        if delay_cnt > 10:
            delay_cnt = 0

    # ------------------------------- display the equation/results
    if len(my_equation) > 10:
        my_equation = my_equation[0:13]  # limit the numbers
    cv2.putText(img, my_equation, (810, 125), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # ------------------------------- display image
    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

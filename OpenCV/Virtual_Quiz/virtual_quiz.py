import csv
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)


class QuestionClass:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])  # to verify if it's correct answer

        self.user_answer = None  # verify if the user choose a answer


# import csv file data
path_csv = "questions.csv"
with open(path_csv, newline="\n") as f:
    reader = csv.reader(f)
    data_total = list(reader)[1:]  # ignore the first row

# create object for each question
questions_list = []
for q in data_total:
    questions_list.append(QuestionClass(q))

q_num = 0
q_total = len(data_total)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    question_simple = questions_list[0]
    img, bbox = cvzone.putTextRect(img, question_simple.question, [100, 100], 2, 2, offset=50, border=5,
                                   colorB=(255, 255, 255), colorR=(0, 0, 0))

    cv2.imshow("Image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

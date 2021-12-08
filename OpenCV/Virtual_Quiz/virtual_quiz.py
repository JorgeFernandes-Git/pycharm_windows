import csv
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time


class QuestionClass:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])  # to verify if it's correct answer

        self.user_answer = None  # verify if the user choose a answer

    def update(self, cursor_c, bboxs_c):
        bbox_list = []
        for x, bbox_c in enumerate(bboxs_c):
            # bbox_list.append(bbox_c)
            x1_c, y1_c, x2_c, y2_c = bbox_c
            if x1_c < cursor_c[0] < x2_c and y1_c < cursor_c[1] < y2_c:
                self.user_answer = x + 1  # x + 1 because of the csv format
                cv2.rectangle(img, (x1_c, y1_c), (x2_c, y2_c), (0, 255, 0), cv2.FILLED)  # green box to show the click
                # print("user: ", self.user_answer)
                # print("correct: ", self.answer)
                if self.user_answer != self.answer:
                    # x1_ans, y1_ans, x2_ans, y2_ans = bbox_list[self.answer]
                    # cv2.rectangle(img, (x1_ans, y1_ans), (x2_ans, y2_ans), (255, 0, 0), cv2.FILLED)
                    print("incorrect")
                else:
                    print("correct")
        # print(bbox_list)


"""
Initialization
"""
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
detector = HandDetector(detectionCon=0.8)

# import csv file data
path_csv = "questions.csv"
with open(path_csv, newline="\n") as f:
    reader = csv.reader(f)
    data_total = list(reader)[1:]  # ignore the first row

# create object for each question
questions_list = []
for q in data_total:
    questions_list.append(QuestionClass(q))

# total number of questions read
q_num = 0
q_total = len(data_total)

# variable flags
user_resp = False

# variables
question_simple = ""

"""
Processing
"""
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # iterate through all questions
    if q_num < q_total:
        question_simple = questions_list[q_num]
        # question_simple.user_answer = None
        img, bbox = cvzone.putTextRect(img, question_simple.question, [100, 100], 2, 2, offset=30, border=5,
                                       colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox1 = cvzone.putTextRect(img, question_simple.choice1, [100, 200], 2, 2, offset=30, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox2 = cvzone.putTextRect(img, question_simple.choice2, [450, 200], 2, 2, offset=30, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox3 = cvzone.putTextRect(img, question_simple.choice3, [100, 300], 2, 2, offset=30, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox4 = cvzone.putTextRect(img, question_simple.choice4, [450, 300], 2, 2, offset=30, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))

        if hands:  # hands are from the method findHands
            lm_list = hands[0]["lmList"]
            cursor = lm_list[8]  # tip of the index by mediapipe
            length, info = detector.findDistance(lm_list[8], lm_list[12])  # dist between index and middle fingertips

            # click mode
            if length < 60:
                question_simple.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                # print(question_simple.user_answer)
                if question_simple.user_answer is not None:
                    print(question_simple.user_answer)
                    user_resp = True

            if length > 80 and user_resp:
                q_num += 1
                user_resp = False

    else:  # after all questions
        score = 0
        results_list = []
        for i, question_simple in enumerate(questions_list):
            if question_simple.answer == question_simple.user_answer:
                score += 1
                results_list.append(f'Question {i+1} correct')
            else:
                results_list.append(f'Question {i+1} incorrect')
        score = round((score / q_total) * 100, 2)
        # print(results_list)

        # final screen
        # img, _ = cvzone.putTextRect(img, f'Quiz Complete', [250, 300], 2, 2, offset=50,
        #                             border=5, colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        # score box
        img, _ = cvzone.putTextRect(img, f'Your Score: {score} %', [460, 300], 2, 2, offset=50,
                                    border=5, colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        # play again box
        img, bbox_p_again = cvzone.putTextRect(img, f'Play Again', [500, 500], 3, 2, offset=50,
                                               border=5, colorB=(255, 255, 255), colorR=(0, 0, 0),
                                               colorT=(255, 255, 255))

        # results
        results_dist = 0
        for i, result in enumerate(results_list):
            img, _ = cvzone.putTextRect(img, str(result), [70, (100+results_dist)], 1, 1, offset=5,
                                        border=0, colorB=(255, 255, 255), colorR=(0, 0, 0),
                                        colorT=(255, 255, 255))
            results_dist += 30
            # print(results_dist)

        # play again
        if hands:  # hands are from the method findHands
            lm_list = hands[0]["lmList"]
            cursor = lm_list[8]  # tip of the index by mediapipe
            length, info = detector.findDistance(lm_list[8], lm_list[12])  # dist between index and middle fingertips
            x1, y1, x2, y2 = bbox_p_again  # box position

            # click play again
            if length < 60 and x1 < cursor[0] < x2 and y1 < cursor[1] < y2:  # cursor[0], cursor[1] = x, y
                q_num = 0
                question_simple.user_answer = None
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)  # green box to show the click
                # time.sleep(2)

    # draw progress bar
    bar_value = 70 + ((1100 - 70) // q_total) * q_num
    cv2.rectangle(img, (70, 600), (bar_value, 650), (0, 255, 0), cv2.FILLED)  # fill bar
    cv2.rectangle(img, (70, 600), (1100, 650), (255, 255, 255), 5)  # outer rectangle
    img, _ = cvzone.putTextRect(img, f'{round((q_num / q_total) * 100)} %', [1130, 635], 2, 2, offset=16,
                                border=5, colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
    img, _ = cvzone.putTextRect(img, f'Question: {q_num}', [86, 560], 2, 2, offset=16,
                                border=5, colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))

    cv2.imshow("Image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

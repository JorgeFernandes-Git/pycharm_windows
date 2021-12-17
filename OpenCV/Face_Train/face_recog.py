import os
import cv2
import numpy as np

DIR = r'D:\Projetos\Pycharm\pycharm_windows\OpenCV\Face_Train\images'
haar_cascade = cv2.CascadeClassifier("haar_face.xml")

people = []
for i in os.listdir(DIR):
    people.append(i)

features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy')

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

img = cv2.imread(r'D:\Projetos\Pycharm\pycharm_windows\OpenCV\Face_Train\images\Madonna\madona (2).png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Person', gray)

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

for (x, y, w, h) in faces_rect:
    faces_roi = gray[y:y + h, x:x + w]

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label = {people[label]} with a confidence of {confidence}')

    cv2.putText(img, str(people[label]), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

cv2.imshow("Detected Face", img)

cv2.waitKey(0)

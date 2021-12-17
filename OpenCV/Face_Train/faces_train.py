import os
import cv2
import numpy as np

DIR = r'D:\Projetos\Pycharm\pycharm_windows\OpenCV\Face_Train\images'

people = []
for i in os.listdir(DIR):
    people.append(i)

features = []
labels = []


def create_train():
    for person in people:
        path = os.path.join(DIR,person)
        label = people.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv2.imread(img_path)
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)


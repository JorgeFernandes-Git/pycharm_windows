import cv2

img = cv2.imread("D:\Projetos\Pycharm\pycharm_windows\OpenCV\Face_Train\images\Ben Afflek\download (1).png")
cv2.imshow("Person", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)

haar_cascade = cv2.CascadeClassifier("haar_face.xml")

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

for (x, y, w, h) in faces_rect:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

cv2.imshow("Detected Faces", img)

cv2.waitKey(0)

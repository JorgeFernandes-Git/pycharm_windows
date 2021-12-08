import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    # ESC to close
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
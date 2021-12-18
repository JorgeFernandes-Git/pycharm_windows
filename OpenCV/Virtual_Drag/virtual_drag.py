import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

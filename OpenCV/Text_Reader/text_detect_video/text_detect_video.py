import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

while True:
    _, img = cap.read()
    # img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(pytesseract.image_to_string(img))  # detect chars

    data = pytesseract.image_to_data(img)

    for cnt, word in enumerate(data.splitlines()):
        if not cnt == 0:
            word = word.split()
            # print(word)  # char, x, y, w, h
            if len(word) == 12:
                x, y, w, h = int(word[6]), int(word[7]), int(word[8]), int(word[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(img, word[11], (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("Image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

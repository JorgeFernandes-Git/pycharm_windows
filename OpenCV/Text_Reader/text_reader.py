import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img = cv2.imread('Capture.PNG')

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img))  # detect chars
# print(pytesseract.image_to_boxes(img))  # detect rect on chars

h_img, w_img, _ = img.shape

boxes = pytesseract.image_to_boxes(img)

for box in boxes.splitlines():
    box = box.split(' ')
    # print(box)  # char, x, y, w, h
    x, y, w, h = int(box[1]), int(box[2]), int(box[4]), int(box[5])
    cv2.rectangle(img, (x, h_img-y), (w, h_img-h), (0, 255, 0), 1)

cv2.imshow("result", img)
cv2.waitKey(0)

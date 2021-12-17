import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img = cv2.imread('Capture.PNG')

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img))  # detect chars
# print(pytesseract.image_to_boxes(img))  # detect rect on chars

h_img, w_img, _ = img.shape
#
# boxes = pytesseract.image_to_boxes(img)
#
# for box in boxes.splitlines():
#     box = box.split(' ')
#     # print(box)  # char, x, y, w, h
#     x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
#     cv2.rectangle(img, (x, h_img - y), (w, h_img - h), (0, 255, 0), 3)
#     cv2.putText(img, box[0], (x, h_img - y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)


data = pytesseract.image_to_data(img)

for cnt, word in enumerate(data.splitlines()):
    if not cnt == 0:
        word = word.split()
        print(word)  # char, x, y, w, h
        if len(word) == 12:
            x, y, w, h = int(word[6]), int(word[7]), int(word[8]), int(word[9])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(img, word[11], (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)


cv2.imshow("result", img)
cv2.waitKey(0)

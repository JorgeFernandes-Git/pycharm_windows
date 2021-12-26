import cv2
import pickle


def mouse_click(events, x, y, flags, param):
    if events == cv2.EVENT_LBUTTONDOWN:  # create space
        pos_list.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:  # delete space
        for i, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                pos_list.pop(i)


width, height = 107, 48  # 157-50, 240-192
pos_list = []

while True:
    img = cv2.imread("carParkImg.png")

    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 1)

    # cv2.rectangle(img, (50, 192), (157, 240), (255, 0, 255), 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouse_click)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

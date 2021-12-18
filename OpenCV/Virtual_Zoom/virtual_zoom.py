import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# init
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
detector = HandDetector(detectionCon=0.8)

# variables
start_dist = None
scale = 0
cx, cy = 200, 200

# process
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    hands = detector.findHands(img, draw=False)
    zoom_img = cv2.imread('linux.png', cv2.IMREAD_UNCHANGED)
    zoom_img = cv2.resize(zoom_img, (273, 286))

    if len(hands) == 2:
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
            lm_list_1 = hands[0]["lmList"]
            lm_list_2 = hands[1]["lmList"]

            if start_dist is None:
                length, info = detector.findDistance(hands[0]["center"], hands[1]["center"])
                # length, info, img = detector.findDistance(lm_list_1[8], lm_list_2[8], img)
                start_dist = length

            # length, info, img = detector.findDistance(lm_list_1[8], lm_list_2[8], img)
            length, info = detector.findDistance(hands[0]["center"], hands[1]["center"])

            scale = int((length - start_dist) // 2)
            cx, cy = info[4], info[5]  # get center point of the length

    else:
        start_dist = None

    try:

        h1, w1, _ = zoom_img.shape
        new_h1, new_w1 = ((h1 + scale)//2)*2, ((w1 + scale)//2)*2  # this will prevent the lost of a pixel

        # prevent image too small
        if new_h1 > 0 and new_w1 > 0:
            zoom_img = cv2.resize(zoom_img, (new_w1, new_h1))
        else:
            new_h1, new_w1 = 1, 1

        img = cvzone.overlayPNG(img, zoom_img, [cx - new_w1 // 2, cy - new_h1 // 2])
        # img[cy - new_h1 // 2:cy + new_h1 // 2, cx - new_w1 // 2:cx + new_w1 // 2] = zoom_img

    except ValueError:  # prevent image out of screen
        pass

    cv2.imshow("image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

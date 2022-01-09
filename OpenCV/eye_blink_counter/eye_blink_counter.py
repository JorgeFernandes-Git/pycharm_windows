import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# https://www.youtube.com/watch?v=-TVUwH1PgBs

cap = cv2.VideoCapture("Video.mp4")
# cap = cv2.VideoCapture(0)

detector = FaceMeshDetector(maxFaces=1)
plot_y = LivePlot(640, 360, [20, 50], invert=True)

ids_list = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratio_list = []
blink_cnt = 0
cnt = 0
color = (0, 0, 255)

while True:
    # loop the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    _, img = cap.read()
    img = cv2.resize(img, (640, 360))

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in ids_list:
            cv2.circle(img, face[id], 3, color, cv2.FILLED)

        left_up = face[159]
        left_down = face[23]
        left_left = face[130]
        left_right = face[243]
        length_ver, _ = detector.findDistance(left_up, left_down)
        length_hor, _ = detector.findDistance(left_left, left_right)

        cv2.line(img, left_up, left_down, color, 1)
        cv2.line(img, left_left, left_right, color, 1)

        # print(int((length_ver / length_hor) * 100))
        ratio = (length_ver / length_hor) * 100
        ratio_list.append(ratio)

        if len(ratio_list) > 3:  # increase to smooth the plot
            ratio_list.pop(0)

        ratio_avg = sum(ratio_list) / len(ratio_list)

        if ratio_avg < 35 and cnt == 0:
            blink_cnt += 1
            cnt = 1
            color = (0, 200, 0)

        # ignore multiple blink in once
        if cnt != 0:
            cnt += 1
            if cnt > 10:
                cnt = 0
                color = (0, 0, 255)

        cvzone.putTextRect(img, f'Blink Count: {blink_cnt}', (20, 30),
                           scale=1, colorR=color, thickness=1)

        img_plot_y = plot_y.update(ratio_avg, color)

        img_stack = cvzone.stackImages([img, img_plot_y], 2, 1)
    else:
        img_stack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("image", img_stack)

    # ESC to close
    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

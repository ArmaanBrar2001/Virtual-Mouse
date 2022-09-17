import cv2
import mediapipe as mp
import pyautogui as pg

capture = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
scrn_wth, scrn_ht = pg.size()

pg.FAILSAFE = False

middle_x = 0
middle_y = 0
ring_x = 0
index_y = 0
index_x = 0

while True:
    _, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))

                    index_x = scrn_wth/frame_width * x
                    index_y = scrn_ht/frame_height * y

                    pg.moveTo(index_x, index_y)

                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))

                    middle_x = scrn_wth/frame_width * x
                    middle_y = scrn_ht/frame_height * y

                if id == 16:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 0))

                    ring_x = scrn_wth/frame_width * x
                    ring_y = scrn_ht/frame_height * y

                    print(ring_y - middle_y)
                    print(middle_y - ring_y, '\n\n')

                    if ring_y - middle_y > 110:
                        pg.scroll(50)

                    if middle_y - ring_y > 110:
                        pg.scroll(-50)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 255))

                    thumb_x = scrn_wth/frame_width * x
                    thumb_y = scrn_ht/frame_height * y

                    if abs(index_x - thumb_x) < 30:
                        pg.click()

                    if abs(middle_x - thumb_x) < 30:
                        pg.rightClick()

                    if abs(middle_x - thumb_x) < 30:
                        pg.doubleClick()

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)

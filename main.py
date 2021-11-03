"""
IMPORTS
"""
import cv2
from hand_mouse_control import HandEncodings
import ctypes
from window_control import Mouse_Control
import mediapipe as mp
import time
from datetime import datetime
import win32api, win32con

print("Sleeping 10 sec")
time.sleep(10)
print("Starting Program ...")
user32 = ctypes.windll.user32

click = False
clicked_time = datetime.now()
mp_hands = mp.solutions.hands

video_capture = cv2.VideoCapture("http://192.168.0.107:4747/video")

print("Loading Hand Model ...")
with mp_hands.Hands(
             static_image_mode = False,
             max_num_hands = 1,
             min_detection_confidence = 0.5,
             model_complexity = 0) as hands:
    print("Hand Model Load Complete ...")
    print("Starting Inference")

    while video_capture.isOpened():

        ret ,frame = video_capture.read()

        if not ret:
            continue

        flipped_frame = cv2.flip(frame, 1)
        """ Resizing the frame to the half of the size of the display """
        resized_frame = cv2.resize(flipped_frame ,(int(user32.GetSystemMetrics(0)/2),int(user32.GetSystemMetrics(1)/2)))

        """ Created Object of class HandEncodings """
        HEclass = HandEncodings(resized_frame,hands,mp_hands)

        """ Calling frame_to_encodings fuction from HandEncoding 
        class to get hand landmarks"""

        MainFinger,SecondaryFinger = HEclass.frame_to_encodings()

        if MainFinger is not None and SecondaryFinger is not None:
            cv2.circle(resized_frame,MainFinger, 5, (0,255,0), thickness=-1)
            cv2.circle(resized_frame, SecondaryFinger, 5, (0, 255, 0), thickness=-1)
            """Calculating Euclidean Distance using CalculateDistance Function from HandEncodings class"""
            distance = HEclass.CalculateDistace(MainFinger, SecondaryFinger)
            """ Creating Object of class Mouse_Control"""
            mc = Mouse_Control(MainFinger[0],MainFinger[1])
            """ Using move mouse fuction from Mouse_Control  which is used to move mouse to specified position on the screen """
            mc.mouse_move()

            if distance < 25:
                if click is False:
                    """ Using mouse_click to click on a specific area of the screen """
                    mc.mouse_click()
                    mc.mouse_click()
                    click = True
                    clicked_time = datetime.now()
                else:
                    diff = datetime.now() - clicked_time
                    if diff.total_seconds() > 5:
                        click = False
                print("Clicked")
                cv2.line(resized_frame, MainFinger, SecondaryFinger, (0, 0, 255), 5)
            else:
                cv2.line(resized_frame, MainFinger, SecondaryFinger, (0, 255, 0), 5)

            # print("Distance",distance)

        key = cv2.waitKey(60)

        cv2.imshow("Output Window",resized_frame)

        if key == ord('q'):
            break

    video_capture.release()

    cv2.destroyAllWindows()





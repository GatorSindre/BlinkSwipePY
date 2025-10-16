import cv2
import mediapipe as mp
import numpy as np
import pyautogui

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, eye_points, img_w, img_h):
    points = np.array([(int(landmarks[i].x * img_w), int(landmarks[i].y * img_h)) for i in eye_points])
    vertical1 = np.linalg.norm(points[1] - points[5])
    vertical2 = np.linalg.norm(points[2] - points[4])
    horizontal = np.linalg.norm(points[0] - points[3])
    EAR = (vertical1 + vertical2) / (2.0 * horizontal)
    return EAR

cap = cv2.VideoCapture(0)

BLINK_THRESH = 0.21
FIRST_CLOSED_FRAMES = 1
SECOND_CLOSED_FRAMES = 5
THIRD_CLOSED_FRAMES = 9
Frame_Counter = 9
NumberMode = False

while True:
    success, frame = cap.read()
    if not success: break

    img_h, img_w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        left_EAR = eye_aspect_ratio(landmarks, LEFT_EYE, img_w, img_h)
        right_EAR = eye_aspect_ratio(landmarks, RIGHT_EYE, img_w, img_h)
        avg_EAR = (left_EAR + right_EAR) / 2.0
        

        if NumberMode == True: 
            if avg_EAR < BLINK_THRESH:
                Frame_Counter += 1
            elif Frame_Counter >= THIRD_CLOSED_FRAMES:
                    pyautogui.press("3")
                    print("Blink Third - Numbers mode")
                    Frame_Counter = 0
                    NumberMode = False
            elif Frame_Counter >= SECOND_CLOSED_FRAMES:
                    pyautogui.press("2")
                    print("Blink Second - Numbers mode")
                    Frame_Counter = 0    
                    NumberMode = False
            elif Frame_Counter >= FIRST_CLOSED_FRAMES:
                    pyautogui.press("1")
                    print("Blink First - Numbers mode")
                    Frame_Counter = 0
                    NumberMode = False
        else:
            if avg_EAR < BLINK_THRESH:
                Frame_Counter += 1
            elif Frame_Counter >= THIRD_CLOSED_FRAMES:
                    NumberMode = True
                    print("Blink Third")
                    Frame_Counter = 0
            elif Frame_Counter >= SECOND_CLOSED_FRAMES:
                    pyautogui.press("up")
                    print("Blink Second")
                    Frame_Counter = 0    
            elif Frame_Counter >= FIRST_CLOSED_FRAMES:
                    pyautogui.press("down")
                    print("Blink First")
                    Frame_Counter = 0     

            
    cv2.imshow("Blink Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
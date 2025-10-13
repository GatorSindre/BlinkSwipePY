import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import subprocess

cameraNum = input("CameraNum: ")
cameraNum = int(cameraNum)
scrollType = input("Scroll on laptop[0] or phone[1] or both[2]\n  ")
scrollType = int(scrollType)

if not scrollType >= 0 and scrollType <= 2:
    print("error: invalid scrollType")
    exit()

if cameraNum < 0 or cameraNum > 100:
    exit()

def adb_command(cmd):
    full_cmd = f"adb shell {cmd}"
    subprocess.run(full_cmd, shell=True)

def swipe(x1, y1, x2, y2, duration=500):
    adb_command(f"input swipe {x1} {y1} {x2} {y2} {duration}")

def DoAswipe(scrollType):
    if scrollType == 0:
        pyautogui.press("down")
    elif scrollType == 1:
        swipe(500, 1800, 500, 500, 100)
    elif scrollType == 2:
        pyautogui.press("down")
        swipe(500, 1800, 500, 500, 100)
    else:
        print("Invalid scrollType\nexiting...")
        exit()

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

cap = cv2.VideoCapture(cameraNum)

BLINK_THRESH = 0.21
CLOSED_FRAMES = 3
frame_counter = 0

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
        
        if avg_EAR < BLINK_THRESH:
            frame_counter += 1
        else:
            if frame_counter >= CLOSED_FRAMES:
                DoAswipe(scrollType)
            frame_counter = 0

    cv2.imshow("Blink Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
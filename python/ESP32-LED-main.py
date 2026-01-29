import serial
import time
import cv2
import mediapipe as mp


# Serial port and Camera setup
ser = serial.Serial(port="COM3", baudrate=115200)
cam_width, cam_height = (
    1280,
    720,
)  # Reduce resolution from 1280x720 to 640x360 for better FPS
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

# MediaPipe Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)
mpDraw = mp.solutions.drawing_utils

# Finger tracking
finger_count = ["0", "0", "0", "0", "0"]

try:
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        # Check if hands are in frame
        if results.multi_hand_landmarks:
            handLms = results.multi_hand_landmarks[0]
            hand_label = results.multi_handedness[0].classification[0].label

            # Update finger status for thumb
            if hand_label == "Right":
                finger_count[0] = (
                    "1" if handLms.landmark[4].x < handLms.landmark[3].x else "0"
                )
            elif hand_label == "Left":
                finger_count[0] = (
                    "1" if handLms.landmark[4].x > handLms.landmark[3].x else "0"
                )

            # Update finger status for other fingers
            finger_count[1] = (
                "1"
                if handLms.landmark[6].y > handLms.landmark[8].y < handLms.landmark[7].y
                else "0"
            )
            finger_count[2] = (
                "1"
                if handLms.landmark[10].y
                > handLms.landmark[12].y
                < handLms.landmark[11].y
                else "0"
            )
            finger_count[3] = (
                "1"
                if handLms.landmark[14].y
                > handLms.landmark[16].y
                < handLms.landmark[15].y
                else "0"
            )
            finger_count[4] = (
                "1"
                if handLms.landmark[18].y
                > handLms.landmark[20].y
                < handLms.landmark[19].y
                else "0"
            )

            # Draw landmarks on the hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        else:
            finger_count = ["0", "0", "0", "0", "0"]

        # Send finger-state to ESP32
        if ser.is_open:
            message = "".join(finger_count)
            ser.write((message + "\n").encode())
            print(message)

        # Display window
        cv2.imshow("Img", img)

        time.sleep(0.001)
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    if ser.is_open:
        ser.close()

import cv2
import numpy as np
import os
import sys
import time
import pyautogui

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)

def start_gesture_listener():
    print("[ASTRA-GESTURE] Initializing Robust Volume HUD...")
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    last_action_time = 0
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Flip frame horizontally for mirror view
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        # Define Region of Interest (ROI) coordinates for the box: right side
        roi_x1, roi_y1, roi_x2, roi_y2 = w - 280, 50, w - 40, 290
        
        # Draw the ROI box on the frame
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 243, 255), 2)
        cv2.putText(frame, "TOP=VOL+ | BOT=VOL-", (roi_x1, roi_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 243, 255), 2)

        # Extract only the ROI region for hand tracking
        roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]

        # Convert ROI to HSV color space for skin detection
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv_roi, lower_skin, upper_skin)

        # Clean noise
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # Find contours inside the ROI box only
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)
            if area > 1000: # Hand detected in box
                x, y, cw, ch = cv2.boundingRect(max_contour)
                cv2.rectangle(frame, (roi_x1 + x, roi_y1 + y), (roi_x1 + x + cw, roi_y1 + y + ch), (0, 255, 0), 2)

                # Map vertical position to volume control with a strict cooldown timer
                box_height = float(roi_y2 - roi_y1)
                norm_y = float(y) / box_height # 0.0 at top, 1.0 at bottom
                
                current_time = time.time()
                # Cooldown of 0.25 seconds ensures it steps the volume smoothly instead of locking up
                if current_time - last_action_time > 0.25:
                    if norm_y < 0.35: # Hand near top -> Physical Volume Up
                        pyautogui.press('volumeup')
                        cv2.putText(frame, "VOLUME UP (+)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        last_action_time = current_time
                    elif norm_y > 0.65: # Hand near bottom -> Physical Volume Down
                        pyautogui.press('volumedown')
                        cv2.putText(frame, "VOLUME DOWN (-)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        last_action_time = current_time

        # Show HUD preview window
        cv2.imshow("ASTRA Gesture HUD (Press 'Q' to Exit)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
import mediapipe as mp
import cv2
import numpy as np

mp_pose = mp.solutions.pose

def detect_yoga_pose(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(img_rgb)
        if not results.pose_landmarks:
            return "No person detected."

        landmarks = results.pose_landmarks.landmark
        return landmarks  # backend will use this for feedback

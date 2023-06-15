import numpy as np
from enum import Enum

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class State(Enum):
    UP = 0
    DOWN = 1


class Counter:
    def __init__(self):
        self._counters = {
            "curl": 0
        }
        self._states = {
            "curl": State.DOWN
        }

    def count(self, exercise, raw_keypoints):
        #Get x, y coordinates for key points
        shoulder = [raw_keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [raw_keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [raw_keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        angle = self._calculate_angle(shoulder, elbow, wrist)
        print(f"angle: {angle}")

        if exercise == "curl":
            if angle > 140:
                self._states["curl"] = State.DOWN
            if angle < 70 and self._states["curl"] == State.DOWN:
                self._states["curl"] = State.UP
                self._counters["curl"] += 1

        print(f"counters: {self._counters}")
        print(f"states: {self._states}")
    
    def visualise(self, cap, image):
        pass

    def _calculate_angle(self, a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360-angle

        return angle
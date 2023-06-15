import numpy as np
import pprint
from enum import Enum
from constants import EXERCISES

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class State(Enum):
    START = 0
    END = 1

class Counter:
    def __init__(self):
        self._counters = {}
        self._states = {}

        for exercise in EXERCISES:
            self._counters[exercise] = 0
            self._states[exercise] = State.START

    def count(self, exercise, raw_keypoints):
        #Get x, y coordinates for key points
        shoulder = [raw_keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [raw_keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [raw_keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        hip = [raw_keypoints[mp_pose.PoseLandmark.LEFT_HIP.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee  = [raw_keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [raw_keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,raw_keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        #21
        if exercise == "curl":
            angle = self._calculate_angle(shoulder, elbow, wrist)
            print(f"angle: {angle}")
            if angle > 140:
                self._states["curl"] = State.START
            if angle < 70 and self._states["curl"] == State.START:
                self._states["curl"] = State.END
                self._counters["curl"] += 1
        #99
        elif exercise == "armraise":
            angle = self._calculate_angle(elbow, shoulder, hip)
            print(f"angle: {angle}")
            if angle > 110:
                    self._states["armraise"] = State.END
            if angle < 70 and self._states["armraise"] == State.END:
                self._states["armraise"] = State.START
                self._counters["armraise"] += 1
        #30
        elif exercise == "legraise":
            angle = self._calculate_angle(shoulder, hip, knee)
            print(f"angle: {angle}")
            if angle > 130:
                    self._states["legraise"] = State.START
            if angle < 110 and self._states["legraise"] == State.START:
                self._states["legraise"] = State.END
                self._counters["legraise"] += 1
        #19
        elif exercise == "squat":
            angle = self._calculate_angle(hip, knee, ankle)
            print(f"angle: {angle}")
            if angle > 170:
                    self._states["squat"] = State.END
            if angle < 160 and self._states["squat"] == State.END:
                self._states["squat"] = State.START
                self._counters["squat"] += 1

        pp = pprint.PrettyPrinter(depth=6)
        print("counters:", end="")
        pp.pprint(self._counters)
        print("states:", end="")
        pp.pprint(self._states)
    
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
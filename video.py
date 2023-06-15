import sys
import tensorflow as tf
import collections
model = tf.keras.models.load_model("models/model4.tf")


import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

from counter import Counter

def dominant(A):
    x = None
    count = 0
    for i in A:
        if count == 0:
            x = i
            count += 1
        elif i == x:
            count += 1
        else:
            count -= 1
    return x

text_color = (124,252,0)

exercise = str(sys.argv[1])
id = int(sys.argv[2])
clip_no = str(id).zfill(6)

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(f"./data/infinityai_fitness_basic_{exercise}_v1.0/data/{clip_no}.mp4") 

counter = Counter()

PREDICTIONS_BUFFER_SIZE = 100 # TODO: Zmniejszyć bufor na 5 i pokazać, że na squat 19 model4 działa lepiej niż model3
predictions = collections.deque(maxlen=PREDICTIONS_BUFFER_SIZE)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        try:
            frame_keypoints = []

            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Make detection
            results = pose.process(image)
            raw_keypoints = results.pose_landmarks.landmark

            for landmark in mp_pose.PoseLandmark:
                frame_keypoints.append([
                    raw_keypoints[landmark.value].x,
                    raw_keypoints[landmark.value].y,
                    #raw_keypoints[landmark.value].z,
                ])

            prediction = model.predict([frame_keypoints])

            number_to_class = {
                0: "armraise",
                1: "bicyclecrunch",
                2: "birddog",
                3: "curl",
                4: "fly",
                5: "legraise",
                6: "overheadpress",
                7: "pushup",
                8: "squat",
                9: "superman"
            }

            predicted_class = number_to_class[np.argmax(prediction)]

            predictions.append(predicted_class)

            print(f"predictions: {predictions}")

            predicted_class = dominant(predictions)

            counter.count(predicted_class, raw_keypoints)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.putText(image, str(predicted_class), (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
            image = cv2.putText(image, str(prediction), (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            
            cv2.imshow("TWM", image)
        except Exception as e:
            print(f"Error processing frame: {e}")

        if cv2.waitKey(10) & 0xFF == ord('q'):
                break

cv2.destroyAllWindows()

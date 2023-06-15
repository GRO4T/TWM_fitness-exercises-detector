
import tensorflow as tf
model = tf.keras.models.load_model("models/model3.tf")


import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

from counter import Counter

text_color = (124,252,0)

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("./data/infinityai_fitness_basic_curl_v1.0/data/000093.mp4") 

counter = Counter()

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
                    raw_keypoints[landmark.value].z,
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

            counter.count(predicted_class, raw_keypoints)

            debug_info = f"{predicted_class}: {prediction}"

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.putText(image, debug_info, (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
            
            cv2.imshow("TWM", image)
        except Exception as e:
            print(f"Error processing frame: {e}")

        if cv2.waitKey(10) & 0xFF == ord('q'):
                break

cv2.destroyAllWindows()

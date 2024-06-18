import os
import pickle

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []
counter = 0  # Counter to track the number of iterations

# Ensure only directories are processed
for dir_ in os.listdir(DATA_DIR):
    dir_path = os.path.join(DATA_DIR, dir_)
    if os.path.isdir(dir_path):
        for img_path in os.listdir(dir_path):
            if counter >= 100:
                break  # Break the loop if the counter reaches 100
            
            data_aux = []
            x_ = []
            y_ = []

            img_path = os.path.join(dir_path, img_path)
            imgGray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            sift = cv2.SIFT_create()
            keypoints = sift.detect(imgGray, None)
            imgKeypoints = cv2.drawKeypoints(imgGray, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            results = hands.process(imgKeypoints)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                data.append(data_aux)
                labels.append(dir_)
                counter += 1  # Increment the counter after processing each image

# Save the data
with open(os.path.join(DATA_DIR, 'data.pickle'), 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

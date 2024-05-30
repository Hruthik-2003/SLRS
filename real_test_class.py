import cv2
import mediapipe as mp
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk

# --- dependency for building and training LSTM neural network
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

DATA_PATH = os.path.join(r"C:\Users\hruth\project_pys\SignLanguage\MP_Data")
actions = np.array(['hello', 'thanks', 'iloveyou'])

# Thirty videos worth of data
no_sequences = 40

# Videos are going to be 40 frames in length
sequence_length = 40

# hello:0 thanks:1 ilu:2
label_map = {label: num for num, label in enumerate(actions)}
sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

# for action in actions:
#     for sequence in range(no_sequences):
#         try:
#             os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
#         except:
#             pass

X = np.array(sequences)
y = to_categorical(labels).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

# print(x.shape)
# print(y)
# print(X_train.shape)
# print(y_test.shape)

#  ---------Building and train LSTM Neural network
# tensor board is a web apps that works on neural network and monitor neural network training
# log_dir = os.path.join('Logs')
# tb_callback = TensorBoard(log_dir=log_dir)
#
# model = Sequential()
# # 64model units + activation on relu + input shape will be 30 frames *  1662 units
# model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 1662)))
# model.add(LSTM(128, return_sequences=True, activation='relu'))
# model.add(LSTM(64, return_sequences=False, activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(32, activation='relu'))
# # model with 3 args
# model.add(Dense(actions.shape[0], activation='softmax'))
# res = model.predict(X_test)
# print(actions[np.argmax(res[3])])
# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
#
# model.fit(X_train, y_train, epochs=2000, callbacks=[tb_callback])
# print(model.summary())
# res = model.predict(X_test)


model = tf.keras.models.load_model(r'C:\Users\hruth\project_pys\SignLanguage\my_model.keras')

# del model
# model = tf.keras.models.load_model('action.h5')
# model.load_weights('action.h5')
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score

yhat = model.predict(X_test)
ytrue = np.argmax(y_test, axis=1).tolist()
yhat = np.argmax(yhat, axis=1).tolist()
multilabel_confusion_matrix(ytrue, yhat)

accuracy_score(ytrue, yhat)

mp_holistic = mp.solutions.holistic  # holistic model
mp_drawing = mp.solutions.drawing_utils  # drawing utilities


def on_closing():
    cv2.close()
    cv2.destroyAllWindows()


def mediapipe_detection(images, model):
    images = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)  # color conversion from bgr to rgb
    images.flags.writeable = False  # image is no longer writable here
    result = model.process(images)  # make prediction
    images.flags.writeable = True  # image now writable
    images = cv2.cvtColor(images, cv2.COLOR_RGB2BGR)  # color conversion from rgb to bgr
    return images, result


def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                              mp_drawing.DrawingSpec(color=(108, 9, 60), thickness=1,
                                                     circle_radius=1),
                              mp_drawing.DrawingSpec(color=(199, 125, 255), thickness=1,
                                                     circle_radius=1)
                              )  # draw face connection
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=2,
                                                     circle_radius=1),
                              mp_drawing.DrawingSpec(color=(191, 44, 123), thickness=2,
                                                     circle_radius=1))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(0, 0, 225), thickness=2,
                                                     circle_radius=1),
                              mp_drawing.DrawingSpec(color=(200, 225, 164), thickness=2,
                                                     circle_radius=1))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(26, 22, 164), thickness=2,
                                                     circle_radius=1),
                              mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2,
                                                     circle_radius=1))


def extract_keypoints(results):
    # pose is flattened value of x,y,z pose_landmarks
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in
                     results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(132)
    # face is flattened value of x,y,z face_landmarks
    face = np.array([[res.x, res.y, res.z] for res in
                     results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(1404)
    # lh is flattened value of x,y,z left_hand_landmarks
    lh = np.array([[res.x, res.y, res.z] for res in
                   results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    # rh is flattened value of x,y,z right_hand_landmark
    rh = np.array([[res.x, res.y, res.z] for res in
                   results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(
        21 * 3)
    # this function return concatenate of pose ,face, right,left landmarks array
    # it is the length of (33*4)+(468 * 3)+(21 * 3)+(21*3) = 1662
    # return np.concatenate([pose, face, lh, rh])
    return np.concatenate([pose, face, lh, rh])


from scipy import stats

colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

# def prob_viz(res, actions, input_frame, colors):
#     output_frame = input_frame.copy()
#     for num, prob in enumerate(res):
#         cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
#         cv2.putText(output_frame, actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
#                     cv2.LINE_AA)
#
#     return output_frame


# 1. New detection variables
# 1. New detection variables
s_sequence01 = []
sentence = []
predictions = []
threshold = 0.3


# win = Tk()
class RealTimeTest(ctk.CTkToplevel):
    # Set the size of the window
    def __init__(self):
        super().__init__()
        self.focus_set()
        self.grab_set()
        # self.geometry("1300x550")  # Create a Label to capture the Video frames
        self.state('zoomed')
        frame = ctk.CTkFrame(self, height=600, width=800)
        frame.place(x=50, y=50)
        label = ctk.CTkLabel(frame, text=" ")
        label.pack()
        description_title = ctk.CTkLabel(self, text="DESCRIPTION", text_color="#375862",
                                         font=("Copperplate Gothic Bold", 25, "bold"))
        description_title.place(x=650, y=40)
        description_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#FFF", height=550, width=520)
        description_frame.place(x=650, y=70)

        description = ctk.CTkTextbox(description_frame, height=550, width=520,font=("Times New Roman", 18, "bold"))
        description.place(x=0, y=0)
        cap = cv2.VideoCapture(0)
        # Set mediapipe model
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():

                # Read feed
                ret, frame = cap.read()

                # Make detections
                imageCV, results = mediapipe_detection(frame, holistic)
                print(results)

                # Draw landmarks
                draw_styled_landmarks(imageCV, results)

                # 2. Prediction logic
                # global sentence
                # global predictions
                # key_points = extract_keypoints(results)
                global s_sequence01
                # s_sequence01.append(key_points)
                # s_sequence01 = s_sequence01[-40:]
                keypoints = extract_keypoints(results)
                s_sequence01.append(keypoints)
                s_sequence01 = s_sequence01[-40:]

                if len(s_sequence01) == 40:
                    res = model.predict(np.expand_dims(s_sequence01, axis=0))[0]
                    print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))

                    # 3. Viz logic
                    if np.unique(predictions[-10:])[0] == np.argmax(res):
                        if res[np.argmax(res)] > threshold:

                            if len(sentence) > 0:
                                if actions[np.argmax(res)] != sentence[-1]:
                                    sentence.append(actions[np.argmax(res)])
                            else:
                                sentence.append(actions[np.argmax(res)])

                    # if len(sentence) > 4:
                    #     sentence = sentence[-5:]

                    # Viz probabilities
                    # image = prob_viz(res, actions, image, colors)

                # cv2.rectangle(imageCV, (0, 0), (640, 40), (245, 117, 16), -1)
                # cv2.putText(imageCV, ' '.join(sentence), (3, 30),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                description.delete(1.0, ctk.END)
                description.insert(ctk.END, sentence)
                # Show to screen
                # cv2.imshow('OpenCV Feed', image)
                image1 = cv2.cvtColor(imageCV, cv2.COLOR_BGR2RGB)
                image1 = cv2.resize(image1, (800, 600))
                image1 = Image.fromarray(image1)
                imgtk = ImageTk.PhotoImage(image=image1)
                label.configure(image=imgtk)

                # Break gracefully
                # if cv2.waitKey(10) & 0xFF == ord('q'):
                #     # self.destroy()

                self.update()
                image1.close()
                if self.protocol == "WM_DELETE_WINDOW":
                    cap.release()
                    self.destroy()
                    self.quit()
                    cv2.close()
                    break
            cap.release()
            self.destroy()
            image1.close()
            self.protocol("WM_DELETE_WINDOW", cv2.close)
            cv2.destroyAllWindows()

        cap.release()
        self.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    RealTimeTest().mainloop()

# sequence = []
# sentence = []
# threshold = 0.3
# predictions = []
# cap = cv2.VideoCapture(0)
# # Set mediapipe model
# with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#     while cap.isOpened():
#
#         # Read feed
#         ret, frame = cap.read()
#
#         # Make detections
#         image, results = mediapipe_detection(frame, holistic)
#         print(results)
#
#         # Draw landmarks
#         draw_styled_landmarks(image, results)
#
#         # 2. Prediction logic
#         keypoints = extract_keypoints(results)
#         sequence.append(keypoints)
#         sequence = sequence[-40:]
#
#         if len(sequence) == 40:
#             res = model.predict(np.expand_dims(sequence, axis=0))[0]
#             print(actions[np.argmax(res)])
#             predictions.append(np.argmax(res))
#
#             # 3. Viz logic
#             if np.unique(predictions[-10:])[0] == np.argmax(res):
#                 if res[np.argmax(res)] > threshold:
#
#                     if len(sentence) > 0:
#                         if actions[np.argmax(res)] != sentence[-1]:
#                             sentence.append(actions[np.argmax(res)])
#                     else:
#                         sentence.append(actions[np.argmax(res)])
#
#             if len(sentence) > 4:
#                 sentence = sentence[-5:]
#
#             # Viz probabilities
#             # image = prob_viz(res, actions, image, colors)
#
#         cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
#         cv2.putText(image, ' '.join(sentence), (3, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#
#         # Show to screen
#         cv2.imshow('OpenCV Feed', image)
#
#         # Break gracefully
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()

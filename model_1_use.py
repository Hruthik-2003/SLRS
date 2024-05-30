from tkinter.messagebox import showerror
import cv2
# cvzone package has HandTrackingModule then we import HandDetector class
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector

# import time


# capture object
sentence = []


class RunModelClass1(ctk.CTkToplevel):

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
                                         font=("Copperplate Gothic Bold", 30, "bold"))
        description_title.place(x=650, y=40)
        description_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#FFF", height=550, width=520)
        description_frame.place(x=650, y=70)

        description = ctk.CTkTextbox(description_frame, text_color="#555", height=550, width=520,
                                     font=("Times New Roman", 18, "bold"))
        description.place(x=0, y=0)
        cap = cv2.VideoCapture(0)

        detector = HandDetector(maxHands=2)
        classifier = Classifier("model/keras_model.h5", "model/labels.txt")
        # declaring gaps between border of container of bbox
        offset = 20
        imgSize = 300
        counter = 0

        # labels = ["A", "B", "C"]
        labels = []
        try:
            mydb = mysql.connector.connect(host="localhost", username="root", password="", database="slrs")
            my_cursor = mydb.cursor()
            query = "SELECT labels FROM model1_labels"
            my_cursor.execute(query)

            for row in my_cursor.fetchall():
                labels.append(row[0])

        except mysql.connector.Error as e:
            showerror("Server not response", "Error: Something went wrong")

        print(labels)

        # declaring the path of data folder
        dataFolder = "data/D"

        # img capture
        while cap.isOpened():
            success, img = cap.read()
            img = cv2.flip(img, 1)
            imgOutput = img.copy()
            # removing pointers on hand
            hands, img = detector.findHands(img, flipType=False)
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            # cropping image
            if hands:
                hand = hands[0]
                # bbox is the bounding box of hand(box contain hands only)
                x, y, w, h = hand['bbox']

                # setting up background image is white
                # unit8-> unsigned integer 8 bit
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

                # cropping an hand image
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                # embedding cropped image into white background image (matrix [0]->height [1]->width)
                imgCropShape = imgCrop.shape
                # imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop

                # aspectRatio=height/width
                aspectRatio = h / w
                # placing the cropped image at white background with fixed height
                if aspectRatio > 1:
                    # constant define to reference of particular height ratio
                    constant = imgSize / h
                    # returns the greater decimal value
                    widthCalculated = math.ceil(constant * w)
                    # we must resize the cropped image width=(imgSize/h)*width , height=imgSize 300
                    imgResize = cv2.resize(imgCrop, (widthCalculated, imgSize))

                    imgResizeShape = imgResize.shape

                    # making the image placed at center
                    widthGap = math.ceil((imgSize - widthCalculated) / 2)
                    imgWhite[0:imgResizeShape[0], widthGap:widthCalculated + widthGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(prediction, index, " - " + labels[index])

                # placing the cropped image at white background with fixed width
                else:
                    # constant define to reference of particular width ratio
                    constant = imgSize / w
                    # returns the greater decimal value
                    heightCalculated = math.ceil(constant * h)
                    # we must resize the cropped image width=(imgSize/h)*width , height=imgSize 300
                    imgResize = cv2.resize(imgCrop, (imgSize, heightCalculated))

                    imgResizeShape = imgResize.shape

                    # making the image placed at center
                    heightGap = math.ceil((imgSize - heightCalculated) / 2)
                    imgWhite[heightGap:heightCalculated + heightGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(prediction, index)

                cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 100, y - offset), (0, 0, 0),
                              cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 255, 0), 2)
                # shows cropped image
                # cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)
                if len(sentence) > 0:
                    if sentence[-1] != labels[index]:
                        sentence.append(labels[index])
                else:
                    sentence.append(labels[index])

            description.delete(1.0, ctk.END)
            description.insert(ctk.END, sentence)
            image1 = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
            image1 = cv2.resize(image1, (800, 600))
            image1 = Image.fromarray(image1)
            imgtk = ImageTk.PhotoImage(image=image1)
            label.configure(image=imgtk)
            self.update()
            image1.close()

            # shows entire image captured by webcam
            # cv2.imshow("Image", imgOutput)
            # wait 1ms wait key to capture
            cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
                break

        def on_closing():
            cap.release()
            cv2.destroyAllWindows()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    RunModelClass1().mainloop()

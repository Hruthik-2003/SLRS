import cv2
# cvzone package has HandTrackingModule then we import HandDetector class
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
import os

# capture object

# declaring the path of data folder


class ModelClass1(ctk.CTkToplevel):

    def __init__(self, class_name, dataFolder):
        super().__init__()
        self.focus_set()
        self.grab_set()
        # self.geometry("1300x550")  # Create a Label to capture the Video frames
        self.state('zoomed')
        frame = ctk.CTkFrame(self, height=600, width=800)
        frame.place(x=50, y=50)
        label = ctk.CTkLabel(frame, text=" ")
        label.pack()
        ctk.CTkLabel(self, text="Press and Hold 'S' to Collect Data", text_color="#8A3A75",
                     font=("Sitka Text Semibold", 30, "bold")).place(x=700, y=50)
        description_title = ctk.CTkLabel(self, text="DESCRIPTION", text_color="#375862",
                                         font=("Copperplate Gothic Bold", 30, "bold"))
        msg = ctk.CTkLabel(self, text=f"Image Collection is started for {class_name}", text_color="#8A2A25",
                           font=("Sitka Text Semibold", 20, "bold"))
        # description_title.place(x=650, y=40)
        # description_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#FFF", height=550, width=520)
        # description_frame.place(x=650, y=70)
        #
        # description = ctk.CTkTextbox(description_frame, height=550, width=520, font=("Times New Roman", 18, "bold"))
        # description.place(x=0, y=0)

        cap = cv2.VideoCapture(0)
        detector = HandDetector(maxHands=2)
        # detector=detector.tipIds
        # declaring gaps between border of container of bbox
        offset = 20
        imgSize = 300
        counter = 0
        # img capture
        while cap.isOpened():
            success, img = cap.read()
            img = cv2.flip(img, 1)
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
                # shows cropped image
                # cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)

                # shows entire image captured by webcam
            # cv2.imshow("Image", img)
            # wait 1ms wait key to capture
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image1 = cv2.resize(image1, (800, 600))
            image1 = Image.fromarray(image1)
            imgtk = ImageTk.PhotoImage(image=image1)
            label.configure(image=imgtk)
            self.update()
            image1.close()

            key = cv2.waitKey(1)
            if key == ord("s"):
                counter += 1
                cv2.imwrite(f'{dataFolder}/Image_{time.time()}.jpg', imgWhite)
                msg.place(x=700, y=100)
                print(counter)
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
    ModelClass1("null", "null").mainloop()

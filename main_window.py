# import PyPDF2
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, simpledialog
from tkinter import messagebox
from tkinter import scrolledtext
import admin_registration as ar
import user_registration as ur
import user_login as ul
import admin_login as al
import trainer_login as tl
# import mysql.connector
import warnings
import webbrowser

warnings.filterwarnings("ignore", message="loaded more than 1 DLL from .libs")

from PIL import ImageTk, Image


class MainPage(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def exit_window(self):
        self.destroy()

    def open_home(self, options: str):
        if options == "Home":
            self.destroy()
            new = MainPage()
            new.mainloop()
        else:
            pass

    def open_registration(self, options: str):
        if options == "User registration":
            # user_input = simpledialog.askstring("Input", "Enter primary Secretkey:", parent=self)
            # if user_input == "projectslrs@2023":
            #     if self.winfo_viewable():  # If root window is visible
            #         self.withdraw()  # Hide root window
            #         ar.AdminRegistration().deiconify()  # Show window2
            #     else:
            #         self.deiconify()  # Show root window
            #         ar.AdminRegistration().withdraw()  # Hide window2
            # else:
            #     messagebox.askretrycancel("secretkey is wrong",
            #                               "please check your secretkey or\n contact SLRS administration")
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                ur.UserRegistration().deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                ur.UserRegistration().withdraw()  # Hide window2
        else:
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                ur.UserRegistration().deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                ur.UserRegistration().withdraw()  # Hide window2

    def open_login(self, options: str):
        if options == "Admin Login":
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                al.AdminLogin("Admin").deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                al.AdminLogin("Admin").withdraw()  # Hide window2
        elif options == "Trainer Login":
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                tl.TrainerLogin("Trainer").deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                tl.TrainerLogin("Trainer").withdraw()  # Hide window2
        elif options == "User Login":
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                ul.UserLogin().deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                ul.UserLogin().withdraw()  # Hide window2

    def open_websites(self, btn_id):
        if btn_id == 1:
            webbrowser.open("https://amritmahotsav.nic.in/")
        if btn_id == 2:
            webbrowser.open("https://youtube.com/playlist?list=PL2rZQvyPycXJPaPuFSvtlyQxmb6GfNUP_")
        if btn_id == 3:
            webbrowser.open("https://wcd.karnataka.gov.in/page/Contact+us/Karnataka+State+Disabilities+Act+Office/kn")

    def open_about_us(self, option: str):
        if option == "about us":
            self.about_us = tk.Toplevel(self)
            self.about_us.title("About us")
            # self.state('zoomed')
            self.about_us.geometry("950x900+50+20")
            self.about_us.wm_iconbitmap("image_folder\\plant.ico")
            # # ---------content read
            file_path = "README\\aboutustxt.txt"
            with open(file_path, "r") as file:
                content = file.read()

            text_widget = tk.scrolledtext.ScrolledText(self.about_us, font=("Georgia", 16, "normal"),
                                                       padx=20, pady=20,
                                                       )
            text_widget.pack(expand=True, fill="both")
            text_widget.insert("1.0", content)
            text_widget.config(state="disabled")
            self.about_us.focus()
            self.about_us.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            self.quit()

    def __init__(self):
        super().__init__()

        # configure the root window
        self.about_us = None
        self.title("SIGN LANGUAGE RECOGNITION SYSTEM")
        # self.geometry("1090x650+10+10")
        self.state("zoomed")
        self.after(250, lambda: self.iconbitmap('image_folder\\plant.ico'))
        self.focus()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff")
        self.frame.pack(pady=10, padx=10, fill='both', expand=True)

        title_frame = ctk.CTkFrame(master=self.frame, fg_color="#802754", height=100, width=1000)
        title_frame.place(x=50, y=10)

        heading = ctk.CTkLabel(title_frame, text="SIGN  LANGUAGE  RECOGNITION  SYSTEM",
                               font=("Georgia", 25, "bold"), text_color="#ffffff")

        heading.place(x=170, y=50)

        slogan = ctk.CTkLabel(title_frame, text="Gesture Speak", padx=10,
                              font=("Brush Script MT", 20, "bold"),
                              text_color="#ffe5ec")
        slogan.place(x=410, y=5)

        self.logo = Image.open(r"image_folder\icon\main_logo.png")
        # "C:\Users\hruth\PycharmProjects\SignLanguageRecognition\SLR_model\project_SLRS\"
        self.logo_image = ctk.CTkImage(light_image=self.logo, size=(70, 70))
        self.logo_image_label = ctk.CTkLabel(master=title_frame, image=self.logo_image, text="")
        self.logo_image_label.place(x=30, y=20)
        self.logo_image_label.image = self.logo_image

        # menubar section========================
        menubar_frame = ctk.CTkFrame(master=self.frame, fg_color="#ecc5dd", height=70, width=1000)
        menubar_frame.place(x=50, y=120)

        home = ctk.CTkOptionMenu(menubar_frame, values=["Home"], fg_color="#802754",
                                 button_color="#994d74",
                                 command=self.open_home,
                                 button_hover_color="#b96d94")
        home.grid(row=0, column=0, pady=20, padx=30)
        home.set("Home")

        about_us = ctk.CTkOptionMenu(menubar_frame, values=["about us"], fg_color="#802754",
                                     button_color="#994d74",
                                     button_hover_color="#b96d94"
                                     )
        about_us.grid(row=0, column=1, pady=20, padx=30)
        about_us.set("About us")
        about_us.configure(command=self.open_about_us)

        register = ctk.CTkOptionMenu(menubar_frame, values=["User registration"],
                                     fg_color="#802754",
                                     button_color="#994d74",button_hover_color="#b96d94",
                                     command=self.open_registration)
        register.grid(row=0, column=2, pady=20, padx=30)
        register.set("Register")

        login = ctk.CTkOptionMenu(menubar_frame, values=["Admin Login", "Trainer Login", "User Login"],
                                  fg_color="#802754",
                                  button_color="#994d74", button_hover_color="#b96d94"
                                  ,command=self.open_login)
        login.grid(row=0, column=3, pady=20, padx=30)
        login.set("Login")
        # about_us = ctk.CTkOptionMenu(menubar_frame, values=["about us"], fg_color="#994d74",
        #                              button_color="#a663cc",
        #                              )
        exit_window = ctk.CTkButton(menubar_frame, text="Exit", fg_color="#802754",
                                    hover_color="#b96d94",
                                    corner_radius=20,
                                    command=self.on_closing)
        exit_window.grid(row=0, column=4, pady=20, padx=30)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # content section
        self.img = Image.open("image_folder/d_d/d8.jpg")
        self.side_image = ctk.CTkImage(light_image=self.img, size=(660, 150))
        self.side_image_label = ctk.CTkLabel(master=self.frame, image=self.side_image, text="")
        self.side_image_label.place(x=40, y=190)
        self.side_image_label.image = self.side_image

        self.img1 = Image.open("image_folder/d_d/d81.jpg")
        self.side_image1 = ctk.CTkImage(light_image=self.img1, size=(330, 150))
        self.side_image_label1 = ctk.CTkLabel(master=self.frame, image=self.side_image1, text="")
        self.side_image_label1.place(x=700, y=190)
        self.side_image_label1.image = self.side_image

        #         side content------------
        side_content_frame = ctk.CTkFrame(master=self.frame, fg_color="#ecc5dd", width=190, height=610)
        side_content_frame.place(x=1060, y=10)

        abt_us = ctk.CTkButton(master=side_content_frame, text="S.L.R.S", fg_color="#FFF", width=170, height=100,
                               border_width=2, border_color="#802754", hover_color="#fefae0",
                               image=self.logo_image, compound="top", font=("Sitka Text Semibold", 17, "bold"),
                               text_color="#802754",
                               command=lambda: self.open_about_us("about us"))
        abt_us.grid(row=1, column=0, pady=10, padx=10)

        self.akam_img = Image.open("image_folder/icon/akam.png")
        self.akam_image_ico = ctk.CTkImage(light_image=self.akam_img, size=(110, 70), )

        akam = ctk.CTkButton(master=side_content_frame, text=".", fg_color="#FFF", width=170, height=100,
                             border_width=2, border_color="#802754",
                             hover_color="#fefae0",
                             image=self.akam_image_ico, compound="top", font=("Sitka Text Semibold", 17, "bold"),
                             text_color="#802754",
                             command=lambda: self.open_websites(1)
                             )
        akam.grid(row=2, column=0, pady=10, padx=10)

        self.reg_img = Image.open("image_folder/icon/register.png")
        self.reg_image_ico = ctk.CTkImage(light_image=self.reg_img, size=(70, 70))
        reg = ctk.CTkButton(master=side_content_frame, text="Registration", fg_color="#FFF", width=170, height=100,
                            border_width=2, border_color="#802754",
                            hover_color="#fefae0",
                            image=self.reg_image_ico, compound="top", font=("Sitka Text Semibold", 17, "bold"),
                            text_color="#802754",
                            command=lambda: self.open_registration("User registration")
                            )
        reg.grid(row=3, column=0, pady=10, padx=10)

        self.sign_img = Image.open("image_folder/icon/sign.png")
        self.sign_image_ico = ctk.CTkImage(light_image=self.sign_img, size=(70, 70))
        sign = ctk.CTkButton(master=side_content_frame, text="Learn Sign Language", fg_color="#FFF", width=170,
                             height=100,
                             border_width=2, border_color="#802754",
                             hover_color="#fefae0",
                             image=self.sign_image_ico, compound="top", font=("Sitka Text Semibold", 17, "bold"),
                             text_color="#802754",
                             command=lambda: self.open_websites(2)
                             )
        sign.grid(row=4, column=0, pady=10, padx=10)
        # abt_us7 = ctk.CTkButton(master=side_content_frame, text="about us", fg_color="#FFF", width=170, height=100)
        # abt_us7.grid(row=7, column=0, pady=10, padx=10)
        self.web_img = Image.open("image_folder/icon/webcam.png")
        self.web_image_ico = ctk.CTkImage(light_image=self.web_img, size=(70, 70))
        abt_us4 = ctk.CTkButton(master=side_content_frame, text="Recognise", fg_color="#FFF", width=170, height=100,
                                border_width=2, border_color="#802754",
                                hover_color="#fefae0",
                                image=self.web_image_ico, compound="top", font=("Sitka Text Semibold", 17, "bold"),
                                text_color="#802754",
                                command=lambda :self.open_login("User Login")
                                )
        abt_us4.grid(row=5, column=0, pady=10, padx=10)

        #         content---------------
        ctk.CTkLabel(master=self.frame, text="Hello There....!", font=("Sitka Small Semibold", 35, "bold"),
                     text_color="#46394c").place(x=100, y=350)

        ctk.CTkLabel(master=self.frame,
                     text='Welcome to our Sign Language Recognition System,'
                          '\ndesigned to bridge the communication gap between hearing and non-hearing individuals.'
                          '\nWith this system, you can effortlessly communicate your thoughts, ideas, '
                          '\nand emotions through sign language,'
                          '\nas it accurately recognizes your signs and translates them into text or spoken words.',
                     justify="left", anchor="w",
                     font=("Sitka Small Semibold", 18, "bold"),
                     text_color="#959595").place(x=100, y=410)


if __name__ == '__main__':
    MainPage().mainloop()

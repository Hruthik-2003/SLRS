# import PyPDF2
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, simpledialog
from tkinter import messagebox
from tkinter import scrolledtext
import view_profile as vp
import main_window as mw
import user_login as ul
# import mysql.connector
import webbrowser
import real_test_class as rtc
from PIL import ImageTk, Image
import add_trainers as atr
import remove_trainer_user as rtu



class AdminWindow(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def exit_window(self):
        self.destroy()

    def open_home(self):
        self.destroy()
        new = mw.MainPage()
        new.mainloop()

    def open_realtime_use(self):

        rtc.RealTimeTest().deiconify()
        pass

    def open_about_us(self):
        self.about_us = tk.Toplevel(self)
        self.about_us.title("About us")
        # self.state('zoomed')
        # self.about_us.geometry("950x900+50+20")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
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

    def manage_user_operation(self, options: str):
        if options == "Add Trainer":
            atr.AddTrainer().deiconify()
        elif options == "Remove User/Trainer":
            rtu.RemoveUser().deiconify()
        else:
            pass

    def log_out(self):
        if messagebox.askokcancel("Log Out", "Do you want to log out ?"):
            if self.winfo_viewable() or rtc.RealTimeTest().winfo_viewable():  # If root window is visible
                # rtc.RealTimeTest().withdraw()
                self.withdraw()  # Hide root window
                ul.UserLogin().deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                ul.UserLogin().withdraw()  # Hide window2

        # if rtc.RealTimeTest().winfo_viewable():  # If root window is visible
        #     self.withdraw()  # Hide root window
        #     rtc.RealTimeTest().withdraw()
        #     ul.UserLogin().deiconify()  # Show window2
        # else:
        #     self.deiconify()  # Show root window
        #     ul.UserLogin().withdraw()

    image_paths = [
        r"image_folder\d_d\d4.jpg",
        r"image_folder\d_d\d5.jpg",
        r"image_folder\d_d\d6.jpg",
        r"image_folder\d_d\d7.jpg",
        r"image_folder\d_d\d1.jpg",
        r"image_folder\d_d\d2.jpg",
        r"image_folder\d_d\d3.jpg"]

    current_image_index = 0

    def show_image(self):
        self.canvas.delete("all")  # Clear the canvas before displaying a new image
        image_path = self.image_paths[self.current_image_index]
        image = Image.open(image_path)
        resized_image = image.resize((600, 450))
        photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=photo)
        self.canvas.image = photo  # Save a reference to prevent the image from being garbage collected

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.show_image()

    def prev_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.show_image()

    def open_websites(self, btn_id):
        if btn_id == 1:
            webbrowser.open("https://www.islrtc.nic.in/")
        if btn_id == 2:
            webbrowser.open("https://www.swavlambancard.gov.in/cms/about-persons-with-disability")
        if btn_id == 3:
            webbrowser.open("https://wcd.karnataka.gov.in/page/Contact+us/Karnataka+State+Disabilities+Act+Office/kn")

    def __init__(self, user_data):
        super().__init__()
        occupation = user_data[7]

        def view_profile():
            if self.winfo_viewable():
                vp.ViewProfile("user", user_data).deiconify()

        # configure the root window
        self.about_us = None
        self.title("ADMIN PAGE")
        self.geometry("1100x650+20+20")
        self.state('zoomed')
        print(user_data)
        self.after(250, lambda: self.iconbitmap('image_folder\\plant.ico'))
        # self.focus()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff")
        self.frame.pack(pady=10, padx=10, fill='both', expand=True)

        title_frame = ctk.CTkFrame(master=self.frame, fg_color="#246287", height=100, width=1160)
        title_frame.place(x=50, y=10)

        heading = ctk.CTkLabel(title_frame, text="SIGN  LANGUAGE  RECOGNITION  SYSTEM",
                               font=("Georgia", 25, "bold"), text_color="#FFF")

        heading.place(x=270, y=50)

        slogan = ctk.CTkLabel(title_frame, text="Gesture Speak", padx=10,
                              font=("Brush Script MT", 30, "bold"),
                              text_color="#ffe5ec")
        slogan.place(x=510, y=5)

        # menubar section========================
        menubar_frame = ctk.CTkFrame(master=self.frame, fg_color="#93E0DB", height=70, width=1000)
        menubar_frame.place(x=50, y=120)

        self.home_img = Image.open("image_folder/icon/house.png")
        self.home_image_ico = ctk.CTkImage(light_image=self.home_img, size=(20, 20))
        home = ctk.CTkButton(menubar_frame, text="Home", fg_color="#266785", corner_radius=10,
                             hover_color="#397C93",
                             height=30,
                             command=self.open_home,
                             image=self.home_image_ico)
        home.grid(row=0, column=0, pady=20, padx=26)

        self.cam_img = Image.open("image_folder/icon/userss.png")
        self.cam_image_ico = ctk.CTkImage(light_image=self.cam_img, size=(20, 20))

        self.mgr_img = Image.open("image_folder/icon/userss.png")
        self.mgr_image_ico = ctk.CTkImage(light_image=self.mgr_img, size=(20, 20))
        manage_user = ctk.CTkOptionMenu(menubar_frame, values=["Add Trainer", "Remove User/Trainer"],
                                        fg_color="#266785",
                                        button_color="#266785", button_hover_color="#397C93",
                                        command=self.manage_user_operation
                                        )

        manage_user.grid(row=0, column=1, pady=20, padx=26)
        manage_user.set("Manage User")

        self.profile_img = Image.open("image_folder/icon/profile.png")
        self.profile_image_ico = ctk.CTkImage(light_image=self.profile_img, size=(20, 20))

        profile = ctk.CTkButton(menubar_frame, text="View Profile", fg_color="#266785", corner_radius=10,
                                hover_color="#397C93",
                                height=30, image=self.profile_image_ico,
                                command=view_profile
                                )
        profile.grid(row=0, column=2, pady=20, padx=26)

        help_btn = ctk.CTkOptionMenu(menubar_frame, values=["register as Admin", "register as User"],
                                     fg_color="#266785",
                                     button_color="#8A3A75", button_hover_color="#397C93"
                                     )
        help_btn.grid(row=0, column=3, pady=20, padx=26)
        help_btn.set("Help")

        self.abt_us_img = Image.open("image_folder/icon/info.png")
        self.abt_us_image_ico = ctk.CTkImage(light_image=self.abt_us_img, size=(20, 20))
        about_us = ctk.CTkButton(menubar_frame, text="About us", fg_color="#266785", corner_radius=10,
                                 hover_color="#397C93",
                                 height=30,
                                 image=self.abt_us_image_ico)
        about_us.grid(row=0, column=4, pady=20, padx=26)
        about_us.configure(command=self.open_about_us)

        self.logout_img = Image.open("image_folder/icon/shutdown.png")
        self.logout_image_ico = ctk.CTkImage(light_image=self.logout_img, size=(20, 20))
        logout_window = ctk.CTkButton(menubar_frame, text="Logout", fg_color="#266785", corner_radius=10,
                                      hover_color="#397C93",
                                      command=self.log_out,
                                      height=30,
                                      image=self.logout_image_ico)
        logout_window.grid(row=0, column=5, pady=20, padx=26)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # content section
        self.img = Image.open("image_folder/d_d/d5.jpg")
        self.side_image = ctk.CTkImage(light_image=self.img, size=(350, 350))
        self.side_image_label = ctk.CTkLabel(master=self.frame, image=self.side_image, text="")
        self.side_image_label.place(x=10, y=210)
        self.side_image_label.image = self.side_image

        welcome_title = ctk.CTkLabel(master=self.frame,
                                     text="Wellcome  To  Real  Time  Sign  Language  Recognition  System..............!",
                                     fg_color="#fff", corner_radius=30, text_color="#8A3A75",
                                     font=("Brush Script MT", 25, "normal"))
        welcome_title.place(x=50, y=200)

        # image slider
        self.canvas = ctk.CTkCanvas(master=self.frame, width=600, height=450)
        self.canvas.place(x=50, y=370)

        self.back_img = Image.open("image_folder/icon/barrow.png")
        self.back_image_ico = ctk.CTkImage(light_image=self.back_img, size=(20, 20))
        self.prev_button = ctk.CTkButton(master=self.frame, text="", image=self.back_image_ico, command=self.prev_image,
                                         width=30, fg_color="#266785", hover_color="#ff6d9f")
        self.prev_button.place(x=30, y=565)

        self.next_img = Image.open("image_folder/icon/farrow.png")
        self.next_image_ico = ctk.CTkImage(light_image=self.next_img, size=(20, 20))

        self.next_button = ctk.CTkButton(master=self.frame, text="", image=self.next_image_ico, command=self.next_image,
                                         width=30, fg_color="#266785", hover_color="#ff6d9f")
        self.next_button.place(x=400, y=565)
        self.show_image()

        open_webcam1 = ctk.CTkButton(self.frame, text="Hands Talk", fg_color="#8A3A75", corner_radius=10,
                                     hover_color="#397C93",
                                     height=50, image=self.cam_image_ico,
                                     font=("Harrington", 18, "bold"),
                                     command=self.open_realtime_use
                                     )
        open_webcam1.place(x=170, y=570)

        # -------------------------------------------
        content_frame = ctk.CTkFrame(master=self.frame, fg_color="#a5f2ed", height=380, width=700,
                                     corner_radius=15)
        content_frame.place(x=490, y=240)

        self.islrtc_img = Image.open("image_folder/d_d/ISLRTC1.png")
        self.islrtc_image_ico = ctk.CTkImage(light_image=self.islrtc_img, size=(70, 70))
        self.govt_img = Image.open("image_folder/d_d/Karnataka-Govt-Logo-PNG.png")
        self.govt_image_ico = ctk.CTkImage(light_image=self.govt_img, size=(70, 70))
        self.aidds_img = Image.open("image_folder/d_d/aidds.png")
        self.aidds_image_ico = ctk.CTkImage(light_image=self.aidds_img, size=(70, 70))
        self.ind_img = Image.open("image_folder/d_d/inggov.png")
        self.ind_image_ico = ctk.CTkImage(light_image=self.ind_img, size=(50, 70))
        btn_1 = ctk.CTkButton(master=content_frame, fg_color="#FFF", text_color="#8A3A75", text="ISLRTC", height=100,
                              width=100,
                              image=self.islrtc_image_ico, hover_color="#eee", compound="top",
                              command=lambda: self.open_websites(1))
        btn_1.place(x=570, y=10)
        btn_2 = ctk.CTkButton(master=content_frame, fg_color="#FFF", height=100, width=100, text="UDID & DEP",
                              image=self.ind_image_ico, hover_color="#eee", compound="top", text_color="#8A3A75",
                              command=lambda: self.open_websites(2))
        btn_2.place(x=570, y=130)
        btn_3 = ctk.CTkButton(master=content_frame, fg_color="#FFF", height=100, width=100, text="ADDIS",
                              image=self.govt_image_ico, hover_color="#eee", compound="top", text_color="#8A3A75",
                              command=lambda: self.open_websites(1)
                              )
        btn_3.place(x=570, y=250)
        btn_4 = ctk.CTkButton(master=content_frame, fg_color="#FFF", height=100, width=100, text="DDWO",
                              image=self.aidds_image_ico, hover_color="#eee", compound="top", text_color="#8A3A75"
                              )
        # btn_4.place(x=550, y=360)

        self.profile_container = ctk.CTkFrame(master=content_frame, fg_color="#EEF9F8", height=360, width=400)
        self.profile_container.place(x=20, y=10)

        profile_data = user_data
        f_name = str(profile_data[1]).upper()
        s_name = str(profile_data[2]).upper()
        ctk.CTkLabel(self.profile_container, text=f"Hello....  {f_name} {s_name}",
                     text_color="#397C93",
                     font=("Rockwell", 20, "bold")).place(x=20, y=20)
        id_label = ctk.CTkLabel(self.profile_container, text=f"I D :", font=("Rockwell", 14, "bold"),
                                text_color="#397C93")
        id_label.place(x=30, y=90)

        ids = ctk.CTkLabel(self.profile_container, text=profile_data[0], font=("Rockwell", 14, "bold"),
                           text_color="#397C93")
        ids.place(x=180, y=90)

        name_label = ctk.CTkLabel(self.profile_container, text=f"Name :",
                                  font=("Rockwell", 14, "bold"), text_color="#397C93")
        name_label.place(x=30, y=120)

        name = ctk.CTkLabel(self.profile_container, text=f"{profile_data[1]} {profile_data[2]}",
                            font=("Rockwell", 14, "bold"), text_color="#397C93")
        name.place(x=180, y=120)

        email_label = ctk.CTkLabel(self.profile_container, text=f"Email :", font=("Rockwell", 14, "bold"),
                                   text_color="#397C93")
        email_label.place(x=30, y=150)

        email = ctk.CTkLabel(self.profile_container, text=profile_data[3], font=("Rockwell", 14, "bold"),
                             text_color="#397C93")
        email.place(x=180, y=150)

        contact_label = ctk.CTkLabel(self.profile_container, text=f"Contact :", font=("Rockwell", 14, "bold"),
                                     text_color="#397C93")
        contact_label.place(x=30, y=180)

        contact = ctk.CTkLabel(self.profile_container, text=profile_data[4], font=("Rockwell", 14, "bold"),
                               text_color="#397C93")
        contact.place(x=180, y=180)

        dob_label = ctk.CTkLabel(self.profile_container, text=f"Date of Birth :", font=("Rockwell", 14, "bold"),
                                 text_color="#397C93")
        dob_label.place(x=30, y=210)

        dob = ctk.CTkLabel(self.profile_container, text=profile_data[5], font=("Rockwell", 14, "bold"),
                           text_color="#397C93")
        dob.place(x=180, y=210)

        gender_label = ctk.CTkLabel(self.profile_container, text=f"Gender :", font=("Rockwell", 14, "bold"),
                                    text_color="#397C93")
        gender_label.place(x=30, y=240)

        gender = ctk.CTkLabel(self.profile_container, text=profile_data[6], font=("Rockwell", 14, "bold"),
                              text_color="#397C93")
        gender.place(x=180, y=240)

        occupation_label = ctk.CTkLabel(self.profile_container, text=f"Occupation :",
                                        font=("Rockwell", 14, "bold"), text_color="#397C93")
        occupation_label.place(x=30, y=270)

        occupation = ctk.CTkLabel(self.profile_container, text=profile_data[7],
                                  font=("Rockwell", 14, "bold"), text_color="#397C93")
        occupation.place(x=180, y=270)

        city_label = ctk.CTkLabel(self.profile_container, text=f"City :", font=("Rockwell", 14, "bold"),
                                  text_color="#397C93")
        city_label.place(x=30, y=300)
        city = ctk.CTkLabel(self.profile_container, text=profile_data[8], font=("Rockwell", 14, "bold"),
                            text_color="#397C93")
        city.place(x=180, y=300)

        state_label = ctk.CTkLabel(self.profile_container, text=f"State :", font=("Rockwell", 14, "bold"),
                                   text_color="#397C93")
        state_label.place(x=30, y=330)

        state = ctk.CTkLabel(self.profile_container, text=profile_data[9], font=("Rockwell", 14, "bold"),
                             text_color="#397C93")
        state.place(x=180, y=330)


if __name__ == '__main__':
    AdminWindow(["hello", " ", " ", " ", " ", " ", " ", "Data Manager", " ", " ", " ", " ", " ", " ", " "]).mainloop()

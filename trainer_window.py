# import PyPDF2
import tkinter as tk
from tkinter.messagebox import *
import customtkinter as ctk
from tkinter import ttk, simpledialog
from tkinter import messagebox
from tkinter import scrolledtext
import view_profile as vp
import main_window as mw
import user_login as ul
import mysql.connector
import webbrowser
import real_test_class as rtc
import model_1_use as mu1
from PIL import ImageTk, Image
import os
import model_1_train as m1


class TrainerWindow(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def exit_window(self):
        self.destroy()

    def open_home(self):
        self.destroy()
        new = mw.MainPage()
        new.mainloop()

    def open_realtime_use(self, id):
        if id == "1":
            mu1.RunModelClass1().deiconify()
        elif id == "2":
            rtc.RealTimeTest().deiconify()
        else:
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

    def create_class(self, class_name):
        data_path = os.path.join("data", class_name)
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            print(f"class created {data_path}")
        else:
            print(f"collect data {data_path}")

    def open_websites(self, btn_id):
        if btn_id == 1:
            webbrowser.open("https://www.islrtc.nic.in/")
        if btn_id == 2:
            webbrowser.open("https://www.swavlambancard.gov.in/cms/about-persons-with-disability")
        if btn_id == 3:
            webbrowser.open("https://wcd.karnataka.gov.in/page/Contact+us/Karnataka+State+Disabilities+Act+Office/kn")
        if btn_id == 4:
            webbrowser.open("https://teachablemachine.withgoogle.com/train")

    def create_class1(self, class_name):
        if class_name == "":
            messagebox.showerror("class name is empty", "class name is empty please enter formatted name")
        else:
            try:
                mydb = mysql.connector.connect(host="localhost", username="root", password="", database="slrs")
                my_cursor = mydb.cursor()
                exist_query = "SELECT * FROM model1_labels WHERE labels = '" + class_name + "'"
                my_cursor.execute(exist_query)
                exist_result = my_cursor.fetchone()
                if exist_result:
                    showinfo("class already exists",
                             "class already exists")
                else:
                    insert_cmd = "insert into model1_labels values ('" + class_name + "')"
                    # val = [
                    #     (class_name)
                    # ]
                    my_cursor.execute(insert_cmd)
                    mydb.commit()
                    print(f"{my_cursor.rowcount} record inserted")
                    print("label inserted successfully, ")
            except mysql.connector.Error as e:
                showerror("Server not response", "Error: Something went wrong")
                print(e)
            data_path = os.path.join("data", class_name)
            if not os.path.exists(data_path):
                os.makedirs(data_path)
                if messagebox.askokcancel("model is ready to collection",
                                          f"Model 1 is ready to collect data for {class_name}"
                                          "'\n click OK to open web cam'"):
                    m1.ModelClass1(class_name, data_path).mainloop()

            else:
                if messagebox.askokcancel("model is ready to train", "Model 1 is ready to train"
                                                                     "'\n click OK to open web cam'"):
                    m1.ModelClass1(class_name, data_path).mainloop()

    def remove_class(self, class_name):
        if class_name == "":
            messagebox.showerror("class name is empty", "class name is empty please enter formatted name")
        else:
            try:
                mydb = mysql.connector.connect(host="localhost", username="root", password="", database="slrs")
                my_cursor = mydb.cursor()
                exist_query = "SELECT * FROM model1_labels WHERE labels = '" + class_name + "'"
                my_cursor.execute(exist_query)
                exist_result = my_cursor.fetchone()
                if exist_result:
                    del_query = "DELETE from model1_labels where labels=%s"
                    val = (class_name,)
                    if askokcancel("confirmation", "Do you want to delete data set"):
                        my_cursor.execute(del_query, val)
                        mydb.commit()
                        showinfo("deleted ", "data set is deleted successfully\nRetrain the model")
                        webbrowser.open("https://teachablemachine.withgoogle.com/train")
                else:
                    showinfo("class name notfound", "data set is doesn't exists")

            except mysql.connector.Error as e:
                showerror("Server not response", "Error: Something went wrong")
                print(e)

    def enter_class_name(self, windows: ctk.CTkToplevel, id):
        if windows.winfo_viewable():
            windows.destroy()
        entry_window = ctk.CTkToplevel(self)
        entry_window.title("Training Model 1")
        entry_window.geometry("500x200")
        entry_window.after(250, lambda: entry_window.iconbitmap('image_folder\\plant.ico'))
        entry_window.grab_set()
        entry_window.focus()
        entry_frame1 = ctk.CTkFrame(master=entry_window, fg_color="#fff")
        entry_frame1.pack(pady=10, padx=10, fill='both', expand=True)
        ctk.CTkLabel(entry_frame1, text="Enter The Class Name",
                     font=("Sitka Text Semibold", 18, "bold")).grid(row=0, column=0, padx=20, pady=30)
        class_entry = ctk.CTkEntry(entry_frame1, fg_color="#f0f0f0", width=150)
        class_entry.grid(row=0, column=1, padx=20, pady=30)
        ok_btn = ctk.CTkButton(entry_frame1, text="Collect Data", fg_color="#8A3A75",
                               corner_radius=10,
                               hover_color="#AA5A95",
                               height=30,
                               font=("Sitka Text Semibold", 14, "bold"),
                               )
        if id == "1":
            ok_btn.configure(command=lambda: self.create_class1(class_entry.get()))
        elif id == "2":
            ok_btn.configure(command=lambda: self.remove_class(class_entry.get()), text="Delete Data set")

        ok_btn.grid(row=1, column=0, padx=20, pady=30)

        cancel1 = ctk.CTkButton(entry_frame1, text="Cancel", fg_color="#8A3A75",
                                corner_radius=10,
                                hover_color="#AA5A95",
                                height=30,
                                font=("Sitka Text Semibold", 14, "bold"),
                                command=entry_window.destroy,
                                )
        cancel1.grid(row=1, column=1, padx=20, pady=30)
        # entry_window.mainloop()

    def train_model(self, option: str):
        if option == "Train Model-1":
            trainer_model1 = ctk.CTkToplevel(self)
            trainer_model1.title("Training Model 1")
            trainer_model1.geometry("700x400")
            trainer_model1.after(250, lambda: trainer_model1.iconbitmap('image_folder\\plant.ico'))
            trainer_model1.grab_set()
            trainer_model1.focus()
            frame1 = ctk.CTkFrame(master=trainer_model1, fg_color="#fff")
            frame1.pack(pady=10, padx=10, fill='both', expand=True)
            ctk.CTkLabel(frame1, text="Train Model 1", text_color="#fff", fg_color="#8A3A75",
                         font=("Sitka Text Semibold", 25, "bold"), width=230, corner_radius=20).pack()

            btn_frame = ctk.CTkFrame(frame1, corner_radius=20, width=650, height=350, fg_color="#ffe5ec")
            btn_frame.pack()
            collect_data_btn = ctk.CTkButton(btn_frame, text="Collect Data", fg_color="#8A3A75",
                                             corner_radius=10,
                                             hover_color="#AA5A95",
                                             height=30, image=self.cam_image_ico,
                                             font=("Sitka Text Semibold", 14, "bold"),
                                             command=lambda: self.enter_class_name(trainer_model1, "1")
                                             )
            train_model_btn = ctk.CTkButton(btn_frame, text="Train Model", fg_color="#8A3A75",
                                            corner_radius=10,
                                            hover_color="#AA5A95",
                                            height=30, image=self.cam_image_ico,
                                            font=("Sitka Text Semibold", 14, "bold"),
                                            command=lambda: self.open_websites(4)
                                            )
            remove_class = ctk.CTkButton(btn_frame, text="Remove Class and Retrain", fg_color="#8A3A75",
                                         corner_radius=10,
                                         hover_color="#AA5A95",
                                         height=30, image=self.cam_image_ico,
                                         font=("Sitka Text Semibold", 14, "bold"),
                                         command=lambda: self.enter_class_name(trainer_model1, "2")
                                         )
            help_train_1 = ctk.CTkButton(btn_frame, text="How to Train Model 1", fg_color="#8A3A75",
                                         corner_radius=10,
                                         hover_color="#AA5A95",
                                         height=30, image=self.cam_image_ico,
                                         font=("Sitka Text Semibold", 14, "bold"),

                                         )
            test = ctk.CTkButton(btn_frame, text="Test Trained Model", fg_color="#8A3A75",
                                 corner_radius=10,
                                 hover_color="#AA5A95",
                                 height=30, image=self.cam_image_ico,
                                 font=("Sitka Text Semibold", 14, "bold"),

                                 )
            cancel = ctk.CTkButton(btn_frame, text="Cancel", fg_color="#8A3A75",
                                   corner_radius=10,
                                   hover_color="#AA5A95",
                                   height=30, image=self.cam_image_ico,
                                   font=("Sitka Text Semibold", 14, "bold"),
                                   command=trainer_model1.destroy
                                   )
            train_model_btn.grid(row=0, column=0, pady=30, )
            collect_data_btn.grid(row=0, column=1, padx=20, pady=30, )
            remove_class.grid(row=1, column=0, padx=20, pady=30)
            help_train_1.grid(row=1, column=1, padx=20, pady=30)
            cancel.grid(row=3, column=0, columnspan=2, pady=30)
            test.grid(row=2, column=0, columnspan=2, pady=30)

            # trainer_model1.mainloop()

        elif option == "":
            pass

    def __init__(self, user_data):
        super().__init__()

        def view_profile():
            if self.winfo_viewable():
                vp.ViewProfile("user", user_data).deiconify()

        # configure the root window
        self.about_us = None
        self.title("Trainer Window")
        self.geometry("1100x650+20+20")
        self.state('zoomed')
        print(user_data)
        self.after(250, lambda: self.iconbitmap('image_folder\\plant.ico'))
        self.focus()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff")
        self.frame.pack(pady=10, padx=10, fill='both', expand=True)

        title_frame = ctk.CTkFrame(master=self.frame, fg_color="#8A3A75", height=100, width=1160)
        title_frame.place(x=50, y=10)

        heading = ctk.CTkLabel(title_frame, text="SIGN  LANGUAGE  RECOGNITION  SYSTEM",
                               font=("Georgia", 25, "bold"), text_color="#FFF")

        heading.place(x=270, y=50)

        slogan = ctk.CTkLabel(title_frame, text="Gesture Speak", padx=10,
                              font=("Brush Script MT", 30, "bold"),
                              text_color="#ffe5ec")
        slogan.place(x=510, y=5)

        # menubar section========================
        menubar_frame = ctk.CTkFrame(master=self.frame, fg_color="#ffe5ec", height=70, width=1000)
        menubar_frame.place(x=50, y=120)

        self.home_img = Image.open("image_folder/icon/house.png")
        self.home_image_ico = ctk.CTkImage(light_image=self.home_img, size=(20, 20))
        home = ctk.CTkButton(menubar_frame, text="Home", fg_color="#fd8891", corner_radius=10,
                             hover_color="#AA5A95",
                             height=30,
                             command=self.open_home,
                             image=self.home_image_ico)
        home.grid(row=0, column=0, pady=20, padx=26)

        self.cam_img = Image.open("image_folder/icon/webcam.png")
        self.cam_image_ico = ctk.CTkImage(light_image=self.cam_img, size=(20, 20))
        train_model = ctk.CTkOptionMenu(menubar_frame, values=["Train Model-1", "Train Model-2"],
                                        fg_color="#fd8891",
                                        button_color="#8A3A75", button_hover_color="#AA5A95", command=self.train_model
                                        )
        train_model.grid(row=0, column=1, pady=20, padx=26)
        train_model.set("Train SLRS Models")

        self.profile_img = Image.open("image_folder/icon/profile.png")
        self.profile_image_ico = ctk.CTkImage(light_image=self.profile_img, size=(20, 20))

        profile = ctk.CTkButton(menubar_frame, text="View Profile", fg_color="#fd8891", corner_radius=10,
                                hover_color="#AA5A95",
                                height=30, image=self.profile_image_ico,
                                command=view_profile
                                )
        profile.grid(row=0, column=2, pady=20, padx=26)

        help_btn = ctk.CTkOptionMenu(menubar_frame, values=["register as Admin", "register as User"],
                                     fg_color="#fd8891",
                                     button_color="#8A3A75", button_hover_color="#AA5A95"
                                     )
        help_btn.grid(row=0, column=3, pady=20, padx=26)
        help_btn.set("Help")

        self.abt_us_img = Image.open("image_folder/icon/info.png")
        self.abt_us_image_ico = ctk.CTkImage(light_image=self.abt_us_img, size=(20, 20))
        about_us = ctk.CTkButton(menubar_frame, text="About us", fg_color="#fd8891", corner_radius=10,
                                 hover_color="#AA5A95",
                                 height=30,
                                 image=self.abt_us_image_ico)
        about_us.grid(row=0, column=4, pady=20, padx=26)
        about_us.configure(command=self.open_about_us)

        self.logout_img = Image.open("image_folder/icon/shutdown.png")
        self.logout_image_ico = ctk.CTkImage(light_image=self.logout_img, size=(20, 20))
        logout_window = ctk.CTkButton(menubar_frame, text="Logout", fg_color="#fd8891", corner_radius=10,
                                      hover_color="#AA5A95",
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
                                         width=30, fg_color="#fd8891", hover_color="#ff6d9f")
        self.prev_button.place(x=30, y=585)

        self.next_img = Image.open("image_folder/icon/farrow.png")
        self.next_image_ico = ctk.CTkImage(light_image=self.next_img, size=(20, 20))

        self.next_button = ctk.CTkButton(master=self.frame, text="", image=self.next_image_ico, command=self.next_image,
                                         width=30, fg_color="#fd8891", hover_color="#ff6d9f")
        self.next_button.place(x=400, y=585)
        self.show_image()

        open_webcam1 = ctk.CTkButton(self.frame, text="Test Model 1", fg_color="#8A3A75", corner_radius=10,
                                     hover_color="#AA5A95",
                                     height=50, image=self.cam_image_ico,
                                     font=("Sitka Text Semibold", 15 ,"bold"),
                                     command=lambda :self.open_realtime_use("1")
                                     )
        open_webcam1.place(x=80, y=570)

        open_webcam2 = ctk.CTkButton(self.frame, text="Test Model 2", fg_color="#8A3A75", corner_radius=10,
                                     hover_color="#AA5A95",
                                     height=50, image=self.cam_image_ico,
                                     font=("Sitka Text Semibold", 15, "bold"),
                                     command=lambda: self.open_realtime_use("2")
                                     )
        open_webcam2.place(x=240, y=570)

        # -------------------------------------------
        content_frame = ctk.CTkFrame(master=self.frame, fg_color="#ffe5ec", height=380, width=700,
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

        self.profile_container = ctk.CTkFrame(master=content_frame, fg_color="#fff5fc", height=360, width=400)
        self.profile_container.place(x=20, y=10)

        profile_data = user_data
        f_name = str(profile_data[1]).upper()
        s_name = str(profile_data[2]).upper()
        ctk.CTkLabel(self.profile_container, text=f"Hello....  {f_name} {s_name}",
                     text_color="#AA5A95",
                     font=("Rockwell", 20, "bold")).grid(row=0, column=0, columnspan=2)

        train_model_btn = ctk.CTkButton(self.profile_container, text="Train Model", fg_color="#8A3A75",
                                        corner_radius=10,
                                        hover_color="#AA5A95",
                                        height=30, image=self.cam_image_ico,
                                        font=("Sitka Text Semibold", 14, "bold"),
                                        command=self.open_realtime_use
                                        )

        collect_data_btn = ctk.CTkButton(self.profile_container, text="Collect Data", fg_color="#8A3A75",
                                         corner_radius=10,
                                         hover_color="#AA5A95",
                                         height=30, image=self.cam_image_ico,
                                         font=("Sitka Text Semibold", 14, "bold"),
                                         command=self.open_realtime_use
                                         )

        remove_class = ctk.CTkButton(self.profile_container, text="Remove Class and Retrain", fg_color="#8A3A75",
                                     corner_radius=10,
                                     hover_color="#AA5A95",
                                     height=30, image=self.cam_image_ico,
                                     font=("Sitka Text Semibold", 14, "bold"),
                                     command=self.open_realtime_use
                                     )

        help_train_1 = ctk.CTkButton(self.profile_container, text="How to Train Model 1", fg_color="#8A3A75",
                                     corner_radius=10,
                                     hover_color="#AA5A95",
                                     height=30, image=self.cam_image_ico,
                                     font=("Sitka Text Semibold", 14, "bold"),
                                     command=self.open_realtime_use
                                     )

        help_train_2 = ctk.CTkButton(self.profile_container, text="How To Train Model 2", fg_color="#8A3A75",
                                     corner_radius=10,
                                     hover_color="#AA5A95",
                                     height=30, image=self.cam_image_ico,
                                     font=("Sitka Text Semibold", 14, "bold"),
                                     command=self.open_realtime_use
                                     )
        remove_model = ctk.CTkButton(self.profile_container, text="Delete Trained Model", fg_color="#8A3A75",
                                     corner_radius=10,
                                     hover_color="#AA5A95",
                                     height=30, image=self.cam_image_ico,
                                     font=("Sitka Text Semibold", 14, "bold"),
                                     command=self.open_realtime_use
                                     )

        train_model_btn.grid(row=2, column=0, padx=20, pady=30, rowspan=1)
        collect_data_btn.grid(row=2, column=1, padx=20, pady=30, rowspan=1)
        remove_class.grid(row=3, column=0, padx=20, pady=30)
        help_train_1.grid(row=3, column=1, padx=20, pady=30)
        help_train_2.grid(row=4, column=0, padx=20, pady=30)
        remove_model.grid(row=4, column=1, padx=20, pady=30)


if __name__ == '__main__':
    TrainerWindow(["hello", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]).mainloop()

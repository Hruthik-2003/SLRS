import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter.messagebox import *
from tkcalendar import DateEntry
import user_registration as ur
import mysql.connector
from tkinter.messagebox import *
import user_window as uw


class UserLogin(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def __init__(self):

        def on_focusout(event):
                user_id_entry.configure(border_width=0)

        def on_entry_click(event):
                user_id_entry.configure(border_width=1)

        def login_activity():

            user_id = user_id_entry.get()
            password = password_entry.get()
            con_pwd = con_password_entry.get()
            if user_id == "" or password == "" or con_pwd == "":
                showerror("Input field is empty", "All information is required please enter information")
            elif password != con_pwd:
                showerror("password not match", "please check password and confirm password should be same")
            else:
                try:
                    mydb = mysql.connector.connect(host="localhost", username="root", password="", database="slrs")
                    my_cursor = mydb.cursor()
                    select_query = "select * from user_table where user_id=%s AND password=%s"
                    val = (user_id, password)
                    my_cursor.execute(select_query, val)
                    rows = my_cursor.fetchone()
                    result_array = []
                    if rows is not None:
                        showinfo("Login Successful", "You have logged in Successfully")
                        if rows:
                            row_data = list(rows)
                            # print(row_data)
                            # print(row_data[7])
                            if self.winfo_viewable():  # If root window is visible
                                self.withdraw()  # Hide root window
                                uw.UserWindow(row_data).deiconify()  # Show window2
                            else:
                                self.deiconify()  # Show root window
                                uw.UserWindow(row_data).withdraw()  # Hide window2

                    else:
                        showerror(title="Login Failed", message="Invalid Username and password")

                except mysql.connector.Error as e:
                    showerror("Server not response", "Error: Something went wrong")

        def open_registration():
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                ur.UserRegistration().deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                ur.UserRegistration().withdraw()  # Hide window2

        def close_operation():
            import main_window as ml
            ml.MainPage().deiconify()
            self.withdraw()

        super().__init__()
        self.title("  USER LOGIN")
        self.geometry("750x450+20+40")
        # icon_image = tk.PhotoImage(file="image_folder\\adminicon_1.ico")
        # ctk.CTkToplevel.iconphoto(self, True, Image.open("image_folder\\adminicon_1.ico"))
        # self.iconbitmap("image_folder\\adminicon_1.ico")
        # self.tk.call("wm", icon_image)
        self.after(250, lambda: self.iconbitmap('image_folder\\enter.ico'))
        self.configure(fg_color="#d5d6d7")
        self.focus()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff", corner_radius=20)
        self.frame.pack(padx=15, pady=15, fill="both", expand=True)

        self.img = Image.open("image_folder/user_login.jpg")
        # self.side_image = ImageTk.PhotoImage(Image.open("image_folder/admin_register.jpg").resize((500, 500)))
        self.side_image = ctk.CTkImage(light_image=self.img, size=(300, 300))

        self.side_image_label = ctk.CTkLabel(master=self.frame, image=self.side_image, text="")
        self.side_image_label.place(x=20, y=80)
        self.side_image_label.image = self.side_image

        head_line = ctk.CTkLabel(self.frame, text="USER LOGIN", text_color="#375862",
                                 font=("Copperplate Gothic Bold", 25, "bold"))
        head_line.place(x=60, y=20)
        field_frame = ctk.CTkFrame(master=self.frame, fg_color="#a4f5ec", corner_radius=20, width=375, height=385,
                                   border_width=3, border_color="#577882")
        field_frame.place(x=320, y=15)

        # user id--------------------------------
        user_id_label = ctk.CTkLabel(master=field_frame,
                                     text_color="#013220",
                                     text="User  I D",
                                     font=("Rockwell", 16, "bold"))
        user_id_label.place(x=70, y=20)

        user_id_entry = ctk.CTkEntry(master=field_frame,
                                     fg_color="#fff", border_width=0, text_color="#022619",
                                     font=("Rockwell", 14, "normal"), width=220, border_color="#223a79")
        user_id_entry.place(x=70, y=50)
        # user_id_entry.bind('<FocusIn>', lambda: on_entry_click("1"))
        # user_id_entry.bind('<FocusOut>', on_focusout)
        # password--------------------------------------
        password_label = ctk.CTkLabel(master=field_frame,
                                      text_color="#013220",
                                      text="Password",
                                      font=("Rockwell", 16, "bold"))
        password_label.place(x=70, y=90)

        password_entry = ctk.CTkEntry(master=field_frame,
                                      fg_color="#fff", border_width=0, text_color="#596b9b",
                                      font=("Rockwell", 10, "normal"), width=150, show=u"\u25CF")
        password_entry.place(x=70, y=120)
        # confirm password--------------------------------------
        con_password_label = ctk.CTkLabel(master=field_frame,
                                          text_color="#013220",
                                          text="Confirm Password",
                                          font=("Rockwell", 16, "bold"))
        con_password_label.place(x=70, y=160)

        con_password_entry = ctk.CTkEntry(master=field_frame,
                                          fg_color="#fff", border_width=0, text_color="#596b9b",
                                          font=("Rockwell", 10, "normal"), width=150, show=u"\u25CF")
        con_password_entry.place(x=70, y=190)
        # buttons--------------------------------
        self.r_img = Image.open("image_folder/icon/pen.png")
        self.reg_image = ctk.CTkImage(light_image=self.r_img, size=(20, 20))
        register_btn = ctk.CTkButton(master=field_frame, text="Register", text_color="#fff", fg_color="#013220",
                                     height=25,
                                     corner_radius=30, hover_color="#596b9b", image=self.reg_image,
                                     command=open_registration)
        register_btn.place(x=200, y=270)

        self.l_img = Image.open("image_folder/icon/login.png")
        self.log_image = ctk.CTkImage(light_image=self.l_img, size=(20, 20))
        login_btn = ctk.CTkButton(master=field_frame, text="Login", text_color="#fff", fg_color="#013220", height=25,
                                  corner_radius=30, hover_color="#596b9b", image=self.log_image,
                                  command=login_activity)
        login_btn.place(x=50, y=270)

        self.c_img = Image.open("image_folder/icon/cancel.png")
        self.cancel_image = ctk.CTkImage(light_image=self.c_img, size=(20, 20))
        cancel_btn = ctk.CTkButton(master=field_frame, text="Cancel", text_color="#fff", fg_color="#013220", height=25,
                                   corner_radius=30, hover_color="#596b9b", image=self.cancel_image,
                                   command=close_operation)
        cancel_btn.place(x=120, y=310)
        self.protocol("WM_DELETE_WINDOW", close_operation)

        fgt_btn = ctk.CTkButton(master=field_frame, text="forget password", text_color="#013220", fg_color="#a4f5ec",
                                hover_color="#afffef", height=10)
        fgt_btn.place(x=120, y=350)


if __name__ == '__main__':
    UserLogin().mainloop()


import tkinter as tk
from tkinter import simpledialog

import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter.messagebox import *
from tkcalendar import DateEntry
import admin_login as al
import mysql.connector
import random
import string


class AdminRegistration(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def __init__(self):
        def on_entry_click(event):
            if f_name_entry.get() == 'First Name':
                f_name_entry.delete(0, tk.END)  # Remove the default text
                # f_name_entry.configure(text_color='black')  # Change the text color
            if l_name_entry.get() == 'Last Name':
                l_name_entry.delete(0, tk.END)

        def on_focusout(event):
            if f_name_entry.get() == '':
                f_name_entry.insert(0, 'First Name')
                # f_name_entry.configure(text_color='gray', font=("Rockwell", 12, "normal"))

            if l_name_entry.get() == '':
                l_name_entry.insert(0, 'Last Name')
                # l_name_entry.configure(text_color='gray', font=("Rockwell", 12, "normal"))

        def opens_admin_login():
            if self.winfo_viewable():  # If root window is visible
                self.withdraw()  # Hide root window
                al.AdminLogin("Admin").deiconify()  # Show window2
            else:
                self.deiconify()  # Show root window
                al.AdminLogin("Admin").withdraw()  # Hide window2

        def checkbox_clicked():
            if var1.get() == 1 and var2.get() == 1:
                register_btn.configure(state=ctk.NORMAL, fg_color="#223a79")
            else:
                register_btn.configure(state=ctk.DISABLED, fg_color="#3b54a4")

        def cancel_operation():
            import main_window as ml
            ml.MainPage().deiconify()
            self.withdraw()

        def admin_registration_activity():

            admin_id = admin_id_entry.get()
            first_name = f_name_entry.get()
            last_name = l_name_entry.get()
            email = email_entry.get()
            contact = contact_entry.get()
            dob = dob_entry.get()
            gender = gender_option.get()
            occupation = occupation_entry.get()
            city = city_entry.get()
            state = state_entry.get()
            characters = string.digits + string.ascii_uppercase
            secretkey = ''.join(random.choices(characters, k=6))

            password = password_entry.get()
            con_password = con_password_entry.get()

            name = f_name_entry.get() + " " + l_name_entry.get()

            if (admin_id == '' or
                    first_name == '' or last_name == '' or first_name == "First Name" or last_name == "Last Name" or
                    email == "" or contact == "" or gender == "" or occupation == "" or state == "" or
                    password == "" or con_password == ""):
                showerror("ERROR:\nDetail(s) is/are empty", "All details are required \nplease check if input is empty")
                self.focus()
            elif password != con_password:
                showerror("ERROR:password error",
                          "Password and Confirm Password are not equal\n pleas check once again")
                self.focus()
            else:
                try:
                    mydb = mysql.connector.connect(host="localhost", username="root", password="", database="slrs")
                    my_cursor = mydb.cursor()
                    exist_query = "SELECT * FROM admin_table WHERE admin_id = %s"
                    my_cursor.execute(exist_query, (admin_id,))
                    exist_result = my_cursor.fetchone()
                    if exist_result:
                        showinfo("admin already exists",
                                 "admin already registered please login \nor try different admin ID")
                    else:
                        insert_cmd = "insert into admin_table(admin_id,f_name,l_name,email,contact,dob,gender,occupation,city,state,password,a_and_p,secretekey) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val = [
                            (
                                admin_id, first_name, last_name, email, contact, dob, gender, occupation, city, state,
                                password,
                                "YES", secretkey)
                        ]
                        my_cursor.executemany(insert_cmd, val)
                        mydb.commit()
                        print(f"{my_cursor.rowcount} record inserted")
                        showinfo("Registration successful", "Registration completed successful.....! ")
                        showinfo("SECRETE KEY", f"your secrete key is : {secretkey}")

                except mysql.connector.Error as e:
                    showerror("Server not response", "Error: Something went wrong")

        super().__init__()

        self.title("  ADMIN REGISTRATION")
        self.geometry("950x600+20+40")
        # icon_image = tk.PhotoImage(file="image_folder\\adminicon_1.ico")
        # ctk.CTkToplevel.iconphoto(self, True, Image.open("image_folder\\adminicon_1.ico"))
        # self.iconbitmap("image_folder\\adminicon_1.ico")
        # self.tk.call("wm", icon_image)
        self.after(250, lambda: self.iconbitmap('image_folder\\adminicon_1.ico'))
        self.configure(fg_color="#ffe5ec")
        self.focus()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff", corner_radius=20)
        self.frame.pack(padx=15, pady=15, fill="both", expand=True)

        self.img = Image.open("image_folder/admin_register.jpg")
        # self.side_image = ImageTk.PhotoImage(Image.open("image_folder/admin_register.jpg").resize((500, 500)))
        self.side_image = ctk.CTkImage(light_image=self.img, size=(350, 350))

        self.side_image_label = ctk.CTkLabel(master=self.frame, image=self.side_image, text="")
        self.side_image_label.place(x=10, y=80)
        self.side_image_label.image = self.side_image

        head_line = ctk.CTkLabel(self.frame, text="ADMIN REGISTRATION", text_color="#586998",
                                 font=("Copperplate Gothic Bold", 25, "bold"))
        head_line.place(x=20, y=20)
        field_frame = ctk.CTkFrame(master=self.frame, fg_color="#a3c9fe", corner_radius=20, width=510, height=540)
        field_frame.place(x=380, y=20)

        # admin id entry's--------------------------------------
        admin_id_label = ctk.CTkLabel(master=field_frame,
                                      text_color="#223a79",
                                      text="Admin ID",
                                      font=("Rockwell", 16, "bold"))
        admin_id_label.place(x=30, y=30)

        admin_id_entry = ctk.CTkEntry(master=field_frame,
                                      fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                      font=("Rockwell", 14, "normal"), width=250)
        admin_id_entry.place(x=130, y=30)
        # name entry--------------------------------------------

        name_label = ctk.CTkLabel(master=field_frame,
                                  text_color="#223a79",
                                  text="Name",
                                  font=("Rockwell", 16, "bold"))
        name_label.place(x=30, y=70)
        f_name_entry = ctk.CTkEntry(master=field_frame,
                                    fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                    font=("Rockwell", 14, "normal"), width=175)
        f_name_entry.insert(0, 'First Name')
        f_name_entry.bind('<FocusIn>', on_entry_click)
        f_name_entry.bind('<FocusOut>', on_focusout)

        f_name_entry.place(x=130, y=70)

        l_name_entry = ctk.CTkEntry(master=field_frame,
                                    fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                    font=("Rockwell", 14, "normal"), width=175)
        l_name_entry.place(x=315, y=70)
        l_name_entry.insert(0, 'Last Name')
        l_name_entry.bind('<FocusIn>', on_entry_click)
        l_name_entry.bind('<FocusOut>', on_focusout)

        # Email--------------------------------------
        email_label = ctk.CTkLabel(master=field_frame,
                                   text_color="#223a79",
                                   text="Email",
                                   font=("Rockwell", 16, "bold"))
        email_label.place(x=30, y=110)

        email_entry = ctk.CTkEntry(master=field_frame,
                                   fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                   font=("Rockwell", 14, "normal"), width=250)
        email_entry.place(x=130, y=110)

        # Contact--------------------------------------
        contact_label = ctk.CTkLabel(master=field_frame,
                                     text_color="#223a79",
                                     text="Contact",
                                     font=("Rockwell", 16, "bold"))
        contact_label.place(x=30, y=150)

        contact_entry = ctk.CTkEntry(master=field_frame,
                                     fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                     font=("Rockwell", 14, "normal"), width=250)
        contact_entry.place(x=130, y=150)

        # Date of Birth----------------------------------------
        dob_label = ctk.CTkLabel(master=field_frame,
                                 text_color="#223a79",
                                 text="Date Of Birth",
                                 font=("Rockwell", 16, "bold"))
        dob_label.place(x=30, y=190)

        dob_entry = DateEntry(field_frame, foreground='white', borderwidth=0,
                              font=("Rockwell", 14, "normal"), background="#596b9b")
        dob_entry.place(x=230, y=290)
        # gender--------------------------------------------

        gen_label = ctk.CTkLabel(master=field_frame,
                                 text_color="#223a79",
                                 text="Gender",
                                 font=("Rockwell", 16, "bold"))
        gen_label.place(x=290, y=190)
        gen_frame = ctk.CTkFrame(master=field_frame, fg_color="#ddecff", height=80, width=80)
        gen_frame.place(x=360, y=190)

        gender_option = tk.StringVar()
        male = ctk.CTkRadioButton(master=gen_frame, text="Male", text_color="#596b9b",
                                  font=("Rockwell", 14, "normal"), fg_color="#223a79",
                                  radiobutton_height=14, radiobutton_width=14,
                                  variable=gender_option, value="male")
        male.grid(row=0, column=0, padx=5, pady=5)
        female = ctk.CTkRadioButton(master=gen_frame, text="Female", text_color="#596b9b",
                                    font=("Rockwell", 14, "normal"), fg_color="#223a79",
                                    radiobutton_height=14, radiobutton_width=14,
                                    variable=gender_option, value="female")
        female.grid(row=1, column=0, padx=5, pady=5)
        other = ctk.CTkRadioButton(master=gen_frame, text="Others", text_color="#596b9b",
                                   font=("Rockwell", 14, "normal"), fg_color="#223a79",
                                   radiobutton_height=14, radiobutton_width=14,
                                   variable=gender_option, value="others")

        other.grid(row=2, column=0, padx=5, pady=5)
        # occupation-----------------------------------------
        occupation_label = ctk.CTkLabel(master=field_frame,
                                        text_color="#223a79",
                                        text="Occupation",
                                        font=("Rockwell", 16, "bold"))
        occupation_label.place(x=30, y=230)

        occupations = [
            "",
            "SLRS Trainer",
            "Data Manager",

        ]
        occupation_entry = ctk.CTkOptionMenu(master=field_frame,
                                             text_color="#596b9b",
                                             font=("Rockwell", 14, "normal"),
                                             values=occupations, fg_color="#ddecff", button_hover_color="#ade8f4",
                                             dropdown_text_color="#596b9b", dropdown_fg_color="#fff", corner_radius=10,
                                             dropdown_hover_color="#caf0f8",
                                             button_color="#ddecff")
        occupation_entry.place(x=140, y=230)

        # city--------------------------------------------
        city_label = ctk.CTkLabel(master=field_frame,
                                  text_color="#223a79",
                                  text="City",
                                  font=("Rockwell", 16, "bold"))
        city_label.place(x=30, y=270)

        city_entry = ctk.CTkEntry(master=field_frame,
                                  fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                  font=("Rockwell", 14, "normal"), width=150)
        city_entry.place(x=140, y=270)
        # state----------------------------------------
        state_label = ctk.CTkLabel(master=field_frame,
                                   text_color="#223a79",
                                   text="State",
                                   font=("Rockwell", 16, "bold"))
        state_label.place(x=30, y=310)

        state_list = ["", "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh",
                      "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli",
                      "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
                      "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadweep",
                      "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
                      "Nagaland", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim",
                      "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
                      "West Bengal"]

        state_entry = ctk.CTkOptionMenu(master=field_frame,
                                        text_color="#596b9b",
                                        font=("Rockwell", 14, "normal"),
                                        values=state_list, fg_color="#ddecff", button_hover_color="#ade8f4",
                                        dropdown_text_color="#596b9b", dropdown_fg_color="#fff", corner_radius=10,
                                        dropdown_hover_color="#caf0f8",
                                        button_color="#ddecff")
        state_entry.place(x=140, y=310)
        # pwd frame-----------------------
        pwd_frame = ctk.CTkFrame(master=field_frame, fg_color="#91bfff", height=120, width=450)
        pwd_frame.place(x=20, y=360)

        # password--------------------------------------
        password_label = ctk.CTkLabel(master=pwd_frame,
                                      text_color="#223a79",
                                      text="Password",
                                      font=("Rockwell", 16, "bold"))
        password_label.place(x=15, y=20)

        password_entry = ctk.CTkEntry(master=pwd_frame,
                                      fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                      font=("Rockwell", 10, "normal"), width=150, show=u"\u25CF")
        password_entry.place(x=170, y=20)
        # confirm password--------------------------------------
        con_password_label = ctk.CTkLabel(master=pwd_frame,
                                          text_color="#223a79",
                                          text="Confirm Password",
                                          font=("Rockwell", 16, "bold"))
        con_password_label.place(x=15, y=70)

        con_password_entry = ctk.CTkEntry(master=pwd_frame,
                                          fg_color="#ddecff", border_width=0, text_color="#596b9b",
                                          font=("Rockwell", 10, "normal"), width=150, show=u"\u25CF")
        con_password_entry.place(x=170, y=70)
        # agree----------------------------
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        checkbox1 = tk.Checkbutton(field_frame,
                                   text="The above information is true to the best of my knowledge ",
                                   variable=var1, fg="#00f", font=("Arial", 12, "normal"), bg="#a3c9fe",
                                   command=checkbox_clicked)
        checkbox1.place(x=70, y=730)
        checkbox2 = tk.Checkbutton(field_frame,
                                   text="I agree to the terms and conditions ",
                                   variable=var2, fg="#00f", font=("Arial", 12, "normal"), bg="#a3c9fe",
                                   command=checkbox_clicked)
        checkbox2.place(x=70, y=760)

        # buttons--------------------------------
        self.r_img = Image.open("image_folder/icon/pen.png")
        self.reg_image = ctk.CTkImage(light_image=self.r_img, size=(20, 20))
        register_btn = ctk.CTkButton(master=self.frame, text="Register", text_color="#fff", fg_color="#3b54a4",
                                     height=35,
                                     corner_radius=30, hover_color="#596b9b", image=self.reg_image,
                                     command=admin_registration_activity, state=ctk.DISABLED)
        register_btn.place(x=30, y=450)

        self.l_img = Image.open("image_folder/icon/login.png")
        self.log_image = ctk.CTkImage(light_image=self.l_img, size=(20, 20))
        login_btn = ctk.CTkButton(master=self.frame, text="Login", text_color="#fff", fg_color="#223a79", height=35,
                                  corner_radius=30, hover_color="#596b9b", image=self.log_image,
                                  command=opens_admin_login)
        login_btn.place(x=200, y=450)

        self.c_img = Image.open("image_folder/icon/cancel.png")
        self.cancel_image = ctk.CTkImage(light_image=self.c_img, size=(20, 20))
        cancel_btn = ctk.CTkButton(master=self.frame, text="Cancel", text_color="#fff", fg_color="#223a79", height=35,
                                   corner_radius=30, hover_color="#596b9b", image=self.cancel_image,
                                   command=cancel_operation)
        self.protocol("WM_DELETE_WINDOW", cancel_operation)
        cancel_btn.place(x=100, y=500)


if __name__ == '__main__':
    AdminRegistration().mainloop()

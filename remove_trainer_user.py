import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
# from tkinter.messagebox import *
# from tkcalendar import DateEntry
# import user_registration as ur
import mysql.connector
from tkinter.messagebox import *
# import user_window as uw


class RemoveUser(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def __init__(self):

        def remove_activity():

            user_id = user_id_entry.get()
            print(user_id)

            if user_id == "":
                showerror("Input field is empty", "All information is required please enter information")

            else:
                try:
                    user_id = user_id_entry.get()
                    mydb = mysql.connector.connect(host="localhost", username="root", password="", database="slrs")
                    my_cursor = mydb.cursor()
                    del_query = "DELETE from user_table where user_id = %s"
                    if str(users_option.get()).lower() == "user":
                        del_query = f"DELETE from user_table where user_id = %s"

                    if str(users_option.get()).lower() == "trainer":
                        del_query = f"DELETE from trainer_table where trainer_id = %s"

                    # val = user_id
                    # my_cursor.execute(del_query, val)
                    my_cursor.execute(del_query,(user_id,))


                    mydb.commit()
                    rows = my_cursor.fetchone()

                    if my_cursor.rowcount == 1:
                        if askokcancel("confirmation", "Are you sure to remove account"):
                            showinfo("Account Removed", "Account removed")
                            self.destroy()

                    else:
                        showerror(title="Failed to remove", message="Invalid User id")

                except mysql.connector.Error as e:
                    showerror("Server not response", "Error: Something went wrong")
                    print(e)

        def close_operation():
            import main_window as ml
            ml.MainPage().deiconify()
            self.withdraw()

        super().__init__()
        self.title("  Remove Account")
        self.geometry("750x450+20+40")
        # icon_image = tk.PhotoImage(file="image_folder\\adminicon_1.ico")
        # ctk.CTkToplevel.iconphoto(self, True, Image.open("image_folder\\adminicon_1.ico"))
        # self.iconbitmap("image_folder\\adminicon_1.ico")
        # self.tk.call("wm", icon_image)
        self.after(250, lambda: self.iconbitmap('image_folder\\enter.ico'))
        self.configure(fg_color="#ffb3c1")
        self.focus()
        self.grab_set()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff", corner_radius=20)
        self.frame.pack(padx=15, pady=15, fill="both", expand=True)

        self.img = Image.open("image_folder/d_d/remove_account.jpg")
        # self.side_image = ImageTk.PhotoImage(Image.open("image_folder/admin_register.jpg").resize((500, 500)))
        self.side_image = ctk.CTkImage(light_image=self.img, size=(300, 300))

        self.side_image_label = ctk.CTkLabel(master=self.frame, image=self.side_image, text="")
        self.side_image_label.place(x=20, y=80)
        self.side_image_label.image = self.side_image

        head_line = ctk.CTkLabel(self.frame, text="Remove Account", text_color="#c9184a",
                                 font=("Copperplate Gothic Bold", 25, "bold"))
        head_line.place(x=40, y=20)
        field_frame = ctk.CTkFrame(master=self.frame, fg_color="#ffccd5", corner_radius=20, width=375, height=385)
        field_frame.place(x=320, y=15)
        # user type-----------------------------
        u_type_label = ctk.CTkLabel(master=field_frame,
                                    text_color="#c9184a",
                                    text="User Type",
                                    font=("Rockwell", 16, "bold"))
        u_type_label.place(x=30, y=50)
        u_type_frame = ctk.CTkFrame(master=field_frame, fg_color="#ddecff", height=80, width=80)
        u_type_frame.place(x=130, y=50)

        users_option = tk.StringVar()
        trainer = ctk.CTkRadioButton(master=u_type_frame, text="Trainer", text_color="#596b9b",
                                     font=("Rockwell", 14, "normal"), fg_color="#a4133c",
                                     radiobutton_height=14, radiobutton_width=14,
                                     variable=users_option, value="trainer")
        trainer.grid(row=0, column=0, padx=5, pady=5)
        user = ctk.CTkRadioButton(master=u_type_frame, text="User", text_color="#596b9b",
                                  font=("Rockwell", 14, "normal"), fg_color="#a4133c",
                                  radiobutton_height=14, radiobutton_width=14,
                                  variable=users_option, value="user")
        user.grid(row=0, column=1, padx=5, pady=5)
        # user id--------------------------------
        user_id_label = ctk.CTkLabel(master=field_frame,
                                     text_color="#c9184a",
                                     text="User  I D",
                                     font=("Rockwell", 16, "bold"))
        user_id_label.place(x=30, y=130)

        user_id_entry = ctk.CTkEntry(master=field_frame,
                                     fg_color="#fff", border_width=0, text_color="#022619",
                                     font=("Rockwell", 14, "normal"), width=220)
        user_id_entry.place(x=130, y=130)

        # # password--------------------------------------
        # password_label = ctk.CTkLabel(master=field_frame,
        #                               text_color="#c9184a",
        #                               text="Password",
        #                               font=("Rockwell", 16, "bold"))
        # password_label.place(x=70, y=90)
        #
        # password_entry = ctk.CTkEntry(master=field_frame,
        #                               fg_color="#fff", border_width=0, text_color="#596b9b",
        #                               font=("Rockwell", 10, "normal"), width=150, show=u"\u25CF")
        # password_entry.place(x=70, y=120)
        # # confirm password--------------------------------------
        # con_password_label = ctk.CTkLabel(master=field_frame,
        #                                   text_color="#c9184a",
        #                                   text="Confirm Password",
        #                                   font=("Rockwell", 16, "bold"))
        # con_password_label.place(x=70, y=160)
        #
        # con_password_entry = ctk.CTkEntry(master=field_frame,
        #                                   fg_color="#fff", border_width=0, text_color="#596b9b",
        #                                   font=("Rockwell", 10, "normal"), width=150, show=u"\u25CF")
        # con_password_entry.place(x=70, y=190)
        # buttons--------------------------------
        self.r_img = Image.open("image_folder/icon/pen.png")
        self.rm_image = ctk.CTkImage(light_image=self.r_img, size=(20, 20))
        remove_btn = ctk.CTkButton(master=field_frame, text="Remove Account", text_color="#fff", fg_color="#a4133c",
                                   height=25,
                                   corner_radius=30, hover_color="#596b9b", image=self.rm_image,
                                   command=remove_activity
                                   )
        remove_btn.place(x=200, y=270)

        self.c_img = Image.open("image_folder/icon/cancel.png")
        self.cancel_image = ctk.CTkImage(light_image=self.c_img, size=(20, 20))
        cancel_btn = ctk.CTkButton(master=field_frame, text="Cancel", text_color="#fff", fg_color="#a4133c", height=25,
                                   corner_radius=30, hover_color="#596b9b", image=self.cancel_image,
                                   command=self.destroy)
        cancel_btn.place(x=50, y=270)
        # self.protocol("WM_DELETE_WINDOW", close_operation)


if __name__ == '__main__':
    RemoveUser().mainloop()

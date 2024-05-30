import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter.messagebox import *
import user_login as ul
import remove_account as ra


class ViewProfile(ctk.CTkToplevel):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    def __init__(self, user_type, profile_data):

        def cancel_operation():
            self.destroy()

        def removing_account():
            ra.RemoveAccount(user_type,str(profile_data[0])).deiconify()

        super().__init__()
        self.title(f"{user_type} profile")
        self.geometry("450x550")

        self.after(250, lambda: self.iconbitmap(r"image_folder\enteruser.ico"))
        self.configure(fg_color="#f2e2e2")
        # self.focus_set()
        self.grab_set()
        # self.focus_force()
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff", corner_radius=20)
        self.frame.pack(padx=15, pady=15, fill="both", expand=True)
        img_path = "image_folder/icon/user.png"
        if profile_data[6] == "male":
            img_path = "image_folder/icon/man.png"
        elif profile_data[6] == "female":
            img_path = "image_folder/icon/woman.png"
        else:
            img_path = "image_folder/icon/user.png"

        self.img = Image.open(img_path)
        self.side_image = ctk.CTkImage(light_image=self.img, size=(70, 70))

        self.side_image_label = ctk.CTkLabel(master=self.frame, image=self.side_image, text="")
        self.side_image_label.place(x=155, y=00)
        self.side_image_label.image = self.side_image

        id_label = ctk.CTkLabel(self.frame, text=f"I D :", font=("Rockwell", 14, "bold"),
                                text_color="#AA5A95")
        id_label.place(x=30, y=90)

        ids = ctk.CTkLabel(self.frame, text=profile_data[0], font=("Rockwell", 14, "bold"),
                           text_color="#AA5A95")
        ids.place(x=180, y=90)

        name_label = ctk.CTkLabel(self.frame, text=f"Name :",
                                  font=("Rockwell", 14, "bold"), text_color="#AA5A95")
        name_label.place(x=30, y=120)

        name = ctk.CTkLabel(self.frame, text=f"{profile_data[1]} {profile_data[2]}",
                            font=("Rockwell", 14, "bold"), text_color="#AA5A95")
        name.place(x=180, y=120)

        email_label = ctk.CTkLabel(self.frame, text=f"Email :", font=("Rockwell", 14, "bold"),
                                   text_color="#AA5A95")
        email_label.place(x=30, y=150)

        email = ctk.CTkLabel(self.frame, text=profile_data[3], font=("Rockwell", 14, "bold"),
                             text_color="#AA5A95")
        email.place(x=180, y=150)

        contact_label = ctk.CTkLabel(self.frame, text=f"Contact :", font=("Rockwell", 14, "bold"),
                                     text_color="#AA5A95")
        contact_label.place(x=30, y=180)

        contact = ctk.CTkLabel(self.frame, text=profile_data[4], font=("Rockwell", 14, "bold"),
                               text_color="#AA5A95")
        contact.place(x=180, y=180)

        dob_label = ctk.CTkLabel(self.frame, text=f"Date of Birth :", font=("Rockwell", 14, "bold"),
                                 text_color="#AA5A95")
        dob_label.place(x=30, y=210)

        dob = ctk.CTkLabel(self.frame, text=profile_data[5], font=("Rockwell", 14, "bold"),
                           text_color="#AA5A95")
        dob.place(x=180, y=210)

        gender_label = ctk.CTkLabel(self.frame, text=f"Gender :", font=("Rockwell", 14, "bold"),
                                    text_color="#AA5A95")
        gender_label.place(x=30, y=240)

        gender = ctk.CTkLabel(self.frame, text=profile_data[6], font=("Rockwell", 14, "bold"),
                              text_color="#AA5A95")
        gender.place(x=180, y=240)

        occupation_label = ctk.CTkLabel(self.frame, text=f"Occupation :",
                                        font=("Rockwell", 14, "bold"), text_color="#AA5A95")
        occupation_label.place(x=30, y=270)

        occupation = ctk.CTkLabel(self.frame, text=profile_data[7],
                                  font=("Rockwell", 14, "bold"), text_color="#AA5A95")
        occupation.place(x=180, y=270)

        city_label = ctk.CTkLabel(self.frame, text=f"City :", font=("Rockwell", 14, "bold"),
                                  text_color="#AA5A95")
        city_label.place(x=30, y=300)
        city = ctk.CTkLabel(self.frame, text=profile_data[8], font=("Rockwell", 14, "bold"),
                            text_color="#AA5A95")
        city.place(x=180, y=300)

        state_label = ctk.CTkLabel(self.frame, text=f"State :", font=("Rockwell", 14, "bold"),
                                   text_color="#AA5A95")
        state_label.place(x=30, y=330)

        state = ctk.CTkLabel(self.frame, text=profile_data[9], font=("Rockwell", 14, "bold"),
                             text_color="#AA5A95")
        state.place(x=180, y=330)

        self.c_img = Image.open("image_folder/icon/cancel.png")
        self.cancel_image = ctk.CTkImage(light_image=self.c_img, size=(20, 20))
        cancel_btn = ctk.CTkButton(master=self.frame, text="Cancel", text_color="#fff", fg_color="#9A4A75", height=35,
                                   corner_radius=30, hover_color="#596b9b", image=self.cancel_image,
                                   command=cancel_operation)
        cancel_btn.place(x=40, y=410)

        self.d_img = Image.open("image_folder/icon/delete.png")
        self.delete_image = ctk.CTkImage(light_image=self.d_img, size=(20, 20))
        delete_btn = ctk.CTkButton(master=self.frame, text="Remove account", text_color="#fff", fg_color="#9A4A75",
                                   height=35,
                                   corner_radius=30, hover_color="#596b9b", image=self.delete_image,
                                   command=removing_account)
        delete_btn.place(x=190, y=410)


if __name__ == '__main__':
    ViewProfile("hello",
                ["lsakndc", "lakc", "lakc", "lsakndc", "lakc", "lakc", "lsakndc", "lakc", "lakc", "cxbx"]).mainloop()

import customtkinter as ctk

root = ctk.CTk()
root.configure(width=300,height=300)
root.title("hello window")
hello=ctk.CTkFrame(master=root,fg_color="#23f4f4",corner_radius=20).pack()
ctk.CTkLabel(master=hello,text="Hello shreyu",text_color="#00f").pack()
root.mainloop()

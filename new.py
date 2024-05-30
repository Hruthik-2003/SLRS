# import main_window
import customtkinter as ctk


class Click(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("hello")
        self.btn = ctk.CTkButton(self, text="click", command=self.bbt)
        self.btn.pack()
        self.mainloop()

    def bbt(self):
        self.quit()
        import main_window
        main_window.MainPage().mainloop()


Click()

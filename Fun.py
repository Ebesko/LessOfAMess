import customtkinter as ctk

app = ctk.CTk()
app.geometry("800x800")
ctk.set_appearance_mode("light")

app.title("TEST OF SHOW-HIDE")
app.rowconfigure((0, 1, 2), weight=1)
app.columnconfigure((0, 1, 2), weight=1)

app.mainloop()
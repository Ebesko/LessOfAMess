import customtkinter as ctk
import tkinter as tk
from data.MajorSubject import Major
import data.MinorSubjectList as MS
from User_Interface.frame_major_subject import CreateFrameMajorSubject
from User_Interface.frame_minor_one import CreateMinorFrame
from User_Interface.frame_minor_two import CreateMiniMinorFrame
import save as svg
import load as ld


class WindowMained:
    def __init__(self):
        ### DATA
        # MAJOR

        #self.dataframed = Major("https://ekvv.uni-bielefeld.de/sinfo/publ/variante/80471673?m").dfmajor()
        #self.dataframed_title = Major("https://ekvv.uni-bielefeld.de/sinfo/publ/variante/80471673?m").title()

        self.dataframed = Major("https://ekvv.uni-bielefeld.de/sinfo/publ/variante/80471673?m")
        # MINOR
        self.url_possible_minors = "https://ekvv.uni-bielefeld.de/sinfo/publ/variante/80471673"
        self.object_available_minors = MS.Minor(self.url_possible_minors)

        self.available_minors = self.object_available_minors.minors()
        self.available_miniminors = self.object_available_minors.mini_minors()

        ###APP
        self.app = ctk.CTk()
        self.app.geometry("1800x800")
        # ctk.set_appearance_mode("dark")

        self.app.title("Dashboard of courses")
        self.app.rowconfigure((0, 1, 2), weight=1)
        self.app.columnconfigure((0, 1, 2), weight=1)

        # MENU
        self.main_menu = tk.Menu(self.app)
        self.app.config(menu=self.main_menu)

        # FILE MENU
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save",
                                   command=lambda: svg.save_progress(self.major_frame, self.minor_frame, self.miniminorframe),
                                   accelerator="Ctrl + S")
        self.file_menu.add_command(label="Load", command=lambda: self.load.restore_all())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Reset", command=lambda: self.reset.reset_all(), accelerator="Ctrl + R")

        ### UPDATE MENU ---------------------------------------------------------------------------------------
        """ ça marche pas parce qu'on veut update ce qu'on croit être un objet 
        mais c'est un dict returns par l'objet en question. Chuis fatiguée, revenez demain."""

        self.update_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Update Courses", menu=self.update_menu)
        self.update_menu.add_command(label="Update Major",
                                   command=lambda: self.major_frame.major_df_update())
        self.update_menu.add_command(label="Update Minors",
                                     command=lambda: self.minor_frame.minor_one_df_update())

        ### Sogennant cemtary of the mess:
        # file_menu.add_command(label="Close", command=lambda: print("4"))
        # file_menu.add_command(label="New", command=lambda: print("1"))
        # file_menu.add_command(label="Exit", command=app.quit)

        # FRAMES
        self.major_frame = CreateFrameMajorSubject(self.app, self.dataframed)
        self.miniminorframe = CreateMiniMinorFrame(self.app, self.available_miniminors)
        self.minor_frame = CreateMinorFrame(self.app, source=self.object_available_minors,
                                            miniframe=self.miniminorframe)

        # Frame mini-minor get frame minor to check if same selected on both
        self.miniminorframe.get_other_frame(self.minor_frame)

        # Setup functions Load & Reset
        self.load = ld.loading(self.major_frame, self.minor_frame, self.miniminorframe)
        self.reset = ld.loading(self.major_frame, self.minor_frame, self.miniminorframe)

        # Bind shortcuts to app
        self.app.bind_all("<Control-s>",
                          lambda event: svg.save_progress(self.major_frame, self.minor_frame, self.miniminorframe))
        self.app.bind_all("<Control-r>",
                          lambda event: self.reset.reset_all())
        self.app.bind_all("<Button-1>",
                          lambda event: svg.save_progress(self.major_frame, self.minor_frame, self.miniminorframe))

        # Automatic load of the last session
        self.load.restore_all()

        # LOOP
        self.app.mainloop()

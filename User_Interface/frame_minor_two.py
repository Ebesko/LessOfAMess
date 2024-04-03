import customtkinter as ctk
from data.MinorSubject import Minor
from User_Interface.checkboxes import CheckboxesValued


class CreateMiniMinorFrame(ctk.CTkFrame):
    def __init__(self, master, dict_minors, **kwargs):
        super().__init__(master, **kwargs)
        self.minor1 = None
        self.dict_minors = dict_minors
        self.actual = None
        self.minor_load = 0

        # INIT FRAME
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)
        self.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # CATEGORY OF MINOR
        self.label_minor = ctk.CTkLabel(self, text="Zweite kleine Nebenfach: ")
        self.label_minor.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # OPTION MENU FOR MINOR
        self.minor_choice_var = ctk.IntVar()
        self.minor_menu_var = ctk.StringVar(value="Wählen...")
        self.minor_list = ["Wählen..."]
        if self.dict_minors is not None:
            for key in self.dict_minors:
                self.minor_list.append(key)
        self.minor_menu = ctk.CTkOptionMenu(self,
                                            variable=self.minor_menu_var,
                                            values=self.minor_list,
                                            command=self.different_miniminor2)
        self.minor_menu.set("Wählen...")
        self.minor_menu.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # EXTRA FRAME
        self.extra_frame = ctk.CTkFrame(self)
        self.extra_frame.rowconfigure((0), weight=1)
        self.extra_frame.columnconfigure((0), weight=1)
        self.extra_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

    #GET MINOR
    def get_other_frame(self, minor1):
        self.minor1 = minor1

    ### FOR MINOR 1 (other frame)
    # CLEANS MINI-MINOR (SELF) WHEN MINOR CHOOSEN (OTHER FRAME)
    def reset_minimenu(self):
        if self.minor_menu != "Wählen..." and self.actual is not None:
            self.actual.delframe()
            self.minor_menu.set("Wählen...")
    # TO PASS TO OTHER FRAME FOR MINI-MINOR INCOMPATIBILITIES
    def gives_minimenu(self):
        return self.minor_menu_var

    def different_miniminor2(self, choice):
        if self.minor1.gives_minormenu().get() != "Wählen...":
            self.minor1.gives_minormenu().set("Wählen...")
            self.minor1.progress_minor_cleaner()

        if self.minor_menu_var.get() != self.minor1.gives_miniminormenu().get():
            self.get_df(choice, True)

        if self.minor_menu_var.get() == self.minor1.gives_miniminormenu().get():
            self.get_df(choice, False)
            self.minor_menu_var.set("Wählen...")

    # CREATE CHECKBOXES
    def get_df(self, choice, validity):
        if self.actual is not None:
            self.actual.delframe()
            if choice != "Wählen...":
                url = self.dict_minors[choice]
                dframed = Minor(url, choice).dfminor()
                self.actual = CheckboxesValued(self.extra_frame, dframed, validity, points=30)
        else:
            if choice in self.dict_minors:
                url = self.dict_minors[choice]
                dframed = Minor(url, choice).dfminor()
                self.actual = CheckboxesValued(self.extra_frame, dframed, validity, points=30)

    ### SAVE FUNCTIONS
    def save1(self):
        if self.minor_menu.get() != "Wählen...":
            return self.minor_menu.get()
        else:
            return None

    def save2(self):
        if self.actual is not None:
            if self.minor_menu.get() != "Wählen...":
                return self.actual.save()
        else:
            return None

    ### FUNCTIONS TO LOAD
    def all_cleaned(self):
        if self.actual is not None:
            self.actual.delframe()
        self.minor_menu_var.set("Wählen...")

    def restore_subject(self, subject):
        self.minor_menu_var.set(subject)
        if subject != "Wählen...":
            self.get_df(subject, True)

    def restore_progress(self, values):
        if self.actual is not None:
            my_dict = self.actual.dict_chk
            for i, chk in enumerate(my_dict):
                if values[i] != 0:
                    my_dict[chk.strip('-')].toggle()
        else:
            self.minor_menu_var.set("Wählen...")

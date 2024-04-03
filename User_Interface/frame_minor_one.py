import customtkinter as ctk
from data.MinorSubject import Minor
from User_Interface.checkboxes import CheckboxesValued


class CreateMinorFrame(ctk.CTkFrame):
    def __init__(self, master, source, miniframe, **kwargs):
        super().__init__(master, **kwargs)
        self.object_source = source

        #self.dict_minors = dict_minors
        #self.dict_miniminors = dict_miniminors
        self.dict_minors = self.object_source.minors()
        self.dict_miniminors = self.object_source.mini_minors()

        self.miniframe = miniframe
        self.actual = None

        #self.other = self.miniframe.gives_minimenu()

        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1), weight=1)
        self.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # NBF LABELS
        self.label_minor = ctk.CTkLabel(self, text="Nebenfach: ")
        self.label_minor.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        self.label_miniminor = ctk.CTkLabel(self, text="...Oder erste kleine Nebenfach: ")
        self.label_miniminor.grid(row=1, column=0, sticky="n", padx=10, pady=10)

        # MENU MINORS-----------------------------------------------------------------------
        self.minor_choice_var = ctk.IntVar()
        self.minor_menu_var = ctk.StringVar(value="Wählen...")

        self.minor_list = ["Wählen..."]

        for key in self.dict_minors:
            self.minor_list.append(key)

        self.minor_menu = ctk.CTkOptionMenu(self,
                                            variable=self.minor_menu_var,
                                            values=self.minor_list,
                                            command=self.minor_clean)
        self.minor_menu.set("Wählen...")
        self.minor_menu.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # MENU MINI-MINORS----------------------------------------------------------------
        self.miniminor_choice_var = ctk.IntVar()
        self.miniminor_menu_var = ctk.StringVar(value="Wählen...")

        self.miniminor_list = ["Wählen..."]

        for key in self.dict_miniminors:
            self.miniminor_list.append(key)

        self.miniminor_menu = ctk.CTkOptionMenu(self,
                                                variable=self.miniminor_menu_var,
                                                values=self.miniminor_list,
                                                command=self.different_miniminor)
        self.miniminor_menu.set("Wählen...")
        self.miniminor_menu.grid(row=1, column=1, sticky="n", padx=10, pady=10)

        # EXTRA FRAME TO PUT CHECKBOXES AND POINTS IN
        self.extra_frame = ctk.CTkFrame(self)
        self.extra_frame.rowconfigure((0), weight=1)
        self.extra_frame.columnconfigure((0), weight=1)
        self.extra_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def gives_minormenu(self):
        return self.minor_menu_var
    def gives_miniminormenu(self):
        return self.miniminor_menu_var

    ### FUNCTIONS TO GET THE CHECKLIST OF MODULES (MINOR OR MINI-MINOR)
    def get_df_minor(self, choice):
        if choice != "Wählen..." and self.actual is not None:
            self.actual.delframe()
            url = self.dict_minors[choice]
            dframed = Minor(url, choice).dfminor()
            self.actual = CheckboxesValued(self.extra_frame, dframed, True)
        else:
            if choice in self.dict_minors:
                url = self.dict_minors[choice]
                dframed = Minor(url, choice).dfminor()
                self.actual = CheckboxesValued(self.extra_frame, dframed, True)

    def get_df_mini(self, choice, validity):
        if self.actual is not None:
            self.actual.delframe()
        if choice != "Wählen...":
            url = self.dict_miniminors[choice]
            dframed = Minor(url, choice).dfminor()
            self.actual = CheckboxesValued(self.extra_frame, dframed, validity, points=30)

    ### FUNCTION TO CLEAN UP WHEN LOADING
    def all_cleaned(self):
        if self.actual is not None:
            self.actual.delframe()
        self.minor_menu_var.set("Wählen...")
        self.miniminor_menu_var.set("Wählen...")

    ### FUNCTIONS TO RESET FOR UNCOMPATIBLES CHOICES
    # FUNCTION TO RESET MINOR WHEN MINI-MINOR CHOOSEN
    def mini_clean(self, choice, validity):
        self.get_df_mini(choice, validity)
        self.minor_menu.set("Wählen...")

    # FUNCTION TO RESET ALL MINI-MINORS WHEN MINOR CHOOSEN
    def minor_clean(self, choice):
        self.get_df_minor(choice)
        self.miniframe.reset_minimenu()
        self.miniminor_menu.set("Wählen...")

    # FUNCTION TO RESET PROGRESS BIG MINOR WHEN MINI-MINOR (OTHER FRAME VERSION)
    def progress_minor_cleaner(self):
        self.actual.delframe()

    # FUNCTION TO AVOID 2 SAME MINI-MINORS
    def different_miniminor(self, choice):
        """when mini choosen, compare with other mini, if same, frame not same mini. else do normally (miniclean or minorclean)"""
        if self.miniminor_menu_var.get() != self.miniframe.gives_minimenu().get():
            self.mini_clean(choice, True)
        else:
            self.mini_clean(choice, False)
            self.miniminor_menu.set("Wählen...")



    def minor_one_df_update(self):
        self.object_source.force_minor_update()



    ### SAVE FUNCTIONS
    def save1(self):
        if self.minor_menu.get() != "Wählen...":
            return str(self.minor_menu.get() + "\nminors_data")
        if self.miniminor_menu.get() != "Wählen...":
            return str(self.miniminor_menu.get() + "\nmini")
        else:
            return str("None\nNo Type")

    def save2(self):
        if self.actual is not None:
            return self.actual.save()
        else:
            return None

    ### LOAD FUNCTIONS
    def load_subject(self, subject, type):
        if type == "minors_data":
            self.minor_menu_var.set(subject)
            self.get_df_minor(subject)
        if type == "mini":
            self.miniminor_menu_var.set(subject)
            self.get_df_mini(subject, True)

    def load_progress(self, values):
        if self.actual is not None:
            if values is not None:
                for i, chk in enumerate(self.actual.dict_chk):
                    if values[i] != 0:
                        self.actual.dict_chk[chk].toggle()

    # EXTRA FOR RESET
    def del_error_frame(self):
        self.actual.del_error_frame1()

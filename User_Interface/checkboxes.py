import customtkinter as ctk


class CheckboxesValued(ctk.CTkFrame):
    """Create a frame for the checkboxes of each module in the subject
    Also create a Label that shows the actual points according to checked checkboxes"""
    def __init__(self, master, df, validity, points=60, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.dataframe = df
        self.points_max = points
        self.validity = validity

        # Master config
        self.master.rowconfigure((0), weight=1)
        self.master.columnconfigure((0), weight=1)

        # SELF FRAME
        self.frame_chk = ctk.CTkFrame(master)
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        self.frame_chk.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # DATA CHECKBOXES VALUES
        self.total_points = 0
        self.dict_values = {}
        self.dict_chk = {}
        self.list_values = []

        # LEISTUNGSPUNKTE / ECTS / POINTS
        self.total_points = 0

        # UNDER-SCROLLABLE-FRAME CHECKBOXES
        self.under_frame_chk = ctk.CTkScrollableFrame(self.frame_chk, width=500, height=500)
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        self.under_frame_chk.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # CHECKBOXES
        for i in range(len(self.dataframe)):
            self.dict_values["chk_value_%02d" % i] = ctk.IntVar()
            checkbox = ctk.CTkCheckBox(self.under_frame_chk, text=self.dataframe.iloc[i]['Bezeichnung'],
                                       variable=self.dict_values["chk_value_%02d" % i],
                                       onvalue=self.dataframe.iloc[i]['LP1'],
                                       offvalue=0,
                                       command=lambda: self.points())
            checkbox.grid(row=i, column=0, sticky='w', padx=5, pady=5)
            self.dict_chk["chk_%02d" % i] = checkbox

        # LEISTUNGSPUNKTE / ECTS / POINTS
        self.total_points = 0
        self.label_points = ctk.CTkLabel(self.frame_chk, text="Leistungspunkte: " + str(self.total_points))
        self.label_points.grid(row=len(self.dataframe) + 1, column=0, sticky="s", padx=10, pady=10)

        # FRAME IF MINI-MINORS ARE SAME
        self.same_miniminor_frame = ctk.CTkFrame(master)
        self.label_same_miniminor = ctk.CTkLabel(self.same_miniminor_frame,
                                                 text="Dieses Fach war schon gewählt. Bitte anderes Fach wählen.")
        self.label_same_miniminor.grid(sticky="nsew", padx=10, pady=10)

        if self.validity is False:
            self.delframe()
            self.del_error_frame1()
            self.same_miniminor_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


        if self.validity is True:
            if self.same_miniminor_frame is not None:
                self.same_miniminor_frame.grid_forget()
                self.del_error_frame1()

    def points(self):
        """Calculate the sum of the points according to checked modules to update the label showing it.
        Also gives the label a color according to if the goal has been reached, overreached or underreached"""
        self.total_points = sum(var.get() for var in self.dict_values.values())
        self.label_points.configure(text="Leistungspunkte: " + str(self.total_points))
        if self.total_points == self.points_max:
            self.label_points.configure(text_color="green")
        if self.total_points < self.points_max:
            self.label_points.configure(text_color="black")
        if self.total_points > self.points_max:
            self.label_points.configure(text_color="red")

    def delframe(self):
        self.frame_chk.grid_forget()

    def del_error_frame1(self):
        self.same_miniminor_frame.destroy()
        self.same_miniminor_frame = ctk.CTkFrame(self.master)
        self.label_same_miniminor = ctk.CTkLabel(self.same_miniminor_frame,
                                                 text="Dieses Fach war schon gewählt. Bitte anderes Fach wählen.")
        self.label_same_miniminor.grid(sticky="nsew", padx=10, pady=10)


    def save(self):
        return self.dict_values

    def dicted(self):
        return self.dict_chk

    def anframe(self):
        return self.frame_chk

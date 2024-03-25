import customtkinter as ctk
from data.MajorSubject import Major
import data.MinorSubjectList as MS
from User_Interface.frame_minor_one import CreateMinorFrame
from User_Interface.frame_minor_two import CreateMiniMinorFrame


class CreateFrameMajorSubject(ctk.CTkFrame):
    """This class manages the Major subject frame. It shows the name of the subject, the list of the courses as a
    checklist (so the user can check what has been validated).
    More Options to come:
    ---------------------------------------- checkboxes have value of ECTS, label shows the value
    ---------------------------------------- can save progress
    ...- show pflicht and wahlplicht ....HOW IS THE BETTER WAY ?
    - FIX THE 'MINOR ALREADY CHOOSEN' BUG
    - shows semester and can select it to show only this one.
    - can check Studien- and Prüfungleistung independantly, even with modules with several Studienleistung
    - can put a marker on wahlpflicht to note what is intended to do (the user choice so far)
    - possibility of notes about a module (appears in a bulle)
    OR a bulle for the leistungspunkte or something"""

    def __init__(self, master, dataframe_title, dataframe, **kwargs):
        super().__init__(master, **kwargs)
        self.dataframe = dataframe
        self.alt = dataframe_title

        self.my_font = ctk.CTkFont(family="Helvetica", size=16, underline=True)
        self.my_font1 = ctk.CTkFont(family="Helvetica", size=16)

        # INIT SELF
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0), weight=1)
        self.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # TITLE MAJOR
        self.label_major = ctk.CTkLabel(self, text=self.alt)
        self.label_major.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # DATAFRAME COLUMN INFO
        self.columns_specific = ['Bezeichnung', 'LP1', 'Empf. Beginn2', 'Bindung3']

        # UNDERFRAME CHECKBOXES
        self.under_frame_chk = ctk.CTkScrollableFrame(self, width=600, height=600)
        self.under_frame_chk.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # DATA CHECKBOXES VALUES
        self.total_major_points = 0
        self.dict_major_values = {}
        self.dict_major_chk = {}
        self.list_major_values = []

        # CHECKBOXES
        for i in range(len(self.dataframe)):
            #print(self.dataframe.iloc[i]['Bindung3'])
            if self.dataframe.iloc[i]['Bindung3'] == "Pflicht":
                self.dict_major_values["chk_major_value_%02d" % i] = ctk.IntVar()
                checkbox = ctk.CTkCheckBox(self.under_frame_chk, text="Pflicht: " + str(self.dataframe.iloc[i]['Bezeichnung']),
                                           variable=self.dict_major_values["chk_major_value_%02d" % i],
                                           onvalue=self.dataframe.iloc[i]['LP1'],
                                           offvalue=0,
                                           command=lambda: self.MajorPoints(),
                                           text_color='black',
                                           font= self.my_font1)
                checkbox.grid(row=i, column=0, sticky='w', padx=5, pady=5)
                self.dict_major_chk["chk_major_%02d" % i] = checkbox

            if self.dataframe.iloc[i]['Bindung3'] == "Wahl­pflicht" or self.dataframe.iloc[i]['Bindung3'] == "Wahl-pflicht":
                self.dict_major_values["chk_major_value_%02d" % i] = ctk.IntVar()
                checkbox = ctk.CTkCheckBox(self.under_frame_chk, text="Wahlpflicht: " + str(self.dataframe.iloc[i]['Bezeichnung']),
                                           variable=self.dict_major_values["chk_major_value_%02d" % i],
                                           onvalue=self.dataframe.iloc[i]['LP1'],
                                           offvalue=0,
                                           command=lambda: self.MajorPoints(),
                                           text_color='grey',
                                           font=self.my_font)
                checkbox.grid(row=i, column=0, sticky='w', padx=5, pady=5)
                self.dict_major_chk["chk_major_%02d" % i] = checkbox

        # LEISTUNGSPUNKTE / ECTS / POINTS
        self.total_major_points = 0
        self.label_major_points = ctk.CTkLabel(self, text="Leistungspunkte: " + str(self.total_major_points))
        self.label_major_points.grid(row=2, column=0, sticky="s", padx=10, pady=10)

    def MajorPoints(self):
        self.total_major_points = sum(var.get() for var in self.dict_major_values.values())
        self.label_major_points.configure(text="Leistungspunkte: " + str(self.total_major_points))
        if self.total_major_points == 60:
            self.label_major_points.configure(text_color="green")
        if self.total_major_points < 60:
            self.label_major_points.configure(text_color="black")
        if self.total_major_points > 60:
            self.label_major_points.configure(text_color="red")

    def save(self):
        return self.dict_major_values

    def load(self, values):
        for i, chk in enumerate(self.dict_major_chk):
            if len(self.dict_major_chk) == i:
                if values[i] != 0:
                    self.dict_major_chk[chk].toggle()

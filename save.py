
class save_progress:
    def __init__(self, kf, nbf1, nbf2):
        self.kf = kf
        self.nbf1 = nbf1
        self.nbf2 = nbf2

        self.listed1 = []
        self.listed2 = []
        self.listed3 = []

        print("Saving...")

        self.dict_1 = kf.save()
        if nbf1 is not None:
            self.dict_2 = nbf1.save2()
        if nbf2 is not None:
            self.dict_3 = nbf2.save2()

        self.save_data = open("save.txt", "w")
        self.save_data.write("Kernfach Geschichte: \n")
        self.save_data.close()

        # MAJOR
        self.save_data = open("save.txt", "a")
        for key in self.dict_1:
            state = self.dict_1[key].get()
            self.listed1.append(state)
        self.save_data.write(str(self.listed1) + "\nNebenfach 1:\n" + str(nbf1.save1()) + "\n")

        # MINOR 1
        if self.dict_2 is not None:
            for key in self.dict_2:
                state = self.dict_2[key].get()
                self.listed2.append(state)
            self.save_data.write(str(self.listed2) + "\nNebenfach 2:\n" + str(nbf2.save1()) + "\n")
        else:
            self.save_data.write("None\nNebenfach 2:\n " + str(nbf2.save1()) + "\n") # sav1 can be None+No Type

        # MINOR 2
        if self.dict_3 is not None:
            for key in self.dict_3:
                state = self.dict_3[key].get()
                self.listed3.append(state)
            self.save_data.write(str(self.listed3))
        else:
            self.save_data.write("None")

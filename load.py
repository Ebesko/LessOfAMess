import ast
import save as svg


class loading:
    def __init__(self, kf, nbf1, nbf2):
        self.kf = kf
        self.nbf1 = nbf1
        self.nbf2 = nbf2

        try:
            self.load = open("save.txt", "r")
            print("Loading...")
        except:
            print("No save file found.")

        self.content = self.load.readlines()
        self.load.close()

    def restore_all(self):
        self.restore_major()
        self.restore_minor()
        self.restore_miniminor()

    def reset_all(self):
        self.restore_major()
        self.nbf1.all_cleaned()
        self.nbf1.del_error_frame()
        self.nbf2.all_cleaned()
        svg.save_progress(self.kf, self.nbf1, self.nbf2)


    def restore_major(self):
        self.kf.load(ast.literal_eval(self.content[1]))  # list chk major value

    def restore_minor(self):
        if self.content[3] != " None": #3 is minors_data title or None, 4 is Minor Typ or No Type
            self.nbf1.load_subject(self.content[3].strip(), self.content[4].strip())
            self.nbf1.load_progress(ast.literal_eval(self.content[5]))

    def restore_miniminor(self):
        if self.content[7] != " None":
            if self.content[8] != " None":
                self.nbf2.restore_subject(self.content[7].strip())
                self.nbf2.restore_progress(ast.literal_eval(self.content[8]))
        else:
            self.nbf2.restore_subject("Wählen...")

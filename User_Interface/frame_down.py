import customtkinter as ctk

class FrameDown(ctk.CTkFrame):
    """To be at the bottom of the main window and show """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        # FRAME ITSELF
        self.frame_down = ctk.CTkFrame(master)
        self.frame_down.grid()

        self.label = ctk.CTkLabel(self.frame_down, text='BONJOUR')

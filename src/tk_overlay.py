from tkinter import Tk, Frame

class TkOverlay:

  def __init__(self):
    self.root = Tk()

    self.root.attributes("-alpha", 0.75)
    self.root.attributes("-fullscreen", True)
    self.root.attributes("-topmost", True)
    self.root.config(bg="black")

    self.back_frame = None
    self.front_frame = None

  def generate_frames(self):

    self.back_frame = Frame(self.root, bg="black")
    self.back_frame.pack(
      fill="both",
      expand=True
    )

    self.front_frame = Frame(self.back_frame, bg="black")
    self.front_frame.place(anchor="center", relx=0.5, rely=0.5)
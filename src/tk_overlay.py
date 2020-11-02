from os import path
from tkinter import Tk, Frame

from src import variables
from src.variables import Env

class TkOverlay:

  def __init__(self):

    print("Root > Started")

    self.root = Tk()

    self.root.attributes("-alpha", 0.75)
    self.root.attributes("-fullscreen", True)
    self.root.attributes("-topmost", True)
    self.root.config(bg="black")
    self.root.title("DW Piper")
    self.root.iconbitmap(path.join(Env.index_dir, "icon.ico"))

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

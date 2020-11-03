from os import path
from tkinter import Tk, Frame, TOP, LEFT, Label

from PIL import Image, ImageTk
import win32api

from src import variables
from src.variables import Env

class TkOverlay:

  def __init__(self):

    print("Root > Started")

    self.root = Tk()

    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
    work_area = monitor_info["Work"]
    width, height = 450, 250

    self.root.attributes("-topmost", True)
    self.root.config(highlightthickness=1, highlightbackground="white")
    self.root.minsize(width, height)
    self.root.title("DW Piper")
    self.root.iconbitmap(path.join(Env.index_dir, "images/icon.ico"))
    self.root.geometry('%dx%d+%d+%d' % (
      width, height,
      (work_area[2] / 2) - ((width + 13) / 2),
      (work_area[3] / 2) - ((height + 36) / 2)
    ))

    self.back_frame = None
    self.front_frame = None

    self.title_frame = None
    self.title_icon = Image.open(path.join(Env.index_dir, "images/icon.ico")).resize((64, 64), Image.LANCZOS)
    self.title_icon_photoimage = ImageTk.PhotoImage(self.title_icon)
    self.title_icon_label = None
    self.title_label = None

  def generate_frames(self):

    self.back_frame = Frame(self.root, bg="#212121")
    self.back_frame.pack(
      fill="both",
      expand=True
    )

    self.front_frame = Frame(self.back_frame, bg="#212121")
    self.front_frame.place(anchor="center", relx=0.5, rely=0.5)

  def generate_title(self):

    if not self.front_frame:
      return

    self.title_frame = Frame(
      self.front_frame,
      bg="#212121"
    )
    self.title_frame.pack(side=TOP)

    self.title_icon_label = Label(
      self.title_frame,
      image=self.title_icon_photoimage,
      bg="#212121",
      borderwidth=0
    )
    self.title_icon_label.pack(side=LEFT)

    self.title_label = Label(
      self.title_frame,
      text="DW Piper",
      font=("Courier", 16),
      pady=10,
      bg="#212121",
      fg="white"
    )
    self.title_label.pack(side=LEFT, padx=(20, 0))
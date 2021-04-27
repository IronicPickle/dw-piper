from os import path
from tkinter import Tk, Frame, Label, LEFT, TOP

from PIL import Image, ImageTk

from src.extract import Extract
from src.capture import Capture
from src.align import Align
from src.map import Map

from src.menus.snap_menu import SnapMenu

from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env

class MainMenu(TkOverlay):

  def __init__(self, root = None):

    super().__init__(root)

    self.generate_frames()
    self.generate_header()
    self.generate_title("Choose an Option")

    self.resize(450, 450)

    self.root.bind("<Key>", self.key_press)


    self.generate_sub_title(self.front_frame, "Image Source")
    
    self.button_frame_top = Label(self.front_frame, bg="#212121")
    self.button_frame_top.pack(side=TOP)
    
    self.generate_button("Extract", self.start_extract, self.button_frame_top)
    self.generate_button("Capture", self.start_capture, self.button_frame_top)

    self.generate_divider(self.front_frame)

    
    self.generate_sub_title(self.front_frame, "Alignment and Mapping")

    self.button_frame_center = Label(self.front_frame, bg="#212121")
    self.button_frame_center.pack(side=TOP)

    self.generate_button("Snap", self.start_snap, self.button_frame_center)
    self.generate_button("Map", self.start_map, self.button_frame_center)
    
    self.generate_divider(self.front_frame)


    self.generate_sub_title(self.front_frame, "Other")
    
    self.button_frame_bottom = Label(self.front_frame, bg="#212121")
    self.button_frame_bottom.pack(side=TOP)

    self.generate_button("Auto-Align", self.start_align, self.button_frame_bottom)
    self.generate_button("Cancel", self.root.destroy, self.button_frame_bottom)

    self.generate_divider(self.front_frame)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def generate_sub_title(self, frame, text = "Unnamed"):
    self.button_title_label = Label(
      frame, text=text,
      font=("Courier", 12),
      bg="#212121", fg="#bbb"
    )
    self.button_title_label.pack(side=TOP, pady=(20, 5))
  
  def generate_divider(self, frame):
    self.button_divider1_frame = Frame(
      frame, bg="white",
      width=250, height=1
    )
    self.button_divider1_frame.pack(side=TOP, pady=(5, 5))

  def start_extract(self):
    self.root.destroy()
    Extract()

  def start_capture(self):
    self.back_frame.destroy()
    Capture(self.root)
    
  def start_align(self):
    self.back_frame.destroy()
    Align(self.root)

  def start_snap(self):
    self.back_frame.destroy()
    SnapMenu(self.root)

  def start_map(self):
    self.back_frame.destroy()
    Map(self.root)

  def key_press(self, event):
    key_events = {
      27: self.root.destroy,
      85: self.start_extract,
      67: self.start_capture,
      65: self.start_align,
      77: self.start_map
    }
    try:
      key_events[event.keycode]()
    except:
      pass

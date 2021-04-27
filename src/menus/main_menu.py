from os import path
from tkinter import Frame, Label, Button, LEFT, TOP

from PIL import Image, ImageTk

from src.upload import Upload
from src.capture import Capture
from src.align import Align
from src.map import Map

from src.menus.snap_menu import SnapMenu

from src.lib.variables import Env

class MainMenu:

  def __init__(self, tk_overlay):
    print("Main Menu > Started")

    tk_overlay.generate_frames()
    tk_overlay.generate_title()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.attributes("-alpha", 1)

    self.root.bind("<Key>", self.key_press)

    self.button_label = Label(
      self.front_frame,
      text="Choose an Option",
      font=("Courier", 16),
      pady=10,
      bg="#212121",
      fg="white"
    )
    self.button_label.pack(side=TOP)

    self.divider_frame = Frame(
      self.front_frame,
      bg="white",
      width=120,
      height=1
    )
    self.divider_frame.pack(side=TOP, pady=(0, 10))

    self.button_frame_top = Label(
      self.front_frame,
      bg="#212121"
    )
    self.button_frame_top.pack(side=TOP)

    self.generate_button("Upload", self.start_upload, self.button_frame_top)
    self.generate_button("Capture", self.start_capture, self.button_frame_top)
    self.generate_button("Align", self.start_align, self.button_frame_top)

    self.button_frame_bottom = Label(
      self.front_frame,
      bg="#212121"
    )
    self.button_frame_bottom.pack(side=TOP)

    self.generate_button("Snap", self.start_snap, self.button_frame_bottom)
    self.generate_button("Map", self.start_map, self.button_frame_bottom)
    self.generate_button("Cancel", self.destroy_root, self.button_frame_bottom)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def generate_button(self, name, command, frame):
    Button(
      frame,
      text=name,
      font=("Courier", 12),
      command=command,
      cursor="hand2",
      bd=0,
      bg="#212121",
      fg="white"
    ).pack(side=LEFT, padx=10)

  def destroy_root(self):
    self.destroy_back_frame()
    self.root.destroy()
    print("Root > Destroyed")

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Main Menu > Destroyed")

  def start_upload(self):
    self.root.destroy()
    Upload()

  def start_capture(self):
    self.destroy_back_frame()
    Capture(self.tk_overlay)
    
  def start_align(self):
    self.destroy_back_frame()
    Align(self.tk_overlay)

  def start_snap(self):
    self.destroy_back_frame()
    SnapMenu(self.tk_overlay)

  def start_map(self):
    self.destroy_back_frame()
    Map(self.tk_overlay)

  def key_press(self, event):
    key_events = {
      27: self.destroy_root,
      85: self.start_upload,
      67: self.start_capture,
      65: self.start_align,
      77: self.start_map
    }
    try:
      key_events[event.keycode]()
    except:
      pass

from os import path
from pathlib import Path
from tkinter import Frame, Label, Button, TOP, LEFT

from win10toast import ToastNotifier

from src import align, variables
from src.align import Align
from src.variables import Env

class AlignMenu:

  def __init__(self, tk_overlay):
    print("Align Menu > Started")

    tk_overlay.generate_frames()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    if not Path(path.join(Env.appdata_path, "images/initial.png")).exists():
      self.destroy_root()
      print("No initial image found")
      ToastNotifier().show_toast("Couldn't find initial image",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=5,
        threaded=True
      )
      exit()
    if not Path(path.join(Env.appdata_path, "state.json")).exists():
      self.destroy_root()
      print("No state file found")
      ToastNotifier().show_toast("Couldn't find state file",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=5,
        threaded=True
      )
      exit()

    self.root.bind("<Key>", self.key_press)

    self.button_label = Label(
      self.front_frame,
      text="Choose an Option",
      font=("Courier", 16),
      pady=10,
      bg="black",
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

    self.button_frame = Label(
      self.front_frame,
      bg="black"
    )
    self.button_frame.pack(side=TOP)

    self.generate_buttons("Clean", self.start_clean)
    self.generate_buttons("Drainage", self.start_drainage)
    self.generate_buttons("Cancel", self.destroy_root)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def generate_buttons(self, name, command):
    Button(
      self.button_frame,
      text=name,
      font=("Courier", 12),
      command=command,
      cursor="hand2",
      bd=0,
      bg="black",
      fg="white"
    ).pack(side=LEFT, padx=10)

  def destroy_root(self):
    self.destroy_back_frame()
    self.root.destroy()
    print("Root > Destroyed")

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Align Menu > Destroyed")

  def start_clean(self):
    self.destroy_back_frame()
    Align(self.tk_overlay, "clean")

  def start_drainage(self):
    self.destroy_back_frame()
    Align(self.tk_overlay, "drainage")

  def key_press(self, event):
    key_events = {
      27: self.destroy_root,
      67: self.start_clean,
      68: self.start_drainage
    }
    try:
      key_events[event.keycode]()
    except:
      pass
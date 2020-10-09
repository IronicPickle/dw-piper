from os import path
from pathlib import Path
from tkinter import Frame, Label, Button, TOP, LEFT

from win10toast import ToastNotifier

from vars import Env

class AlignMenu:
  key_events = {
    27: destroy_root,
    67: start_clean,
    68: start_drainage
  }

  def __init(self, TkOverlay):
    print("Starting main menu")

    if not Path(path.join(Env.appdata_path, "images/initial.png")).exists():
      self.destroy_root()
      print("No initial image found")
      return ToastNotifier().show_toast("Couldn't find initial image",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=10,
        threaded=True
      )
    if not Path(path.join(Env.appdata_path, "state.json")).exists():
      self.destroy_root()
      print("No state file found")
      return ToastNotifier().show_toast("Couldn't find state file",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=10,
        threaded=True
      )

    TkOverlay.generate_buttons()

    self.tk_overlay = TkOverlay
    self.root = TkOverlay.root
    self.back_frame = TkOverlay.back_frame
    self.front_frame = TkOverlay.front_frame

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

    self.button_frame = Label(
      self.front_frame,
      bg="black",
      fg="white"
    )
    self.button_frame.pack(side=TOP)

    self.button_label = Label(
      self.front_frame,
      text="Choose an Option",
      font=("Courier", 16),
      pady=10,
      bg="black",
      fg="white"
    )
    self.button_label.pack(side=TOP)

    button_frame = Label(
      self.front_frame,
      bg="black",
      fg="white"
    )
    self.button_frame.pack(side=TOP)

    self.generate_buttons("Clean", self.start_clean)
    self.generate_buttons("Drainage", self.start_drainage)
    self.generate_buttons("Cancel", self.destroy_root)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()
    print("Root > Destroyed")

  def generate_buttons(self, name, command):
    self.capture_button = Button(
      self.button_frame,
      text=name,
      font=("Courier", 12),
      command=command,
      cursor="hand2",
      bd=0,
      bg="black",
      fg="white"
    )
    self.capture_button.pack(side=LEFT, padx=10)

  def destroy_root(self):
    self.root.destroy()

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Main Menu > Destroyed")

  def start_clean(self):
    self.destroy_back_frame()
    align_main(root, "clean")

  def start_drainage(self):
    self.destroy_back_frame()
    align_main(root, "drainage")

  def key_press(self, event):
    try:
      self.key_events[event.keycode]()
    except:
      pass

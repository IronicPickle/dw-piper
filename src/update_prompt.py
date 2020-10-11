from os import path
from tkinter import Frame, Label, Button, TOP, LEFT

import win32api

from src import variables
from src.variables import Env

class UpdatePrompt:

  def __init__(self, tk_overlay, latest_version, download_version):

    print("Update Prompt > Started")

    self.download_version = download_version
    self.latest_version = latest_version["version"]

    tk_overlay.generate_frames()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.bind("<Key>", self.key_press)

    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
    work_area = monitor_info["Work"]

    self.root.attributes("-fullscreen", False)
    self.root.attributes("-alpha", 0.9)
    self.root.config(bg="black", highlightthickness=1, highlightbackground="white")
    self.root.minsize(450, 200)
    self.root.geometry('%dx%d+%d+%d' % (450, 200, work_area[2] - 463, work_area[3] - 236))
    self.root.title("DW Piper")
    self.root.iconbitmap(path.join(Env.index_dir, "icon.ico"))

    self.title_label = Label(
      self.front_frame,
      text="DW Piper",
      font=("Courier", 16, "underline"),
      bg="black",
      fg="white"
    )
    self.title_label.pack(side=TOP)

    self.version_label = Label(
      self.front_frame,
      text=f"Version: {self.latest_version}",
      font=("Courier", 12),
      bg="black",
      fg="white"
    )
    self.version_label.pack(side=TOP, pady=(0, 5))

    self.button_label = Label(
      self.front_frame,
      text=f"An update is available\nWould you like to install it?",
      font=("Courier", 16),
      bg="black",
      fg="white"
    )
    self.button_label.pack(side=TOP, pady=10)

    self.button_frame = Label(
      self.front_frame,
      bg="black",
      fg="white"
    )
    self.button_frame.pack(side=TOP)

    self.generate_buttons("Update", self.update)
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
    self.back_frame.destroy(self)
    print("Update Prompt > Destroyed")

  def update(self):
    self.button_label.config(text="Downloading update...")
    self.button_frame.destroy()
    self.button_label.update()
    self.download_version(self.latest_version, self.on_download_finish)

  def on_download_finish(self):
    self.destroy_root()

  def key_press(self, event):
    key_events = {
      27: self.destroy_root
    }
    try:
      key_events[event.keycode]()
    except:
      pass

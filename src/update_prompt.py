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
    tk_overlay.generate_title()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.attributes("-alpha", 1)

    self.root.bind("<Key>", self.key_press)

    width, height = self.root.winfo_width(), self.root.winfo_height()
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
    work_area = monitor_info["Work"]

    self.root.geometry('%dx%d+%d+%d' % (width, height, work_area[2] - (width + 13), work_area[3] - (height + 36)))

    self.version_label = Label(
      self.front_frame,
      text=f"Version: {self.latest_version}",
      font=("Courier", 12),
      bg="#212121",
      fg="white"
    )
    self.version_label.pack(side=TOP, pady=(0, 5))

    self.button_label = Label(
      self.front_frame,
      text=f"An update is available\nWould you like to install it?",
      font=("Courier", 16),
      bg="#212121",
      fg="white"
    )
    self.button_label.pack(side=TOP, pady=10)

    self.divider_frame = Frame(
      self.front_frame,
      bg="white",
      width=120,
      height=1
    )
    self.divider_frame.pack(side=TOP, pady=(0, 10))

    self.button_frame = Label(
      self.front_frame,
      bg="#212121"
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
      bg="#212121",
      fg="white"
    ).pack(side=LEFT, padx=10)

  def destroy_root(self):
    self.destroy_back_frame()
    self.root.destroy()
    print("Root > Destroyed")

  def destroy_back_frame(self):
    self.back_frame.destroy()
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

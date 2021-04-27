from os import path
from tkinter import Frame, Label, Button, Scrollbar, Listbox, TOP, BOTTOM, LEFT, RIGHT, Y, X, END, HORIZONTAL, FLAT

import win32api

from src.lib.variables import Env

class UpdatePrompt:

  def __init__(self, tk_overlay, latest_version, changelog, download_version):

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

    width, height = 450, 400
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
    work_area = monitor_info["Work"]

    self.root.minsize(width, height)
    self.root.geometry('%dx%d+%d+%d' % (width, height, work_area[2] - (width + 13), work_area[3] - (height + 36)))

    self.version_label = Label(
      self.front_frame,
      text=f"Version: {self.latest_version}",
      font=("Courier", 12),
      bg="#212121",
      fg="white"
    )
    self.version_label.pack(side=TOP)

    self.date_label = Label(
      self.front_frame,
      text=changelog["date"],
      font=("Courier", 8),
      bg="#212121",
      fg="white"
    )
    self.date_label.pack(side=TOP, pady=(0, 10))

    self.changelog_frame = Frame(
      self.front_frame,
      bg="#212121"
    )
    self.changelog_frame.pack(side=TOP, pady=(0, 5))

    self.changelog_scrollbar_x = Scrollbar(self.changelog_frame, orient=HORIZONTAL)
    self.changelog_scrollbar_x.pack(side=BOTTOM, fill=X)
    self.changelog_scrollbar_y = Scrollbar(self.changelog_frame)
    self.changelog_scrollbar_y.pack(side=RIGHT, fill=Y)

    self.changelog_listbox = Listbox(
      self.changelog_frame,
      font=("Courier", 8),
      bg="#212121",
      fg="white",
      width=50,
      height=8,
      xscrollcommand=self.changelog_scrollbar_x.set,
      yscrollcommand=self.changelog_scrollbar_y.set,
      relief=FLAT
    )
    self.changelog_listbox.pack(side=TOP)

    self.changelog_scrollbar_x.config(command=self.changelog_listbox.xview)
    self.changelog_scrollbar_y.config(command=self.changelog_listbox.yview)

    for change in changelog["changes"]:
      self.changelog_listbox.insert(END, f"{change}\n")

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

    self.generate_button("Update", self.update)
    self.generate_button("Cancel", self.destroy_root)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def generate_button(self, name, command):
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

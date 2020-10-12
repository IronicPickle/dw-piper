from tkinter import Frame, Label, Button, LEFT, TOP

from src import upload, capture, align_menu
from src.upload import Upload
from src.capture import Capture
from src.align_menu import AlignMenu

class MainMenu:

  def __init__(self, tk_overlay):
    print("Main Menu > Started")

    tk_overlay.generate_frames()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

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

    self.generate_buttons("Upload", self.start_upload)
    self.generate_buttons("Capture", self.start_capture)
    self.generate_buttons("Align", self.start_align)
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
    print("Main Menu > Destroyed")

  def start_upload(self):
    self.root.destroy()
    Upload()

  def start_capture(self):
    self.destroy_back_frame()
    Capture(self.tk_overlay)

  def start_align(self):
    self.destroy_back_frame()
    AlignMenu(self.tk_overlay)

  def key_press(self, event):
    key_events = {
      27: self.destroy_root,
      85: self.start_upload,
      67: self.start_capture,
      65: self.start_align
    }
    try:
      key_events[event.keycode]()
    except:
      pass

from tkinter import Frame, Label, Button, LEFT, TOP

from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env

class ConfirmMenu(TkOverlay):

  def __init__(self, root = None, title = "Are you Sure?"):

    super().__init__(root)

    self.cancelled = False

    self.generate_frames()
    self.generate_header()
    self.generate_title(title)

    self.root.bind("<Key>", self.key_press)

    self.button_frame = Label(
      self.front_frame,
      bg=Env.bg
    )
    self.button_frame.pack(side=TOP)

    self.continue_button = self.generate_button("Continue", self.submit, self.button_frame)
    self.cancel_button = self.generate_button("Cancel", self.cancel, self.button_frame)

    self.root.after(1, self.cancel_button.focus)

    self.root.mainloop()

  def cancel(self):
    self.cancelled = True
    self.root.destroy()

  def submit(self):
    self.root.destroy()

  def key_press(self, event):
    key_events = {
      27: self.cancel,
      13: self.submit
    }
    try:
      key_events[event.keycode]()
    except:
      pass

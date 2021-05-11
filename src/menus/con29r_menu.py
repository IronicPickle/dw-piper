from tkinter import Frame, Label, Button, Entry, LEFT, TOP, CENTER, StringVar, FLAT

from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env

class Con29RMenu(TkOverlay):

  def __init__(self, root = None, default_road=""):

    super().__init__(root)

    self.cancelled = False
    self.default_road = StringVar()
    self.road1 = StringVar()
    self.road2 = StringVar()
    self.road3 = StringVar()

    self.default_road.set(default_road)

    self.generate_frames()
    self.generate_header()
    self.generate_title("Roads to Search")

    self.resize(450, 400)

    self.root.bind("<Key>", self.key_press)

    self.entry_0 = self.generate_entries(self.default_road, "readonly")
    self.entry_1 = self.generate_entries(self.road1)
    self.entry_2 =self.generate_entries(self.road2)
    self.entry_3 =self.generate_entries(self.road3)

    self.button_frame = Label(
      self.front_frame,
      bg=Env.bg
    )
    self.button_frame.pack(side=TOP)

    self.generate_button("Submit", self.submit, self.button_frame)
    self.generate_button("Cancel", self.cancel, self.button_frame)

    self.root.after(1, self.entry_2.focus)

    self.root.mainloop()

  def generate_entries(self, road_variable, state="normal"):
    entry = Entry(
      self.front_frame,
      font=("Courier", 12),
      textvariable=road_variable,
      bg=Env.bg,
      fg=Env.fg if state == "normal" else "black",
      insertbackground="white",
      justify=CENTER,
      highlightthickness=1,
      relief=FLAT,
      width=30,
      state=state
    )
    entry.pack(side=TOP, pady=10)
    return entry

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

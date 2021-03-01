from tkinter import Frame, Label, Button, Entry, LEFT, TOP, CENTER, StringVar, FLAT

from src import state_manager

class Con29RMenu:

  def __init__(self, tk_overlay, road1=""):
    print("Options Menu > Started")

    self.cancelled = False
    self.road1 = StringVar()
    self.road2 = StringVar()
    self.road3 = StringVar()

    self.road1.set(road1)

    tk_overlay.generate_frames()
    tk_overlay.generate_title()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.attributes("-fullscreen", False)
    self.root.attributes("-alpha", 1)
    self.root.minsize(450, 350)

    self.root.bind("<Key>", self.key_press)

    self.entry_label = Label(
      self.front_frame,
      text="Roads to Search",
      font=("Courier", 16),
      pady=10,
      bg="#212121",
      fg="white"
    )
    self.entry_label.pack(side=TOP)

    self.divider_frame = Frame(
      self.front_frame,
      bg="white",
      width=120,
      height=1
    )
    self.divider_frame.pack(side=TOP, pady=(0, 10))

    self.entry_1 = self.generate_entries(self.road1)
    self.entry_2 =self.generate_entries(self.road2)
    self.entry_3 =self.generate_entries(self.road3)

    self.button_frame = Label(
      self.front_frame,
      bg="#212121"
    )
    self.button_frame.pack(side=TOP)

    self.generate_button("Submit", self.submit)
    self.generate_button("Cancel", self.cancel)

    self.root.after(1, self.entry_2.focus)

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

  def generate_entries(self, road_variable):
    entry = Entry(
      self.front_frame,
      font=("Courier", 12),
      textvariable=road_variable,
      bg="#212121",
      fg="white",
      insertbackground="white",
      justify=CENTER,
      highlightthickness=1,
      relief=FLAT,
      width=30
    )
    entry.pack(side=TOP, pady=10)
    return entry

  def cancel(self):
    self.cancelled = True
    self.destroy_root()

  def destroy_root(self):
    self.destroy_back_frame()
    self.root.destroy()
    print("Root > Destroyed")

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Options Menu > Destroyed")

  def submit(self):
    self.root.destroy()

  def key_press(self, event):
    key_events = {
      27: self.destroy_root,
      13: self.submit
    }
    try:
      key_events[event.keycode]()
    except:
      pass

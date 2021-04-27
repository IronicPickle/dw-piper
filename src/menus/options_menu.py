from os import path
from tkinter import Frame, Label, Button, Entry, LEFT, TOP, CENTER, StringVar, FLAT

from PIL import Image, ImageTk

from src.lib import state_manager
from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env

class OptionsMenu(TkOverlay):

  def __init__(self, root = None, initial_img_pil = None):

    super().__init__(root)

    self.cancelled = False

    self.reference = StringVar()
    state = state_manager.get()
    state_manager.update(state, { "reference": "" })

    self.generate_frames()
    self.generate_header()
    self.generate_title("Current Image")

    self.resize(450, 625)

    self.root.bind("<Key>", self.key_press)

    self.initial_img_pil = initial_img_pil
    if self.initial_img_pil is None:
      self.initial_img_pil = Image.open(
        path.join(Env.appdata_path, "images/initial.png")
      )

    self.initial_img_tk = ImageTk.PhotoImage(
      self.initial_img_pil.resize((300, 300), Image.BILINEAR)
    )

    self.image_frame = Frame(
      self.front_frame, highlightthickness=1, highlightcolor="#fff"
    )
    self.image_frame.pack(side=TOP, pady=(10))

    self.image_label = Label(
      self.image_frame,
      image=self.initial_img_tk,
      bg="#212121",
      borderwidth=0
    )
    self.image_label.image = self.initial_img_tk
    self.image_label.pack()

    self.generate_title("Input a Reference")


    self.reference_entry = Entry(
      self.front_frame,
      font=("Courier", 12),
      textvariable=self.reference,
      bg="#212121",
      fg="white",
      insertbackground="white",
      justify=CENTER,
      highlightthickness=1,
      relief=FLAT
    )
    self.reference_entry.pack(side=TOP, pady=10)

    self.button_frame = Label(
      self.front_frame,
      bg="#212121"
    )
    self.button_frame.pack(side=TOP)

    self.generate_button("Submit", self.submit, self.button_frame)
    self.generate_button("Cancel", self.cancel, self.button_frame)

    self.root.after(1, self.reference_entry.focus)

    self.root.mainloop()

  def cancel(self):
    self.cancelled = True
    self.root.destroy()

  def submit(self):
    save_ref(self.reference.get())
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

def save_ref(ref):
  state = state_manager.get()
  state_manager.update(state, {
    "reference": ref
  })
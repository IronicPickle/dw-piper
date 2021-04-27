from tkinter import Frame, Label, Button, Entry, LEFT, TOP, CENTER, StringVar, FLAT

from src.lib import state_manager

class OptionsMenu:

  def __init__(self, tk_overlay):
    print("Options Menu > Started")

    self.cancelled = False

    self.reference = StringVar()
    state = state_manager.get()
    state_manager.update(state, { "reference": "" })

    tk_overlay.generate_frames()
    tk_overlay.generate_title()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.attributes("-fullscreen", False)
    self.root.attributes("-alpha", 1)

    self.root.bind("<Key>", self.key_press)

    self.button_label = Label(
      self.front_frame,
      text="Input your Reference",
      font=("Courier", 16),
      pady=10,
      bg="#212121",
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

    self.generate_button("Submit", self.submit)
    self.generate_button("Cancel", self.cancel)

    self.root.after(1, self.reference_entry.focus)

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
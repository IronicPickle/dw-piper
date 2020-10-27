from tkinter import Frame, Label, Button, Entry, LEFT, TOP, CENTER, StringVar, FLAT

from src import state_manager

class OptionsMenu:

  def __init__(self, tk_overlay):
    print("Options Menu > Started")

    self.reference = StringVar()
    state = state_manager.get()
    state_manager.update(state, { "reference": "" })

    tk_overlay.generate_frames()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.bind("<Key>", self.key_press)

    self.button_label = Label(
      self.front_frame,
      text="Input your Reference",
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

    self.reference_entry = Entry(
      self.front_frame,
      font=("Courier", 12),
      textvariable=self.reference,
      bg="black",
      fg="white",
      insertbackground="white",
      justify=CENTER,
      highlightthickness=1,
      relief=FLAT,
    )
    self.reference_entry.pack(side=TOP, pady=10)

    self.button_frame = Label(
      self.front_frame,
      bg="black"
    )
    self.button_frame.pack(side=TOP)

    self.generate_buttons("Submit", self.submit)
    self.generate_buttons("Cancel", self.destroy_root)

    self.root.after(1, self.reference_entry.focus)

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
    print("Options Menu > Destroyed")

  def submit(self):
    state = state_manager.get()
    state_manager.update(state, {
      "reference": self.reference.get()
    })
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

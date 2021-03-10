from tkinter import Frame, Label, Button, LEFT, TOP

class ConfirmMenu:

  def __init__(self, tk_overlay, title="Are you Sure?"):
    print("Confirm Menu > Started")

    self.cancelled = False

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
      text=title,
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

    self.button_frame = Label(
      self.front_frame,
      bg="#212121"
    )
    self.button_frame.pack(side=TOP)

    self.continue_button = self.generate_button("Continue", self.submit)
    self.cancel_button = self.generate_button("Cancel", self.cancel)

    self.root.after(1, self.cancel_button.focus)

    self.root.mainloop()

  def generate_button(self, name, command):
    button = Button(
      self.button_frame,
      text=name,
      font=("Courier", 12),
      command=command,
      cursor="hand2",
      bd=0,
      bg="#212121",
      fg="white"
    )
    button.pack(side=LEFT, padx=10)
    return button

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
      27: self.cancel,
      13: self.submit
    }
    try:
      key_events[event.keycode]()
    except:
      pass

from tkinter import Frame, Label, Button, LEFT, TOP

class MainMenu:
  key_events = {
      27: destroy_root,
      85: start_upload,
      67: start_capture,
      65: start_align
    }

  def __init(self, TkOverlay):
    print("Starting main menu")

    TkOverlay.generate_buttons()

    self.tk_overlay = TkOverlay
    self.root = TkOverlay.root
    self.back_frame = TkOverlay.back_frame
    self.front_frame = TkOverlay.front_frame

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

    self.button_frame = Label(
      self.front_frame,
      bg="black",
      fg="white"
    )
    self.button_frame.pack(side=TOP)

    self.generate_buttons("Upload", self.start_upload)
    self.generate_buttons("Capture", self.start_capture)
    self.generate_buttons("Align", self.start_align)
    self.generate_buttons("Cancel", self.destroy_root)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()
    print("Root > Destroyed")

  def generate_buttons(self, name, command):
    self.capture_button = Button(
      self.button_frame,
      text=name,
      font=("Courier", 12),
      command=command,
      cursor="hand2",
      bd=0,
      bg="black",
      fg="white"
    )
    self.capture_button.pack(side=LEFT, padx=10)

  def destroy_root(self):
    self.root.destroy()

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Main Menu > Destroyed")

  def start_upload(self):
    self.destroy_back_frame()
    self.root.destroy()
    upload_main()

  def start_capture(self):
    self.destroy_back_frame()
    capture_main(self.tk_overlay)

  def start_align(self):
    self.destroy_back_frame()
    align_menu_main(self.tk_overlay)

  def key_press(self, event):
    try:
      self.key_events[event.keycode]()
    except:
      pass

from os import path
from pathlib import Path
from tkinter import Frame, Label, Button, OptionMenu, TOP, LEFT, StringVar, FLAT

from win10toast import ToastNotifier

from src import align, variables, state_manager
from src.snap import Snap
from src.variables import Env, WATER_COMPANIES

class SnapMenu:

  def __init__(self, tk_overlay):
    print("Snap Menu > Started")

    self.water_company = StringVar()
    state = state_manager.get()
    if "water_company" in state:
      self.water_company.set(state["water_company"])
    else:
      self.water_company.set("United Utilities")

    tk_overlay.generate_frames()
    tk_overlay.generate_title()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame
    
    self.root.attributes("-alpha", 1)
    self.root.minsize(450, 300)

    if not Path(path.join(Env.appdata_path, "images/initial.png")).exists():
      self.destroy_root()
      print("No initial image found")
      ToastNotifier().show_toast("Couldn't find initial image",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=5,
        threaded=True
      )
      exit()
    if not Path(path.join(Env.appdata_path, "state.json")).exists():
      self.destroy_root()
      print("No state file found")
      ToastNotifier().show_toast("Couldn't find state file",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=5,
        threaded=True
      )
      exit()

    self.root.bind("<Key>", self.key_press)

    self.water_company_label = Label(
      self.front_frame,
      text="Select a Water Company",
      font=("Courier", 16),
      pady=10,
      bg="#212121",
      fg="white"
    )
    self.water_company_label.pack(side=TOP)

    self.divider_frame = Frame(
      self.front_frame,
      bg="white",
      width=120,
      height=1
    )
    self.divider_frame.pack(side=TOP, pady=(0, 10))

    self.water_company_dropdown = OptionMenu(
      self.front_frame,
      self.water_company,
      *WATER_COMPANIES.keys()
    )
    self.water_company_dropdown.config(
      font=("Courier", 12),
      bg="#212121",
      fg="white",
      highlightthickness=0,
      relief=FLAT
    )
    self.water_company_dropdown.pack(side=TOP, pady=(0, 20))

    self.button_label = Label(
      self.front_frame,
      text="Choose an Option",
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

    self.generate_button("Clean", self.start_clean)
    self.generate_button("Drainage", self.start_drainage)
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
    state = state_manager.get()
    state_manager.update(state, { "water_company": self.water_company.get() })
    self.back_frame.destroy()
    print("Snap Menu > Destroyed")

  def start_clean(self):
    self.destroy_back_frame()
    Snap(self.tk_overlay, "clean", self.water_company.get())

  def start_drainage(self):
    self.destroy_back_frame()
    Snap(self.tk_overlay, "drainage", self.water_company.get())

  def key_press(self, event):
    key_events = {
      27: self.destroy_root,
      67: self.start_clean,
      68: self.start_drainage
    }
    try:
      key_events[event.keycode]()
    except:
      pass

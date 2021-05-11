from os import path
from pathlib import Path
from tkinter import Frame, Label, Button, OptionMenu, TOP, LEFT, StringVar, FLAT

from src.generate import Generate

from src.lib import state_manager
from src.lib.tk_overlay import TkOverlay
from src.lib.utils import Utils
from src.lib.variables import Env, WATER_COMPANIES

class GenerateMenu(TkOverlay):

  def __init__(self, root = None):

    super().__init__(root)

    self.water_company = StringVar()
    state = state_manager.get()
    if "water_company" in state:
      self.water_company.set(state["water_company"])
    else:
      self.water_company.set("United Utilities")

    self.register_key_event(67, self.start_clean)
    self.register_key_event(68, self.start_drainage)

    self.generate_frames()
    self.generate_header()
    self.generate_title("Select a Water Company")
    
    self.resize(450, 300)

    if not Path(path.join(Env.appdata_path, "images/initial.png")).exists():
      self.root.destroy()
      print("No initial image found")
      Utils.send_toast(
        "Couldn't find initial image",
        "You must take a screenshot first",
        duration = 5
      )
      exit()
    if not Path(path.join(Env.appdata_path, "state.json")).exists():
      self.root.destroy()
      print("No state file found")
      Utils.send_toast("Couldn't find state file",
        "You must take a screenshot first",
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=5
      )
      exit()

    self.root.bind("<Key>", self.key_press)

    self.water_company_dropdown = OptionMenu(
      self.front_frame,
      self.water_company,
      *WATER_COMPANIES.keys()
    )
    self.water_company_dropdown.config(
      font=("Courier", 12),
      bg=Env.bg,
      fg=Env.fg,
      highlightthickness=0,
      relief=FLAT
    )
    self.water_company_dropdown.pack(side=TOP, pady=(0, 20))

    self.button_label = Label(
      self.front_frame,
      text="Choose an Option",
      font=("Courier", 16),
      pady=10,
      bg=Env.bg,
      fg=Env.fg
    )
    self.button_label.pack(side=TOP)

    self.divider_frame = Frame(
      self.front_frame,
      bg=Env.div,
      width=120,
      height=1
    )
    self.divider_frame.pack(side=TOP, pady=(0, 10))

    self.button_frame = Label(
      self.front_frame,
      bg=Env.bg
    )
    self.button_frame.pack(side=TOP)

    self.generate_button("Clean", self.start_clean, self.button_frame)
    self.generate_button("Drainage", self.start_drainage, self.button_frame)
    self.generate_button("Cancel", self.root.destroy, self.button_frame)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()


  def on_back_destroy(self):
    state_manager.update({ "water_company": self.water_company.get() })

  def start_clean(self):
    self.back_frame.destroy()
    Generate(self.root, "clean", self.water_company.get())

  def start_drainage(self):
    self.back_frame.destroy()
    Generate(self.root, "drainage", self.water_company.get())

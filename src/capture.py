from os import path
from pathlib import Path
from tkinter import Frame, Label, TOP

import pyautogui

from src.menus.options_menu import OptionsMenu

from src.lib.utils import Utils
from src.lib import state_manager
from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env

class Capture(TkOverlay):
  mouse_start = {"x": 0, "y": 0}

  def __init__(self, root = None):

    super().__init__(root)

    self.img_path = path.join(Env.appdata_path, f"images/initial.png")

    self.generate_frames()

    self.root.attributes("-fullscreen", True)
    self.root.attributes("-alpha", 0.5)

    self.root.bind("<Key>", self.key_press)

    self.back_frame.bind("<Button-1>", self.mouse_1_down)
    self.back_frame.bind("<B1-Motion>", self.mouse_1_move)
    self.back_frame.bind("<ButtonRelease-1>", self.mouse_1_up)
    self.back_frame.bind("<Key>", self.key_press)

    self.back_frame.config(cursor="tcross")

    self.selection_frame = Frame(
      self.back_frame,
      bg="white",
      borderwidth=2
    )

    self.top_label = Label(
      self.back_frame,
      text="Click and drag to select an area\nor press ESC to cancel",
      font=("Courier", 16),
      bg="black",
      fg="white",
      pady=10, padx=10
    )
    self.top_label.pack(side=TOP, pady=(100, 0))

    self.coords_label = Label(
      self.selection_frame,
      text="0 x 0",
      font=("Courier", 16),
      bg="#212121",
      fg="white",
      pady=0,
      padx=5
    )
    self.coords_label.place(anchor="center")

    self.back_frame.after(1, self.back_frame.focus_force)

  def mouse_1_down(self, event):
    self.selection_frame.pack()
    self.mouse_start["x"], self.mouse_start["y"] = event.x, event.y
    self.selection_frame.place(x=event.x, y=event.y)

  def mouse_1_move(self, event):
    width = event.x - self.mouse_start["x"]
    height = event.y - self.mouse_start["y"]
    box_size = 0

    if abs(width) > abs(height):
      box_size = width if height > 0 else -width
    if abs(height) > abs(width):
      box_size = height if width > 0 else -height

    box_x = self.mouse_start["x"]
    box_y = self.mouse_start["y"]

    if event.x - self.mouse_start["x"] < 0:
      box_x -= abs(box_size)
    if event.y - self.mouse_start["y"] < 0:
      box_y -= abs(box_size)

    box_size = abs(box_size)

    if box_x < 0:
      box_size = self.selection_frame.winfo_width()
      box_x = 0
      box_y = self.selection_frame.winfo_y()
    elif box_x + box_size > Env.res_x:
      box_size = self.selection_frame.winfo_width()
      box_x = Env.res_x - box_size
      box_y = self.selection_frame.winfo_y()

    elif box_y < 0:
      box_size = self.selection_frame.winfo_width()
      box_y = 0
      box_x = self.selection_frame.winfo_x()
    elif box_y + box_size > Env.res_y:
      box_size = self.selection_frame.winfo_width()
      box_y = Env.res_y - box_size
      box_x = self.selection_frame.winfo_x()

    self.selection_frame.place(x=box_x, y=box_y)
    self.selection_frame.config(width=box_size, height=box_size)

    self.coords_label.config(text=f"{box_size} x {box_size}")
    self.coords_label.place(x=box_size / 2, y=box_size / 2)

  def mouse_1_up(self, event):

    capture_x = self.selection_frame.winfo_x()
    capture_y = self.selection_frame.winfo_y()
    box_size = self.selection_frame.winfo_width()
    self.root.withdraw()

    self.initial_img_pil = pyautogui.screenshot(region=(
      capture_x, capture_y,
      box_size, box_size
    ))

    Utils.send_toast(
      f"Screenshot taken at: {capture_x}, {capture_y}",
      f"Size: {box_size} x {box_size}"
    )
    print(f"Initial screenshot taken at: {capture_x}, {capture_y}\n  Size: {box_size} x {box_size}")

    self.back_frame.destroy()
    self.root.deiconify()

    options_menu = OptionsMenu(self.root, self.initial_img_pil)
    if options_menu.cancelled:
      return None

    initial_path = path.join(Env.appdata_path, "images/initial.png")
    if(path.exists(initial_path)):
      Path(path.join(Env.appdata_path, "images")).mkdir(parents=True, exist_ok=True)
      self.initial_img_pil.save(initial_path)

    state = state_manager.get()
    state_manager.update(state, {
      "x": int((Env.res_x / 2) - (box_size / 2)),
      "y": int((Env.res_y / 2) - (box_size / 2)),
      "size": box_size, "rotation": 0
    })

    Utils.send_toast(
      "Capture complete", "You can now align the image"
    )

  def key_press(self, event):
    key_events = {
      27: self.root.destroy
    }
    try:
      key_events[event.keycode]()
    except:
      pass


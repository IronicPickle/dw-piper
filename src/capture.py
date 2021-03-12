from os import path, replace, remove
from pathlib import Path
from tkinter import Frame, Label, TOP

import pyautogui
from win10toast import ToastNotifier

from src import state_manager, variables
from src.variables import Env
from src.options_menu import OptionsMenu

class Capture:
  mouse_start = {"x": 0, "y": 0}

  def __init__(self, tk_overlay):

    print("Capture > Started")

    self.img_path = path.join(Env.appdata_path, f"images/initial.png")

    tk_overlay.generate_frames()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

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

  def destroy_root(self):
    self.destroy_back_frame()
    self.root.destroy()
    print("Root > Destroyed")

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Capture > Destroyed")

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

    Path(path.join(Env.appdata_path, "images")).mkdir(parents=True, exist_ok=True)
    temp_initial_path = path.join(Env.appdata_path, "images/initial_temp.png")
    pyautogui.screenshot(temp_initial_path, (
      capture_x, capture_y,
      box_size, box_size
    ))

    self.destroy_back_frame()
    self.root.deiconify()

    options_menu = OptionsMenu(self.tk_overlay)
    if options_menu.cancelled:
      if(path.exists(temp_initial_path)):
        remove(temp_initial_path)
      return None

    initial_path = path.join(Env.appdata_path, "images/initial.png")
    if(path.exists(temp_initial_path)):
      replace(temp_initial_path, initial_path)

    state = state_manager.get()
    state_manager.update(state, {
      "x": int((Env.res_x / 2) - (box_size / 2)),
      "y": int((Env.res_y / 2) - (box_size / 2)),
      "size": box_size, "rotation": 0
    })

    print(f"Initial screenshot taken at: {capture_x}, {capture_y}\n  Size: {box_size} x {box_size}")

    ToastNotifier().show_toast(f"Screenshot taken at: {capture_x}, {capture_y}",
      f"Size: {box_size} x {box_size}",
      icon_path=path.join(Env.index_dir, "images/icon.ico"),
      duration=3,
      threaded=True
    )

  def key_press(self, event):
    key_events = {
      27: self.destroy_root
    }
    try:
      key_events[event.keycode]()
    except:
      pass


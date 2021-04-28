from os import path
from tkinter import Label, Frame, TOP, RIGHT, N
import math
import numpy as np
from time import sleep

from PIL import Image, ImageTk
from pyautogui import position, click, doubleClick

from src.lib import state_manager
from src.lib.variables import Env
from src.lib.tk_resizer import TkResizer

class Map:

  def __init__(self, tk_overlay):

    print("Map > Started")

    state = state_manager.get()
    self.initial_x = 0
    self.initial_y = 0
    self.previous_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.capture_x = int(state["x"] if "x" in state else 0)
    self.capture_y = int(state["y"] if "y" in state else 0)
    self.capture_size = int(state["size"] if "size" in state else 0)
    self.capture_rotation = int(state["rotation"] if "rotation" in state else 0)

    tk_overlay.generate_frames()

    self.tk_overlay = tk_overlay
    self.root = tk_overlay.root
    self.back_frame = tk_overlay.back_frame
    self.front_frame = tk_overlay.front_frame

    self.root.attributes("-fullscreen", True)
    self.root.attributes("-alpha", 0.5)

    self.root.bind("<Key>", self.key_press)

    self.image_frame = Frame(
      self.back_frame,
      bg="#212121"
    )

    self.tk_resizer = TkResizer(self.image_frame).bind_events(self.corner_resize, self.on_rotate)

    self.initial_img = Image.open(path.join(Env.appdata_path, "images/initial.png"))
    initial_photoimage = ImageTk.PhotoImage(self.initial_img)

    self.image_label = Label(
      self.image_frame,
      image=initial_photoimage,
      bg="#212121",
      borderwidth=0,
      cursor="fleur"
    )
    self.image_label.image = initial_photoimage
    self.image_label.pack()

    self.root.bind("<Button-1>", self.mouse_1_down)
    self.root.bind("<ButtonRelease-1>", self.mouse_1_up)

    self.image_label.bind("<B1-Motion>", self.mouse_1_move)
    self.image_label.bind("<ButtonRelease-3>", self.mouse_3_up)
    self.image_frame.bind("<Configure>", self.update_top_info_label)

    self.top_label = Label(
      self.back_frame,
      text="Click and drag to align, resize and resize",
      font=("Courier", 16),
      bg="black",
      fg="white",
      padx=10, pady=10
    )
    self.top_label.pack(side=TOP, pady=(100, 0))

    self.top_info_label = Label(
      self.back_frame,
      font=("Calibri", 12),
      bg="black",
      fg="white",
      padx=10, pady=5
    )
    self.top_info_label.pack(side=TOP, pady=(5, 0))

    self.right_label = Label(
      self.back_frame,
      text="ARROW KEYS - Align\nPLUS - Enlarge\nMINUS - Shrink\n\nENTER - Confirm\nESC - Cancel",
      font=("Courier", 16),
      bg="black",
      fg="white",
      padx=10, pady=10
    )
    self.right_label.pack(side=RIGHT, padx=(0, 50), anchor=N)

    self.back_frame.after(1, self.back_frame_after)

  def destroy_root(self):
    self.save_state()
    self.destroy_back_frame()
    self.root.destroy()
    print("Root > Destroyed")

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Map > Destroyed")

  def corner_resize(self, event, corner):
    mouse_x = position()[0]
    mouse_y = position()[1]

    corner_x = self.capture_x
    corner_y = self.capture_y
    if "w" in corner:
      corner_x = self.capture_x + self.capture_size
    if "n" in corner:
      corner_y = self.capture_y + self.capture_size

    relative_x = mouse_x - corner_x
    relative_y = mouse_y - corner_y
    if "w" in corner:
      relative_x = np.invert(relative_x)
    if "n" in corner:
      relative_y = np.invert(relative_y)

    size = relative_x if relative_x > relative_y else relative_y
    size_difference = self.capture_size - size

    if size < 0:
      return

    new_x = self.capture_x
    new_y = self.capture_y
    if "w" in corner:
      new_x = self.capture_x + size_difference
    if "n" in corner:
      new_y = self.capture_y + size_difference

    self.move_initial_img_x(new_x)
    self.move_initial_img_y(new_y)

    self.resize_initial_img(size, True)

  def on_rotate(self, event, side):
    x = position()[0]
    y = position()[1]
    
    rotation = self.previous_rotation
    if side == "n":
      rotation += (self.initial_x - x) / 4
    elif side == "e":
      rotation += (self.initial_y - y) / 4
    elif side == "s":
      rotation += (x - self.initial_x) / 4
    elif side == "w":
      rotation += (y - self.initial_y) / 4

    self.rotate_initial_img(rotation)

  def mouse_1_down(self, event):
    self.initial_x = position()[0]
    self.initial_y = position()[1]

  def mouse_1_move(self, event):
    self.capture_x = int(self.image_frame.winfo_x())
    self.capture_y = int(self.image_frame.winfo_y())
    mouse_x = position()[0]
    mouse_y = position()[1]

    self.move_initial_img_x(mouse_x - (self.capture_size / 2))
    self.move_initial_img_y(mouse_y - (self.capture_size / 2))

  def mouse_1_up(self, event):
    self.previous_rotation = self.capture_rotation
    self.save_state()

  def mouse_3_up(self, event):
    mouse_x = position()[0]
    mouse_y = position()[1]
    self.root.withdraw()
    sleep(0.1)
    click(x=mouse_x, y=mouse_y)
    self.root.deiconify()

  def finish(self):
    mouse_x = position()[0]
    mouse_y = position()[1]
    self.root.destroy()
    sleep(0.1)
    doubleClick(x=mouse_x, y=mouse_y)

  def save_state(self):
    state_manager.update({
      "x": self.capture_x,
      "y": self.capture_y,
      "size": self.capture_size,
      "rotation": self.capture_rotation
    })

  def key_right(self):
    self.move_initial_img_x(self.capture_x + 1)

  def key_left(self):
    self.move_initial_img_x(self.capture_x - 1)

  def move_initial_img_x(self, x):
    self.capture_x = int(x)
    if x <= 0:
      x = 0
    if x >= Env.res_x - self.capture_size:
      x = Env.res_x - self.capture_size
    self.image_frame.place(x=x + math.floor(self.capture_size / 2))

  def key_up(self):
    self.move_initial_img_y(self.capture_y - 1)

  def key_down(self):
    self.move_initial_img_y(self.capture_y + 1)

  def move_initial_img_y(self, y):
    self.capture_y = int(y)
    if y <= 0:
      y = 0
    if y >= Env.res_y - self.capture_size:
      y = Env.res_y - self.capture_size
    self.image_frame.place(y=y + math.floor(self.capture_size / 2))

  def update_top_info_label(self, event):
    self.top_info_label.config(
      text=f"({self.capture_x}, {self.capture_y}) | " +
      f"{self.capture_size} x {self.capture_size}"
    )

  def key_plus(self):
    self.resize_initial_img(self.capture_size + 2, False)

  def key_minus(self):
    self.resize_initial_img(self.capture_size - 2, False)

  def resize_initial_img(self, size, no_offset):
    size = int(size)
    self.capture_size = size
    if size <= 0 or size > Env.res_x or size > Env.res_y:
      return

    initial_photoimage = ImageTk.PhotoImage(
      self.initial_img
        .rotate(self.capture_rotation, Image.BILINEAR, expand=True)
        .resize((size, size), Image.BILINEAR)
    )
    self.image_label.config(image=initial_photoimage)
    self.image_label.image = initial_photoimage
    offset = -1 if size > self.image_label.winfo_width() else 1
    if no_offset:
      offset = 0
    self.move_initial_img_x(self.capture_x + offset)
    self.move_initial_img_y(self.capture_y + offset)

  def rotate_initial_img(self, rotation):
    rotation = int(rotation)
    self.capture_rotation = rotation

    initial_photoimage = ImageTk.PhotoImage(
      self.initial_img
        .rotate(rotation, Image.BILINEAR, expand=True)
        .resize((self.capture_size, self.capture_size), Image.BILINEAR)
    )
    self.image_label.config(image=initial_photoimage)
    self.image_label.image = initial_photoimage

  def key_press(self, event):
    key_events = {
      27: self.destroy_root,
      37: self.key_left,
      38: self.key_up,
      39: self.key_right,
      40: self.key_down,
      107: self.key_plus,
      109: self.key_minus,
      13: self.finish
    }
    try:
      key_events[event.keycode]()
    except:
      pass

  def back_frame_after(self):
    self.back_frame.focus_force()
    with open(path.join(Env.appdata_path, "state.json"), "r", encoding='utf-8') as state_file:
      self.resize_initial_img(self.capture_size, True)
      self.image_frame.place(
        anchor="center",
        x=self.capture_x + (self.capture_size / 2),
        y=self.capture_y + (self.capture_size / 2)
      )

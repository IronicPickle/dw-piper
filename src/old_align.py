from os import path
from tkinter import Label, Frame, TOP, BOTTOM, RIGHT, LEFT, N, E, S, W, X, Y, BOTH, Tk, filedialog
import math
from pathlib import Path
import pyautogui
import numpy as np
from time import sleep

from PIL import Image, ImageTk
from pyautogui import position
import cv2

from src.auto_align import auto_align

from src.lib import state_manager
from src.lib.variables import Env
from src.lib.pdf_processor import PdfProcessor
from src.lib.tk_overlay import TkOverlay
from src.lib.utils import Utils

class Align(TkOverlay):

  def __init__(self, root = None):

    super().__init__(root)

    self.initial_img = Image.open(path.join(Env.appdata_path, "images/initial.png"))

    state = state_manager.get()
    self.initial_x = 0
    self.initial_y = 0
    self.previous_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.capture_x = int(state["x"] if "x" in state else 0)
    self.capture_y = int(state["y"] if "y" in state else 0)
    self.capture_size = int(state["size"] if "size" in state else 0)
    self.capture_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.generate_frames()

    self.root.attributes("-fullscreen", True)
    self.root.attributes("-alpha", 0.5)

    self.image_frame = Frame(
      self.back_frame,
      bg=Env.bg
    )

    initial_photoimage = ImageTk.PhotoImage(self.initial_img)

    self.image_label = Label(
      self.image_frame,
      image=initial_photoimage,
      bg=Env.bg,
      borderwidth=0
    )
    self.image_label.image = initial_photoimage
    self.image_label.pack()

    self.top_label = Label(
      self.back_frame,
      text="Auto-Aligning...",
      font=("Courier", 16),
      bg=Env.bg,
      fg=Env.fg,
      padx=10, pady=10
    )
    self.top_label.pack(side=TOP, pady=(100, 0))
    
    self.root.bind("<Key>", self.key_press)

    self.back_frame.after(1, self.back_frame_after)

  def on_destroy():
    self.save_state()

  def save_state(self):
    state_manager.update({
      "x": self.capture_x,
      "y": self.capture_y,
      "size": self.capture_size
    })

  def move_initial_img_x(self, x):
    self.capture_x = int(x)
    if x <= 0:
      x = 0
    if x >= Env.res_x - self.capture_size:
      x = Env.res_x - self.capture_size
    self.image_frame.place(x=x + math.floor(self.capture_size / 2))

  def move_initial_img_y(self, y):
    self.capture_y = int(y)
    if y <= 0:
      y = 0
    if y >= Env.res_y - self.capture_size:
      y = Env.res_y - self.capture_size
    self.image_frame.place(y=y + math.floor(self.capture_size / 2))

  def finish(self):

    self.root.destroy()

    Utils.send_toast(
      "Alignment Attempt Completed",
      "Image position and size saved"
    )

  def resize_initial_img(self, size, no_offset=False):
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
      27: self.root.destroy,
      13: self.finish
    }
    try:
      key_events[event.keycode]()
    except Exception as err:
      print(err)
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
    
    self.root.withdraw()
    sleep(0.25)
    screenshot = pyautogui.screenshot()
    self.root.deiconify()

    img = np.array(screenshot.convert("RGB"))
    template = np.array(self.initial_img.convert("RGB"))

    auto_align(
      img, template,
      self.move_initial_img_x, self.move_initial_img_y, self.resize_initial_img, self.root,
      self.finish
    )
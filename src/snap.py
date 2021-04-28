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
from src.lib.variables import Env, WATER_COMPANIES
from src.lib.tk_overlay import TkOverlay
from src.lib.pdf_processor import PdfProcessor
from src.lib.tk_resizer import TkResizer
from src.lib.utils import Utils
from src.lib.file_prompt import FilePromptSave

class Snap(TkOverlay):

  def __init__(self, root, pipe_type, water_company):

    super().__init__(root)

    self.initial_img = Image.open(path.join(Env.appdata_path, "images/initial.png"))

    state = state_manager.get()
    self.initial_x = 0
    self.initial_y = 0
    self.previous_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.water_company = water_company
    self.capture_x = int(state["x"] if "x" in state else 0)
    self.capture_y = int(state["y"] if "y" in state else 0)
    self.capture_size = int(state["size"] if "size" in state else 0)
    self.capture_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.pipe_type = pipe_type
    self.img_path = path.join(Env.appdata_path, f"images/{pipe_type}.png")

    self.generate_frames()

    self.root.attributes("-fullscreen", True)
    self.root.attributes("-alpha", 0.5)

    self.image_frame = Frame(
      self.back_frame,
      bg="#212121"
    )

    self.Resizer = TkResizer(self.image_frame)

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

    self.top_label = Label(
      self.back_frame,
      text="Click and drag to align, resize and rotate",
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

    self.root.bind("<Key>", self.key_press)
    self.root.bind("<Button-1>", self.mouse_1_down)
    self.root.bind("<ButtonRelease-1>", self.mouse_1_up)

    self.image_label.bind("<B1-Motion>", self.mouse_1_move)
    self.image_frame.bind("<Configure>", self.update_top_info_label)

    self.Resizer.bind_events(self.corner_resize, self.on_rotate)

    self.back_frame.after(1, self.back_frame_after)

  def on_destroy(self):
    self.save_state()

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

  def save_state(self):
    state_manager.update({
      "x": self.capture_x,
      "y": self.capture_y,
      "size": self.capture_size
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

  def finish(self):

    self.root.destroy()

    self.take_screenshot()
    self.convert_to_alpha()
    self.apply_masks()

    PdfProcess = PdfProcessor(path.join(Env.index_dir, f"./pdf_templates/{self.pipe_type}_template.pdf"))
    PdfProcess.insert_img(
      path.join(Env.appdata_path, f"images/{self.pipe_type}_final.png"),
      ( 60, 46, 472, 472 ), 0
    )
    PdfProcess.insert_img(
      path.join(Env.index_dir, "./images/copyright.png"),
      ( 60, 510, 210, 9 ), 0
    )
    print("Processed PDF")
    
    state = state_manager.get()

    output_path = map_path = FilePromptSave(
      f"Save {self.pipe_type} PDF file", state["save_dir"] if "save_dir" in state else "/",
      [("PDF File", "*.pdf")], ".pdf", state["reference"] if "reference" in state else "" + (" CC" if self.pipe_type == "clean" else " DD")
    ).path

    if output_path:
      PdfProcess.pdf.save(output_path, deflate=True)
      Utils.send_toast(
        f"Created {path.basename(output_path)} at",
        output_path
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

  def take_screenshot(self):
    Path(Path(self.img_path).parent).mkdir(parents=True, exist_ok=True)

    print(f"{self.capture_size}, {self.capture_size}")

    pyautogui.screenshot(self.img_path, (
      self.capture_x + 1, self.capture_y + 1,
      self.capture_size, self.capture_size
    ))

    print(f"{self.pipe_type} screenshot taken at: {self.capture_x}, {self.capture_y}\n  Size: {self.capture_size} x {self.capture_size}")

  def convert_to_alpha(self):
    if not path.exists(self.img_path):
      raise f"No {self.pipe_type} image found"
    img = cv2.imread(self.img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    cv2.imwrite(self.img_path, img)

  def apply_masks(self):
    final_img = Image.open(path.join(Env.appdata_path, "images/initial.png"))
    img = cv2.imread(self.img_path, flags=cv2.IMREAD_UNCHANGED)
    mask_dir_path = path.join(Env.appdata_path, f"images/masks/{self.pipe_type}")

    Path(mask_dir_path).mkdir(parents=True, exist_ok=True)
    bgra_bounds = WATER_COMPANIES[self.water_company][self.pipe_type]
    for i in bgra_bounds:
      mask_path = path.join(mask_dir_path, f"{i}.png")
      bgra_bound = bgra_bounds[i]
      masked_img = self.apply_mask(img, bgra_bound)
      print(f"Generated {i} mask")
      masked_img = cv2.resize(
        masked_img,
        (final_img.width, final_img.height),
        interpolation=cv2.INTER_CUBIC
      )
      cv2.imwrite(mask_path, masked_img)
      masked_img = Image.open(mask_path)
      final_img.paste(masked_img, (0, 0), masked_img)

    final_img.save(path.join(Env.appdata_path, f"images/{self.pipe_type}_final.png"), "PNG")

  def apply_mask(self, img, bgra_bound):
    mask = cv2.inRange(
      img,
      np.asarray(bgra_bound if type(bgra_bound) == list else bgra_bound[0]),
      np.asarray(bgra_bound if type(bgra_bound) == list else bgra_bound[1])
    )
    return cv2.bitwise_and(
      img,
      img,
      mask=mask
    )

  def key_press(self, event):
    key_events = {
      27: self.root.destroy,
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
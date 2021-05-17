from os import path
from tkinter import Label, Frame, Tk, filedialog, Canvas
import math
from pathlib import Path
from tkinter.constants import CENTER, NW, TOP, BOTTOM, RIGHT, LEFT, N, E, S, W, X, Y, BOTH
import pyautogui
import numpy as np
from time import sleep

from PIL import Image, ImageTk
from pyautogui import position
import cv2

from src.auto_align import auto_align

from src.lib import state_manager, img_utils
from src.lib.variables import Env, WATER_COMPANIES
from src.lib.tk_overlay import TkOverlay
from src.lib.pdf_processor import PdfProcessor
from src.lib.tk_resizer import TkResizer
from src.lib.utils import Utils
from src.lib.file_prompt import FilePromptSave

class TkAligner(TkOverlay):

  def __init__(self, root, dw_img_pil, map_img_pil):

    if dw_img_pil is None:
      raise Exception("dw_img_pil is not a valid PIL image")
    if map_img_pil is None:
      raise Exception("map_img_pil is not a valid PIL image")

    self.initial_dw_img_pil = dw_img_pil
    self.initial_map_img_pil = map_img_pil

    super().__init__(root)

    state = state_manager.get()
    self.previous_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.align_x = int(state["x"] if "x" in state else 0)
    self.align_y = int(state["y"] if "y" in state else 0)
    self.align_width = int(state["width"] if "width" in state else 300)
    self.align_height = int(state["height"] if "height" in state else 300)
    self.align_rotation = int(state["rotation"] if "rotation" in state else 0)

    self.generate_frames()
    self.back_frame.pack_configure(fill = BOTH)
    self.front_frame.pack_configure(fill = BOTH, expand = True)

    self.root.attributes("-fullscreen", True)

    map_img_pil.putalpha(127)
    self.dw_img_pil = img_utils.resize_img(dw_img_pil, self.root.winfo_width(), self.root.winfo_height())
    self.map_img_pil = img_utils.resize_img(map_img_pil, self.align_width, self.align_height)
    
    self.img_canvas = Canvas(self.front_frame, highlightthickness=0, bg=Env.bg)
    self.img_canvas.pack(fill=BOTH, expand=True)
    
    self.back_img_item = self.img_canvas.create_image(0, 0)
    self.front_img_item =  self.img_canvas.create_image(0, 0, anchor=NW)

    self.update_back_img()
    self.update_front_img()

    
    print(self.dw_img_pil.size)
    print(( self.img_canvas.winfo_screenwidth(), self.img_canvas.winfo_screenheight() ))
    
    #self.Resizer = TkResizer(self.front_img_frame)


    for _, key_code in enumerate(( 87, 38 )): # Move image up
      self.register_key_event(key_code, lambda: self.move_front_img_y_rel(-1))
      self.register_key_event(key_code, lambda: self.move_front_img_y_rel(-10), mod="shift")
      self.register_key_event(key_code, lambda: self.move_front_img_y_rel(-50), mod="ctrl")

    for _, key_code in enumerate(( 83, 40 )): # Move image down
      self.register_key_event(key_code, lambda: self.move_front_img_y_rel(1))
      self.register_key_event(key_code, lambda: self.move_front_img_y_rel(10), mod="shift")
      self.register_key_event(key_code, lambda: self.move_front_img_y_rel(50), mod="ctrl")

    for _, key_code in enumerate(( 65, 37 )): # Move image left
      self.register_key_event(key_code, lambda: self.move_front_img_x_rel(-1))
      self.register_key_event(key_code, lambda: self.move_front_img_x_rel(-10), mod="shift")
      self.register_key_event(key_code, lambda: self.move_front_img_x_rel(-50), mod="ctrl")
    
    for _, key_code in enumerate(( 68, 39 )): # Move image right
      self.register_key_event(key_code, lambda: self.move_front_img_x_rel(1))
      self.register_key_event(key_code, lambda: self.move_front_img_x_rel(10), mod="shift")
      self.register_key_event(key_code, lambda: self.move_front_img_x_rel(50), mod="ctrl")

    for _, key_code in enumerate(( 82, 107 )): # Increase image size
      self.register_key_event(key_code, lambda: self.resize_front_img_rel(2))
      self.register_key_event(key_code, lambda: self.resize_front_img_rel(10), mod="shift")
      self.register_key_event(key_code, lambda: self.resize_front_img_rel(50), mod="ctrl")
    
    for _, key_code in enumerate(( 70, 109 )): # Decrease image size
      self.register_key_event(key_code, lambda: self.resize_front_img_rel(-2))
      self.register_key_event(key_code, lambda: self.resize_front_img_rel(-10), mod="shift")
      self.register_key_event(key_code, lambda: self.resize_front_img_rel(-50), mod="ctrl")
    
    for _, key_code in enumerate(( 69, 106 )): # Rotate clockwise
      self.register_key_event(key_code, lambda: self.rotate_front_img_rel(-1))
      self.register_key_event(key_code, lambda: self.rotate_front_img_rel(-15), mod="shift")
      self.register_key_event(key_code, lambda: self.rotate_front_img_rel(-30), mod="ctrl")
    
    for _, key_code in enumerate(( 81, 111 )): # Rotation counter-clockwise
      self.register_key_event(key_code, lambda: self.rotate_front_img_rel(1))
      self.register_key_event(key_code, lambda: self.rotate_front_img_rel(15), mod="shift")
      self.register_key_event(key_code, lambda: self.rotate_front_img_rel(30), mod="ctrl")

    
    self.root.bind("<Key>", self.key_press)


    return self

    self.top_label = Label(
      self.back_frame,
      text="Click and drag to align, resize and rotate",
      font=("Courier", 16),
      bg=Env.bg,
      fg=Env.fg,
      padx=10, pady=10
    )
    self.top_label.pack(side=TOP, pady=(100, 0))

    self.top_info_label = Label(
      self.back_frame,
      font=("Calibri", 12),
      bg=Env.bg,
      fg=Env.fg,
      padx=10, pady=5
    )
    self.top_info_label.pack(side=TOP, pady=(5, 0))

    self.right_label = Label(
      self.back_frame,
      text="ARROW KEYS - Align\nPLUS - Enlarge\nMINUS - Shrink\n\nENTER - Confirm\nESC - Cancel",
      font=("Courier", 16),
      bg=Env.bg, fg=Env.fg,
      padx=10, pady=10
    )
    self.right_label.pack(side=RIGHT, padx=(0, 50), anchor=N)

    self.root.bind("<Button-1>", self.mouse_1_down)
    self.root.bind("<ButtonRelease-1>", self.mouse_1_up)

    self.image_label.bind("<B1-Motion>", self.mouse_1_move)
    self.front_image_frame.bind("<Configure>", self.update_top_info_label)

    self.Resizer.bind_events(self.corner_resize, self.on_rotate)

    self.back_frame.after(1, self.back_frame_after)



  def move_front_img_x_rel(self, x):
    self.move_front_img_x(self.align_x + x)

  def move_front_img_x(self, x):
    x = int(x)
    upper_x = self.root.winfo_width()
    if x + self.align_width > upper_x:
      x = upper_x - self.align_width
    elif x < 0:
      x = 0
    self.align_x = x
    self.update_front_img()



  def move_front_img_y_rel(self, y):
    self.move_front_img_y(self.align_y + y)

  def move_front_img_y(self, y):
    y = int(y)
    upper_y = self.root.winfo_height()
    if y + self.align_height > upper_y:
      y = upper_y - self.align_height
    elif y < 0:
      y = 0
    self.align_y = y
    self.update_front_img()



  def resize_front_img_rel(self, change):
    ratio = self.align_width / self.align_height
    largest = self.align_width if ratio > 1 else self.align_height
    self.resize_front_img(largest + change)

  def resize_front_img(self, size):
    size = int(size)
    old_size = self.map_img_pil.size

    new_align_width, new_align_height = img_utils.calculate_dims(self.initial_map_img_pil, size, size)

    if new_align_width > self.root.winfo_width() or new_align_height > self.root.winfo_height():
      ratio = self.align_width / self.align_height
      smallest = self.root.winfo_width() if ratio > 1 else self.root.winfo_height()
      return self.resize_front_img(smallest)
    elif new_align_width < 300 and new_align_height < 300:
      return self.resize_front_img(300)

    self.align_width, self.align_height = new_align_width, new_align_height
    self.update_front_img()

    new_size = new_align_width, new_align_height
    diff_x, diff_y = old_size[0] - new_size[0], old_size[1] - new_size[1]
    self.move_front_img_x_rel(diff_x / 2)
    self.move_front_img_y_rel(diff_y / 2)


  def rotate_front_img_rel(self, rotation):
    self.rotate_front_img(self.align_rotation + rotation)

  def rotate_front_img(self, rotation):
    self.align_rotation = int(rotation)
    self.update_front_img()


  def update_back_img(self):
    dw_img_tk = ImageTk.PhotoImage(self.dw_img_pil)
    self.img_canvas.itemconfigure(self.back_img_item, image=dw_img_tk)
    self.img_canvas.move(self.back_img_item,
      self.root.winfo_width() / 2,
      self.root.winfo_height() / 2
    )
    self.img_canvas.dw_img = dw_img_tk

  def update_front_img(self):
    print(f"Updating Image: {self.align_x, self.align_y} | {self.align_width} x {self.align_height}")
    self.map_img_pil = img_utils.resize_img(
      img_utils.rotate_img(self.initial_map_img_pil, self.align_rotation), self.align_width, self.align_height
    )
    map_img_tk = ImageTk.PhotoImage(self.map_img_pil)
    self.img_canvas.itemconfigure(self.front_img_item, image=map_img_tk)
    self.img_canvas.moveto(self.front_img_item, self.align_x, self.align_y)
    self.img_canvas.map_img = map_img_tk

  def on_back_destroy(self):
    state_manager.update({
      "x": self.align_x, "y": self.align_y,
      "width": self.align_width, "height": self.align_height,
      "rotation": self.align_rotation
    })









    

  def generate_img(self, frame, img_pil):
    None

  def process_img(self, img_pil):
    align_x, align_y, align_size, align_rotation = (
      self.align_x, self.align_y, self.align_size, self.align_rotation
    )

  def corner_resize(self, event, corner):
    mouse_x = position()[0]
    mouse_y = position()[1]

    corner_x = self.align_x
    corner_y = self.align_y
    if "w" in corner:
      corner_x = self.align_x + self.align_size
    if "n" in corner:
      corner_y = self.align_y + self.align_size

    relative_x = mouse_x - corner_x
    relative_y = mouse_y - corner_y
    if "w" in corner:
      relative_x = np.invert(relative_x)
    if "n" in corner:
      relative_y = np.invert(relative_y)

    size = relative_x if relative_x > relative_y else relative_y
    size_difference = self.align_size - size

    if size < 0:
      return

    new_x = self.align_x
    new_y = self.align_y
    if "w" in corner:
      new_x = self.align_x + size_difference
    if "n" in corner:
      new_y = self.align_y + size_difference

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
    self.align_x = int(self.front_image_frame.winfo_x())
    self.align_y = int(self.front_image_frame.winfo_y())
    mouse_x = position()[0]
    mouse_y = position()[1]

    self.move_initial_img_x(mouse_x - (self.align_size / 2))
    self.move_initial_img_y(mouse_y - (self.align_size / 2))

  def mouse_1_up(self, event):
    self.previous_rotation = self.align_rotation
    self.save_state()

  def save_state(self):
    state_manager.update({
      "x": self.align_x,
      "y": self.align_y,
      "size": self.align_size
    })

  def key_right(self):
    self.move_initial_img_x(self.align_x + 1)

  def key_left(self):
    self.move_initial_img_x(self.align_x - 1)

  def move_initial_img_x(self, x):
    self.align_x = int(x)
    if x <= 0:
      x = 0
    if x >= Env.res_x - self.align_size:
      x = Env.res_x - self.align_size
    self.front_image_frame.place(x=x + math.floor(self.align_size / 2))

  def key_up(self):
    self.move_initial_img_y(self.align_y - 1)

  def key_down(self):
    self.move_initial_img_y(self.align_y + 1)

  def move_initial_img_y(self, y):
    self.align_y = int(y)
    if y <= 0:
      y = 0
    if y >= Env.res_y - self.align_size:
      y = Env.res_y - self.align_size
    self.front_image_frame.place(y=y + math.floor(self.align_size / 2))

  def update_top_info_label(self, event):
    self.top_info_label.config(
      text=f"({self.align_x}, {self.align_y}) | " +
      f"{self.align_size} x {self.align_size}"
    )

  def key_plus(self):
    self.resize_initial_img(self.align_size + 2, False)

  def key_minus(self):
    self.resize_initial_img(self.align_size - 2, False)

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
    self.align_size = size
    if size <= 0 or size > Env.res_x or size > Env.res_y:
      return

    initial_photoimage = ImageTk.PhotoImage(
      self.initial_img
        .rotate(self.align_rotation, Image.BILINEAR, expand=True)
        .resize((size, size), Image.BILINEAR)
      )
    self.image_label.config(image=initial_photoimage)
    self.image_label.image = initial_photoimage
    offset = -1 if size > self.image_label.winfo_width() else 1
    if no_offset:
      offset = 0
    self.move_initial_img_x(self.align_x + offset)
    self.move_initial_img_y(self.align_y + offset)

  def rotate_initial_img(self, rotation):
    rotation = int(rotation)
    self.align_rotation = rotation

    initial_photoimage = ImageTk.PhotoImage(
      self.initial_img
        .rotate(rotation, Image.BILINEAR, expand=True)
        .resize((self.align_size, self.align_size), Image.BILINEAR)
    )
    self.image_label.config(image=initial_photoimage)
    self.image_label.image = initial_photoimage

  def take_screenshot(self):
    Path(Path(self.img_path).parent).mkdir(parents=True, exist_ok=True)

    print(f"{self.align_size}, {self.align_size}")

    pyautogui.screenshot(self.img_path, (
      self.align_x + 1, self.align_y + 1,
      self.align_size, self.align_size
    ))

    print(f"{self.pipe_type} screenshot taken at: {self.align_x}, {self.align_y}\n  Size: {self.align_size} x {self.align_size}")

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

  def back_frame_after(self):
    self.back_frame.focus_force()
    with open(path.join(Env.appdata_path, "state.json"), "r", encoding='utf-8') as state_file:
      self.resize_initial_img(self.align_size, True)
      self.front_image_frame.place(
        anchor="center",
        x=self.align_x + (self.align_size / 2),
        y=self.align_y + (self.align_size / 2)
      )
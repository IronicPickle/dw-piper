from os import path
from tkinter import Label, TOP, Tk, filedialog
import json
import math
from pathlib import Path
import pyautogui
import numpy as np

from PIL import Image, ImageTk
from pyautogui import position
import cv2
from win10toast import ToastNotifier

from vars import Env, Bounds
import state_manager

class Align:
  key_events = {
    27: destroy_root,
    37: key_left,
    38: key_up,
    39: key_right,
    40: key_down,
    107: key_plus,
    109: key_minus,
    13: finish
  }

  def __init__(self, TkOverlay, pipe_type):

    print("Starting align")

    self.pipe_type = pipe_type
    self.img_path = path.join(Env.appdata_path, f"images/{pipe_type}.png")

    TkOverlay.generate_buttons()

    self.tk_overlay = TkOverlay
    self.root = TkOverlay.root
    self.back_frame = TkOverlay.back_frame
    self.front_frame = TkOverlay.front_frame

    self.root.bind("<Key>", self.key_press)

    self.initial_img = Image.open(path.join(Env.appdata_path, "images/initial.png"))
    initial_photoimage = ImageTk.PhotoImage(self.initial_img)

    self.image_label = Label(
      self.back_frame,
      image=initial_photoimage,
      bg="white",
      borderwidth=0,
      cursor="fleur"
    )
    self.image_label.image = initial_photoimage

    self.image_label.bind("<Button-1>", self.mouse_1_down)
    self.image_label.bind("<B1-Motion>", self.mouse_1_move)
    self.image_label.bind("<ButtonRelease-1>", self.mouse_1_up)
    self.image_label.bind("<Configure>", self.update_top_info_label)

    self.top_label = Label(
      self.back_frame,
      text="Click and drag to align",
      font=("Courier", 16),
      bg="black",
      fg="white",
      pady=0, padx=5
    )
    self.top_label.pack(side=TOP, pady=(100, 0))

    self.top_info_label = Label(
      self.back_frame,
      font=("Calibri", 12),
      bg="black",
      fg="white",
      pady=0,
      padx=5
    )
    self.top_info_label.pack(side=TOP)

    self.back_frame.after(1, self.back_frame_after)

  def destroy_root(self):
    self.root.destroy()

  def destroy_back_frame(self):
    self.back_frame.destroy()
    print("Destroyed align")

  def mouse_1_down(self, event):
    self.top_label.config(
      text="Press ENTER to confirm or ESC to cancel",
      font=("Courier", 16)
    )

  def mouse_1_move(self, event):
    self.capture_x = self.image_label.winfo_x()
    self.capture_y = self.image_label.winfo_y()
    self.capture_size = self.image_label.winfo_width()
    self.mouse_x = position()[0]
    self.mouse_y = position()[1]

    self.move_initial_img_x(self.mouse_x - (self.capture_size / 2))
    self.move_initial_img_y(self.mouse_y - (self.capture_size / 2))

  def mouse_1_up(self, event):
    self.save_state()

  def save_state(self):
    with open(Env.state_path, "r", encoding='utf-8') as state_file:
      state = json.loads(state_file.read())
      state["x"] = self.capture_x
      state["y"] = self.capture_y
      state["size"] = self.capture_size
      with open(Env.state_path, "w", encoding='utf-8') as state_file:
        json.dump(state, state_file, ensure_ascii=False, indent=4)

  def key_right(self):
    self.move_initial_img_x(self.capture_x + 1)

  def key_left(self):
    self.move_initial_img_x(self.capture_x - 1)

  def move_initial_img_x(self, x):
    if x <= 0:
      x = 0
    if x >= Env.res_x - self.capture_size:
      x = Env.res_x - self.capture_size
    self.image_label.place(x=x + math.floor(self.capture_size / 2))

  def key_up(self):
    self.move_initial_img_y(self.image_label.winfo_y() - 1)

  def key_down(self):
    self.move_initial_img_y(self.image_label.winfo_y() + 1)

  def move_initial_img_y(self, y):
    if y <= 0:
      y = 0
    if y >= Env.res_y - self.capture_size:
      y = Env.res_y - self.capture_size
    self.image_label.place(y=y + math.floor(self.capture_size / 2))

  def update_top_info_label(self, event):
    self.top_info_label.config(
      text=f"({self.capture_x}, {self.capture_x}) | " +
      f"{self.capture_size} x {self.capture_size}"
    )

  def key_plus(self):
    self.resize_initial_img(self.image_label.winfo_width() + 2)

  def key_minus(self):
    self.resize_initial_img(self.image_label.winfo_width() - 2)



  def finish(self):

    self.destroy_back_frame()
    self.destroy_root()

    self.take_screenshot()
    self.convert_to_alpha()

    pdf_template = pdf_insert_map_img(
      path.join(Env.index_dir, f"./pdf_templates/{self.pipe_type}_template.pdf"),
      path.join(Env.appdata_path, f"images/{self.pipe_type}_final.png"),
      path.join(Env.index_dir, "./images/copyright.png")
    )

    output_path = self.prompt_user_to_save()

    if output_path:
      pdf_template.save(output_path)
      ToastNotifier().show_toast(f"Created {path.basename(output_path)} at",
        output_path,
        icon_path=path.join(Env.index_dir, "icon.ico"),
        duration=3,
        threaded=True
      )

  def resize_initial_img(self, size):
    if size <= 0 or size > Env.res_x or size > Env.res_y:
      return
    photoimage = ImageTk.PhotoImage(self.initial_img.resize((size, size), Image.LANCZOS))
    self.image_label.config(image=photoimage)
    self.image_label.image = photoimage
    self.move_initial_img_x(self.capture_x)
    self.move_initial_img_y(self.capture_y)

  def take_screenshot(self):
    Path(Path(self.img_path).parent).mkdir(parents=True, exist_ok=True)
    pyautogui.screenshot(self.img_path, (
      self.capture_x, self.capture_y,
      self.capture_size, self.capture_size
    ))

    print(f"{self.pipe_type} screenshot taken at: {self.capture_x}, {self.capture_y}\n  Size: {self.capture_size} x {self.capture_size}")

  def convert_to_alpha(self):
    if not path.exists(self.img_path):
      raise "No initial iamge found"
    img = cv2.imread(self.img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    cv2.imwrite(img)

  def apply_masks(self):
    img = Image.open(self.img_path)
    img_size = img.size
    mask_dir_path = path.join(Env.appdata_path, f"images/masks/{self.pipe_type}")

    Path(mask_dir_path).mkdir(parents=True, exist_ok=True)
    bgra_bounds = Bounds.united_utilities[self.pipe_type]
    for i in bgra_bounds:
      mask_path = path.join(mask_dir_path, f"{i}.png")
      bgra_bound = bgra_bounds[i]
      masked_img = self.apply_mask(img, bgra_bound)
      print(f"Generated {i} mask")
      masked_img = cv2.resize(masked_img, (img, img_size), interpolation=cv2.INTER_CUBIC)
      cv2.imwrite(mask_path, masked_img)
      masked_img = Image.open(mask_path)
      img.paste(masked_img, (0, 0), masked_img)

    img.save(path.join(Env.appdata_path, f"images/{self.pipe_type}_final.png"), "PNG")

  def apply_mask(self, img, bgra_bound):
    mask = cv2.inRange(
      img,
      np.asarray(bgra_bound),
      np.asarray(bgra_bound)
    )
    return cv2.bitwise_and(
      img,
      img,
      mask=mask
    )

  def prompt_user_to_save(self):

    root = Tk()
    root.withdraw()

    output_path = None

    def open_prompt():
      state = state_manager.get()

      output_path = filedialog.asksaveasfilename(
        initialdir=state["save_dir"] if "save_dir" in state else "/",
        title=f"Save {self.pipe_type} PDF file",
        filetypes=[("PDF File", "*.pdf")],
        defaultextension=".pdf",
        initialfile="CC" if self.pipe_type == "clean" else "DD"
      )
      root.destroy()

      if output_path:
        state_manager.update(state, { "save_dir": path.dirname(output_path) })

    root.after(1, open_prompt)
    root.mainloop()

    return output_path

  def key_press(self, event):
    try:
      self.key_events[event.keycode]()
    except:
      pass

  def back_frame_after(self):
    self.back_frame.focus_force()
    with open(path.join(Env.appdata_path, "state.json"), "r", encoding='utf-8') as state_file:
      state = json.load(state_file)
      self.resize_initial_img(state["size"])
      self.image_label.place(
        anchor="center",
        x=state["x"] + (state["size"] / 2),
        
        y=state["y"] + (state["size"] / 2))

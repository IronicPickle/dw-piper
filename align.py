import math
import sys
from os import path
import pathlib
import json
import tkinter as tk
from io import BytesIO
import pyautogui
from PIL import Image, ImageTk
import cv2
import win32clipboard
from win10toast import ToastNotifier
import utils
from pdf_processor import replace_img as pdf_replace_img

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))
toaster = ToastNotifier()

def select(root):

  print("Starting align menu")

  if not pathlib.Path(path.join(index_dir, "images/initial.png")).exists():
    print("No initial image found")
    return toaster.show_toast("Couldn't find initial image",
      "You must take a screenshot first",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=10,
      threaded=True
    )
  if not pathlib.Path(path.join(index_dir, "state.json")).exists():
    print("No state file found")
    return toaster.show_toast("Couldn't find state file",
      "You must take a screenshot first",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=10,
      threaded=True
    )

  def destroy_root():
    root.destroy()

  def destroy_back_frame():
    back_frame.destroy()
    print("Destroyed select menu")

  def clean():
    destroy_back_frame()
    main(root, "clean")

  def drainage():
    destroy_back_frame()
    main(root, "drainage")

  def key_press(event):
    try:
      key_events[event.keycode]()
    except:
      pass

  key_events = {
    27: destroy_root,
    67: clean,
    68: drainage
  }

  root.bind("<Key>", key_press)

  root.attributes("-alpha", 0.75)
  root.attributes("-fullscreen", True)
  root.attributes("-topmost", True)
  root.config(bg="black")

  back_frame = tk.Frame(root, bg="black")
  back_frame.pack(
    fill="both",
    expand=True
  )

  front_frame = tk.Frame(back_frame, bg="black")
  front_frame.place(anchor="center", relx=0.5, rely=0.5)

  button_label = tk.Label(
    front_frame,
    text="Choose an Option",
    font=("Courier", 16),
    pady=10,
    bg="black",
    fg="white"
  )
  button_label.pack(side=tk.TOP)

  button_frame = tk.Label(
    front_frame,
    bg="black",
    fg="white"
  )
  button_frame.pack(side=tk.TOP)

  clean_button = tk.Button(
    button_frame,
    text="Clean",
    font=("Courier", 12),
    command=clean,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  clean_button.pack(side=tk.LEFT, padx=10)

  drainage_button = tk.Button(
    button_frame,
    text="Drainage",
    font=("Courier", 12),
    command=drainage,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  drainage_button.pack(side=tk.LEFT, padx=10)

  cancel_button = tk.Button(
    button_frame,
    text="Cancel",
    font=("Courier", 12),
    command=destroy_root,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  cancel_button.pack(side=tk.LEFT, padx=10)

  back_frame.after(1, back_frame.focus_force)

def main(root, pipe_type):

  print("Starting align")

  def destroy_root():
    root.destroy()

  def destroy_back_frame():
    back_frame.destroy()
    print("Destroyed align")

  def mouse_1_down(event):
    top_label.config(
      text="Press ENTER to confirm or ESC to cancel",
      font=("Courier", 16)
    )

  def mouse_1_move(event):
    width = image_label.image.width()
    height = image_label.image.height()
    mouse_pos = pyautogui.position()
    x, y = mouse_pos[0] - (width / 2), mouse_pos[1] - (height / 2)

    move_initial_img_x(x)
    move_initial_img_y(y)

  def mouse_1_up(event):
    None

  def key_right():
    move_initial_img_x(image_label.winfo_x() + 1)

  def key_left():
    move_initial_img_x(image_label.winfo_x() - 1)

  def move_initial_img_x(x):
    width = image_label.winfo_width()
    if x <= 0:
      x = 0
    if x >= res[0] - width:
      x = res[0] - width
    image_label.place(x=x + math.floor(width / 2))

  def key_up():
    move_initial_img_y(image_label.winfo_y() - 1)

  def key_down():
    move_initial_img_y(image_label.winfo_y() + 1)

  def move_initial_img_y(y):
    height = image_label.winfo_height()
    if y <= 0:
      y = 0
    if y >= res[1] - height:
      y = res[1] - height
    image_label.place(y=y + math.floor(height / 2))

  def update_top_info_label(event):
    top_info_label.config(
      text=f"({image_label.winfo_x()}, {image_label.winfo_y()}) | " +
      f"{image_label.winfo_width()} x {image_label.winfo_height()}"
    )

  def key_plus():
    resize_initial_img(image_label.winfo_width() + 2)

  def key_minus():
    resize_initial_img(image_label.winfo_width() - 2)

  def resize_initial_img(size):
    if size <= 0 or size > res[0] or size > res[1]:
      return
    photoimage = ImageTk.PhotoImage(initial_img.resize((size, size), Image.LANCZOS))
    image_label.config(image=photoimage)
    image_label.image = photoimage
    move_initial_img_x(image_label.winfo_x())
    move_initial_img_y(image_label.winfo_y())

  def finish():
    capture_x = image_label.winfo_x()
    capture_y = image_label.winfo_y()
    box_size = image_label.winfo_width()
    destroy_back_frame()
    destroy_root()
    pathlib.Path(path.join(index_dir, "images")).mkdir(parents=True, exist_ok=True)
    pyautogui.screenshot(path.join(index_dir, f"images/{pipe_type}.png"), (
      capture_x, capture_y,
      image_label.image.width(), image_label.image.height()
    ))

    print(f"{pipe_type} screenshot taken at: {capture_x}, {capture_y}\n  Size: {box_size} x {box_size}")

    img = cv2.cvtColor(cv2.imread(path.join(index_dir, f"images/{pipe_type}.png")), cv2.COLOR_BGR2BGRA)
    final_img = initial_img.resize((box_size, box_size), Image.LANCZOS)

    pathlib.Path(path.join(index_dir, "images/masks/drainage")).mkdir(parents=True, exist_ok=True)
    pathlib.Path(path.join(index_dir, "images/masks/clean")).mkdir(parents=True, exist_ok=True)
    for i in utils.bgra_bounds[pipe_type]:
      bgra_bound = utils.bgra_bounds[pipe_type][i]
      masked_img = utils.apply_mask(img, bgra_bound)
      print(f"Generated {i} mask")
      cv2.imwrite(path.join(index_dir, f"images/masks/{pipe_type}/{i}.png"), masked_img)
      masked_img = Image.open(path.join(index_dir, f"images/masks/{pipe_type}/{i}.png"))
      final_img.paste(masked_img, (0, 0), masked_img)

    final_img.save(path.join(index_dir, f"images/{pipe_type}_final.png"), "PNG")
    pdf_replace_img(
      path.join(index_dir, f"./pdf_templates/{pipe_type}_template.pdf"),
      path.join(index_dir, f"images/{pipe_type}_final.png"), pipe_type
    )

    with open(path.join(index_dir, "state.json"), "w", encoding='utf-8') as state_file:
      json.dump({
        "x": capture_x, "y": capture_y, "size": box_size
      }, state_file, ensure_ascii=False, indent=4)

    toaster.show_toast(f"Created {pipe_type}.pdf",
      f"Size: {box_size} x {box_size}",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=3,
      threaded=True
    )

  def key_press(event):
    try:
      key_events[event.keycode]()
    except:
      pass

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

  root.bind("<Key>", key_press)

  root.attributes("-alpha", 0.5)
  root.attributes("-fullscreen", True)
  root.attributes("-topmost", True)
  root.config(bg="black")

  back_frame = tk.Frame(root, bg="black")
  back_frame.pack(
    fill="both",
    expand=True
  )

  initial_img = Image.open(path.join(index_dir, "images/initial.png"))
  initial_photoimage = ImageTk.PhotoImage(initial_img)

  image_label = tk.Label(
    back_frame,
    image=initial_photoimage,
    bg="white",
    borderwidth=0,
    cursor="fleur"
  )
  image_label.image = initial_photoimage

  image_label.bind("<Button-1>", mouse_1_down)
  image_label.bind("<B1-Motion>", mouse_1_move)
  image_label.bind("<ButtonRelease-1>", mouse_1_up)
  image_label.bind("<Configure>", update_top_info_label)

  top_label = tk.Label(
    back_frame,
    text="Click and drag to align",
    font=("Courier", 16),
    bg="black",
    fg="white",
    pady=0, padx=5
  )
  top_label.pack(side=tk.TOP, pady=(100, 0))

  top_info_label = tk.Label(
    back_frame,
    font=("Calibri", 12),
    bg="black",
    fg="white",
    pady=0,
    padx=5
  )
  top_info_label.pack(side=tk.TOP)

  def back_frame_after():
    back_frame.focus_force()
    with open(path.join(index_dir, "state.json"), "r", encoding='utf-8') as state_file:
      state = json.load(state_file)
      resize_initial_img(state["size"])
      image_label.place(
        anchor="center",
        x=state["x"] + (state["size"] / 2),
        y=state["y"] + (state["size"] / 2))

  back_frame.after(1, back_frame_after)

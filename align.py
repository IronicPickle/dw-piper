import math
import sys
from os import path, getenv
import pathlib
import json
import tkinter as tk
from tkinter import filedialog as fd

import pyautogui
from PIL import Image, ImageTk
import cv2
from win10toast import ToastNotifier

import utils
from pdf_processor import insert_map_img as pdf_insert_map_img

toaster = ToastNotifier()

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))
appdata_path = path.join(getenv('APPDATA'), "DW-Piper")

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
    pathlib.Path(path.join(appdata_path, "images")).mkdir(parents=True, exist_ok=True)
    pyautogui.screenshot(path.join(appdata_path, f"images/{pipe_type}.png"), (
      capture_x, capture_y,
      image_label.image.width(), image_label.image.height()
    ))

    print(f"{pipe_type} screenshot taken at: {capture_x}, {capture_y}\n  Size: {box_size} x {box_size}")

    img = cv2.cvtColor(cv2.imread(path.join(appdata_path, f"images/{pipe_type}.png")), cv2.COLOR_BGR2BGRA)
    final_img = Image.open(path.join(appdata_path, "images/initial.png"))
    width, height = final_img.size

    pathlib.Path(path.join(appdata_path, "images/masks/drainage")).mkdir(parents=True, exist_ok=True)
    pathlib.Path(path.join(appdata_path, "images/masks/clean")).mkdir(parents=True, exist_ok=True)
    for i in utils.bgra_bounds[pipe_type]:
      bgra_bound = utils.bgra_bounds[pipe_type][i]
      masked_img = utils.apply_mask(img, bgra_bound)
      print(f"Generated {i} mask")
      masked_img = cv2.resize(masked_img, (height, width), interpolation=cv2.INTER_CUBIC)
      cv2.imwrite(path.join(appdata_path, f"images/masks/{pipe_type}/{i}.png"), masked_img)
      masked_img = Image.open(path.join(appdata_path, f"images/masks/{pipe_type}/{i}.png"))
      final_img.paste(masked_img, (0, 0), masked_img)

    state_path = path.join(appdata_path, "state.json")
    default_state = {
      "x": capture_x, "y": capture_y, "size": box_size
    }

    with open(state_path, "r", encoding='utf-8') as state_file:
      state = json.loads(state_file.read())
      state["x"] = default_state["x"]
      state["y"] = default_state["y"]
      state["size"] = default_state["size"]
      with open(state_path, "w", encoding='utf-8') as state_file:
        json.dump(state, state_file, ensure_ascii=False, indent=4)

    final_img.save(path.join(appdata_path, f"images/{pipe_type}_final.png"), "PNG")
    pdf_template = pdf_insert_map_img(
      path.join(index_dir, f"./pdf_templates/{pipe_type}_template.pdf"),
      path.join(appdata_path, f"images/{pipe_type}_final.png"),
      path.join(index_dir, "./images/copyright.png")
    )

    root = tk.Tk()
    root.withdraw()

    output_path = None

    def open_file_dialog():
      nonlocal output_path
      nonlocal pipe_type

      state_path = path.join(appdata_path, "state.json")
      with open(state_path, "r", encoding='utf-8') as state_file:
        state = json.loads(state_file.read())

        output_path = fd.asksaveasfilename(
          initialdir=state["save_dir"] if "save_dir" in state else "/",
          title=f"Save {pipe_type} PDF file",
          filetypes=[("PDF File", "*.pdf")],
          defaultextension=".pdf",
          initialfile="CC" if pipe_type == "clean" else "DD"
        )

        if output_path:
          state["save_dir"] = path.dirname(output_path)

          with open(state_path, "w", encoding='utf-8') as state_file:
            json.dump(state, state_file, ensure_ascii=False, indent=4)

      root.destroy()

    root.after(1, open_file_dialog)
    root.mainloop()

    if output_path:
      pdf_template.save(output_path)
      toaster.show_toast(f"Created {path.basename(output_path)} at",
        output_path,
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

  initial_img = Image.open(path.join(appdata_path, "images/initial.png"))
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
    with open(path.join(appdata_path, "state.json"), "r", encoding='utf-8') as state_file:
      state = json.load(state_file)
      resize_initial_img(state["size"])
      image_label.place(
        anchor="center",
        x=state["x"] + (state["size"] / 2),
        
        y=state["y"] + (state["size"] / 2))

  back_frame.after(1, back_frame_after)

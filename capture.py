import sys
from os import path
import pathlib
import json
import tkinter as tk

import pyautogui

from win10toast import ToastNotifier

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))
toaster = ToastNotifier()

def main(root):

  print("Starting capture")

  mouse_start = {"x": 0, "y": 0}

  def destroy_root():
    root.destroy()

  def destroy_back_frame():
    back_frame.destroy()
    print("Destroyed capture")

  def mouse_1_down(event):
    selection_frame.pack()
    mouse_start["x"], mouse_start["y"] = event.x, event.y
    selection_frame.place(x=event.x, y=event.y)

  def mouse_1_move(event):
    width = event.x - mouse_start["x"]
    height = event.y - mouse_start["y"]
    box_size = 0

    if abs(width) > abs(height):
      box_size = width if height > 0 else -width
    if abs(height) > abs(width):
      box_size = height if width > 0 else -height

    box_x = mouse_start["x"]
    box_y = mouse_start["y"]

    if event.x - mouse_start["x"] < 0:
      box_x -= abs(box_size)
    if event.y - mouse_start["y"] < 0:
      box_y -= abs(box_size)

    box_size = abs(box_size)

    if box_x < 0:
      box_size = selection_frame.winfo_width()
      box_x = 0
      box_y = selection_frame.winfo_y()
    elif box_x + box_size > res[0]:
      box_size = selection_frame.winfo_width()
      box_x = res[0] - box_size
      box_y = selection_frame.winfo_y()

    elif box_y < 0:
      box_size = selection_frame.winfo_width()
      box_y = 0
      box_x = selection_frame.winfo_x()
    elif box_y + box_size > res[1]:
      box_size = selection_frame.winfo_width()
      box_y = res[1] - box_size
      box_x = selection_frame.winfo_x()

    selection_frame.place(x=box_x, y=box_y)
    selection_frame.config(width=box_size, height=box_size)

    coords_label.config(text=f"{box_size} x {box_size}")
    coords_label.place(x=box_size / 2, y=box_size / 2)

  def mouse_1_up(event):
    capture_x = selection_frame.winfo_x()
    capture_y = selection_frame.winfo_y()
    box_size = selection_frame.winfo_width()
    destroy_back_frame()
    destroy_root()
    pathlib.Path(path.join(index_dir, "images")).mkdir(parents=True, exist_ok=True)
    pyautogui.screenshot(path.join(index_dir, "images/initial.png"), (
      capture_x, capture_y,
      box_size, box_size
    ))

    with open(path.join(index_dir, "state.json"), "w", encoding='utf-8') as state_file:
      json.dump({
        "x": int((res[0] / 2) - (box_size / 2)),
        "y": int((res[1] / 2) - (box_size / 2)),
        "size": box_size
      }, state_file, ensure_ascii=False, indent=4)

    print(f"Initial screenshot taken at: {capture_x}, {capture_y}\n  Size: {box_size} x {box_size}")

    toaster.show_toast(f"Screenshot taken at: {capture_x}, {capture_y}",
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
    27: destroy_root
  }

  root.attributes("-alpha", 0.5)
  root.attributes("-fullscreen", True)
  root.attributes("-topmost", True)
  root.config(bg="black", cursor="tcross")

  back_frame = tk.Frame(root, bg="black")
  back_frame.pack(
    fill="both",
    expand=True
  )

  back_frame.bind("<Button-1>", mouse_1_down)
  back_frame.bind("<B1-Motion>", mouse_1_move)
  back_frame.bind("<ButtonRelease-1>", mouse_1_up)
  back_frame.bind("<Key>", key_press)

  selection_frame = tk.Frame(
    back_frame,
    bg="white",
    borderwidth=2
  )

  top_label = tk.Label(
    back_frame,
    text="Click and drag to select an area\nor press ESC to cancel",
    font=("Courier", 16),
    bg="black",
    fg="white",
    pady=0, padx=5
  )
  top_label.pack(side=tk.TOP, pady=(100, 0))

  coords_label = tk.Label(
    selection_frame,
    text="0 x 0",
    font=("Courier", 16),
    bg="black",
    fg="white",
    pady=0,
    padx=5
  )
  coords_label.place(anchor="center")

  back_frame.after(1, back_frame.focus_force)

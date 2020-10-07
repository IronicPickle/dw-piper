import sys
from os import path, getenv
import pathlib
import tkinter as tk

from win10toast import ToastNotifier

from align import main as align_main

index_dir = path.abspath(path.dirname(sys.argv[0]))
appdata_path = path.join(getenv('APPDATA'), "DW-Piper")
toaster = ToastNotifier()

def main(root):

  print("Starting align menu")

  def destroy_root():
    root.destroy()

  def destroy_back_frame():
    back_frame.destroy()
    print("Destroyed select menu")

  def clean():
    destroy_back_frame()
    align_main(root, "clean")

  def drainage():
    destroy_back_frame()
    align_main(root, "drainage")

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

  if not pathlib.Path(path.join(appdata_path, "images/initial.png")).exists():
    destroy_root()
    print("No initial image found")
    return toaster.show_toast("Couldn't find initial image",
      "You must take a screenshot first",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=10,
      threaded=True
    )
  if not pathlib.Path(path.join(appdata_path, "state.json")).exists():
    destroy_root()
    print("No state file found")
    return toaster.show_toast("Couldn't find state file",
      "You must take a screenshot first",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=10,
      threaded=True
    )

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

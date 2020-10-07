import sys
from os import path
import tkinter as tk

import pyautogui

from upload import main as upload_main
from capture import main as capture_main
from align_menu import main as align_menu_main

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))

def main():

  print("Starting main menu")

  root = tk.Tk()

  def destroy_root():
    root.destroy()

  def destroy_back_frame():
    back_frame.destroy()
    print("Destroyed main menu")

  def upload():
    destroy_back_frame()
    root.destroy()
    upload_main()

  def capture():
    destroy_back_frame()
    capture_main(root)

  def align():
    destroy_back_frame()
    align_menu_main(root)

  def key_press(event):
    try:
      key_events[event.keycode]()
    except:
      pass

  key_events = {
    27: destroy_root,
    85: upload,
    67: capture,
    65: align
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

  upload_button = tk.Button(
    button_frame,
    text="Upload",
    font=("Courier", 12),
    command=upload,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  upload_button.pack(side=tk.LEFT, padx=10)

  capture_button = tk.Button(
    button_frame,
    text="Capture",
    font=("Courier", 12),
    command=capture,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  capture_button.pack(side=tk.LEFT, padx=10)

  align_button = tk.Button(
    button_frame,
    text="Align",
    font=("Courier", 12),
    command=align,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  align_button.pack(side=tk.LEFT, padx=10)

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

  root.after(1, root.focus_force)

  root.mainloop()
  print("Root destroyed")

if __name__ == "__main__": main()

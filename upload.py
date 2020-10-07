import sys
from os import path, remove
import pathlib
import json
import tkinter as tk
from tkinter import filedialog as fd

from win10toast import ToastNotifier
import pyautogui

from pdf_processor import extract_map_img as pdf_extract_map_img

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))
toaster = ToastNotifier()

def main():

  root = tk.Tk()
  root.withdraw()

  input_dir = None

  def open_file_dialog():
    nonlocal input_dir
    input_dir = fd.askopenfilename(
      initialdir="/",
      title="Upload a mapping PDF",
      filetypes=[("PDF File", "*.pdf")],
      defaultextension=".pdf"
    )
    root.destroy()

  root.after(1, open_file_dialog)
  root.mainloop()

  if not input_dir:
    return
  map_pix = pdf_extract_map_img(input_dir)

  if map_pix:

    pathlib.Path(path.join(index_dir, "images")).mkdir(parents=True, exist_ok=True)
    if path.exists(path.join(index_dir, "images/initial.png")):
      remove(path.join(index_dir, "images/initial.png"))
    map_pix.writePNG(path.join(index_dir, "images/initial.png"))

    box_size = int(res[1] / 1.5)

    with open(path.join(index_dir, "state.json"), "w", encoding='utf-8') as state_file:
      json.dump({
        "x": int((res[0] / 2) - (box_size / 2)),
        "y": int((res[1] / 2) - (box_size / 2)),
        "size": box_size
      }, state_file, ensure_ascii=False, indent=4)

    toaster.show_toast("Map extraction success",
      "You can now align the image",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=3,
      threaded=True
    )

  else:
    toaster.show_toast("Map extraction failed",
      "Please make sure your pdf is formatted correctly",
      icon_path=path.join(index_dir, "icon.ico"),
      duration=3,
      threaded=True
    )


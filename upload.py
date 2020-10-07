import sys
from os import path, remove, getenv
import pathlib
import json
import tkinter as tk
from tkinter import filedialog as fd

from win10toast import ToastNotifier
import pyautogui

from pdf_processor import extract_map_img as pdf_extract_map_img
from pdf_processor import reprocess_map_img as pdf_reprocess_map_img

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))
appdata_path = path.join(getenv('APPDATA'), "DW-Piper")
toaster = ToastNotifier()

def main():

  root = tk.Tk()
  root.withdraw()

  upload_dir = None

  box_size = int(res[1] / 1.5)
  default_state = {
    "x": int((res[0] / 2) - (box_size / 2)),
    "y": int((res[1] / 2) - (box_size / 2)),
    "size": box_size
  }

  def open_file_dialog():
    nonlocal upload_dir

    state_path = path.join(appdata_path, "state.json")

    if not path.exists(state_path):
      with open(state_path, "w", encoding='utf-8') as state_file:
        json.dump(default_state, state_file, ensure_ascii=False, indent=4)

    with open(state_path, "r", encoding='utf-8') as state_file:
      state = json.loads(state_file.read())

      upload_dir = fd.askopenfilename(
        initialdir=state["upload_dir"] if "upload_dir" in state else "/",
        title="Upload a mapping PDF",
        filetypes=[("PDF File", "*.pdf")],
        defaultextension=".pdf"
      )

      if upload_dir:
        state["upload_dir"] = path.dirname(upload_dir)

        with open(state_path, "w", encoding='utf-8') as state_file:
          json.dump(state, state_file, ensure_ascii=False, indent=4)

    root.destroy()

  root.after(1, open_file_dialog)
  root.mainloop()

  if not upload_dir:
    return
  map_pix = pdf_extract_map_img(upload_dir)

  if map_pix:

    pathlib.Path(path.join(appdata_path, "images")).mkdir(parents=True, exist_ok=True)
    if path.exists(path.join(appdata_path, "images/initial.png")):
      remove(path.join(appdata_path, "images/initial.png"))
    map_pix.writePNG(path.join(appdata_path, "images/initial.png"))
    pdf_reprocess_map_img(path.join(appdata_path, "images/initial.png"))

    state_path = path.join(appdata_path, "state.json")

    with open(state_path, "r", encoding='utf-8') as state_file:
      state = json.loads(state_file.read())
      state["x"] = default_state["x"]
      state["y"] = default_state["y"]
      state["size"] = default_state["size"]
      with open(state_path, "w", encoding='utf-8') as state_file:
        json.dump(state, state_file, ensure_ascii=False, indent=4)

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


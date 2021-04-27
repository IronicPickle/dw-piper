from os import path, remove
from tkinter import Tk
from pathlib import Path

from src.menus.options_menu import OptionsMenu, save_ref

from src.lib.pdf_processor import PdfProcessor
from src.lib.img_utils import crop_img
from src.lib.tk_overlay import TkOverlay
from src.lib.utils import Utils
from src.lib.file_prompt import FilePromptOpen
from src.lib import state_manager
from src.lib.variables import Env

class Extract:

  def __init__(self, map_path=None, ref=None):
    
    state = state_manager.get()

    if not map_path:
      map_path = FilePromptOpen(
        "Choose a PDF", state["map_path"], [("PDF File", "*.pdf")]
      ).path

    if not map_path:
      return None

    state_manager.update(state, { "map_path": path.dirname(map_path) })

    PdfProcess = PdfProcessor(map_path)
    img_pix = PdfProcess.extract_img(16)

    img_path = path.join(Env.appdata_path, "images/initial.png")

    if not img_pix:
      Utils.send_toast(
        "Map extraction failed",
        "Please make sure your pdf is formatted correctly"
      )
      return None

    Path(path.join(Env.appdata_path, "images")).mkdir(parents=True, exist_ok=True)
    if path.exists(img_path):
      remove(img_path)
    img_pix.writePNG(img_path)
    crop_img(img_path, 1, 1, img_pix.width, img_pix.height)

    state = state_manager.get()
    size = int(Env.res_y / 1.5)
    state_manager.update(state, {
      "x": int((Env.res_x / 2) - (size / 2)),
      "y": int((Env.res_y / 2) - (size / 2)),
      "size": size, "rotation": 0
    })

    if not ref:
      Utils.send_toast(
        "Map extraction success",
        "Input a reference to continue"
      )
      option_menu = OptionsMenu()
      if option_menu.cancelled: return None
      ref = option_menu.reference.get()
    else:
      save_ref(ref)
  
    Utils.send_toast(
      "Map extraction complete", "You can now align the image"
    )

    
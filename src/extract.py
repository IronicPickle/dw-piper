from os import path, remove
from io import BytesIO
from tkinter import Tk
from pathlib import Path

from PIL import Image

from src.menus.options_menu import OptionsMenu
from src.menus.img_selector_menu import ImgSelectorMenu

from src.lib.pdf_processor import PdfProcessor
from src.lib.img_utils import crop_img
from src.lib.tk_overlay import TkOverlay
from src.lib.utils import Utils
from src.lib.file_prompt import FilePromptOpen
from src.lib import state_manager
from src.lib.variables import Env

class Extract:

  def __init__(self, source = None, source_path = None, xref = None, ref = None):

    if not [ "dw", "map" ].__contains__(source):
      return

    self.source = source
    self.source_name = { "dw": "DW", "map": "Map" }[source]
    
    state = state_manager.get()

    if not source_path:
      source_path = FilePromptOpen(
        "Choose a PDF", state["source_path"] if "source_path" in state else "/", [("PDF File", "*.pdf")]
      ).path

    if not source_path:
      return

    state_manager.update({ "source_path": path.dirname(source_path) })

    self.PdfProcess = PdfProcessor(source_path)

    img_pil = self.specific_extract(xref) if xref is not None else self.full_extract()

    if not img_pil:
      Utils.send_toast(
        "Map extraction failed",
        "Please make sure your pdf is formatted correctly"
      )
      return

    img_path = path.join(Env.appdata_path, f"images/{source}_source.png")
    Path(path.join(Env.appdata_path, "images")).mkdir(parents=True, exist_ok=True)
    if path.exists(img_path):
      remove(img_path)
    img_pil.save(img_path)
    
    #width, height = img_pil.size
    #crop_img(img_path, 1, 1, width, height)

    size = int(Env.res_y / 1.5)
    state_manager.update({
      "x": int((Env.res_x / 2) - (size / 2)),
      "y": int((Env.res_y / 2) - (size / 2)),
      "size": size, "rotation": 0
    })

    if not ref:
      Utils.send_toast(
        "Map extraction success",
        "Input a reference to continue"
      )
      option_menu = OptionsMenu(None, source, img_pil)
      if option_menu.cancelled:
        return

    else:
      state_manager.update({ "reference": ref })
  
    Utils.send_toast(
      "Map extraction complete", "You can now align the image"
    )

  def full_extract(self):
    pix_imgs = self.PdfProcess.extract_imgs()
    pil_imgs = []
    for i, pix_img in enumerate(pix_imgs):
      pil_img_data = pix_img.pillowData("png")
      pil_img = Image.open(BytesIO(pil_img_data))
      pil_imgs.append(pil_img)

    ImgSelector = ImgSelectorMenu(None, pil_imgs)
    if ImgSelector.cancelled:
      return
    
    return ImgSelector.selected_img_pil

  def specific_extract(self, xref):
    pix_img = self.PdfProcess.extract_img(xref)
    if pix_img is None:
      return None
    pil_img_data = pix_img.pillowData("png")
    return Image.open(BytesIO(pil_img_data))
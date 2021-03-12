from os import path, remove
from tkinter import Tk, filedialog
from pathlib import Path

from win10toast import ToastNotifier

from src import variables, pdf_processor, state_manager, img_utils
from src.variables import Env
from src.pdf_processor import PdfProcessor
from src.img_utils import crop_img
from src.options_menu import OptionsMenu, save_ref
from src.tk_overlay import TkOverlay

class Upload:

  def __init__(self, map_path=None, ref=None):

    if not map_path:
      map_path = self.prompt_user_to_open()

    if not map_path:
      return None

    pdf_process = PdfProcessor(map_path)
    img_pix = pdf_process.extract_img(16)

    img_path = path.join(Env.appdata_path, "images/initial.png")

    if not img_pix:
      ToastNotifier().show_toast("Map extraction failed",
        "Please make sure your pdf is formatted correctly",
        icon_path=path.join(Env.index_dir, "images/icon.ico"),
        duration=3,
        threaded=True
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
      option_menu = OptionsMenu(TkOverlay())
      if option_menu.cancelled: return None
      ref = option_menu.reference.get()
    else:
      save_ref(ref)

    ToastNotifier().show_toast("Map extraction success",
      f"You can now align the image\nReference: {ref}",
      icon_path=path.join(Env.index_dir, "images/icon.ico"),
      duration=3,
      threaded=True
    )

  def prompt_user_to_open(self):

    root = Tk()
    root.withdraw()

    map_path = None

    def open_prompt():
      nonlocal map_path
      state = state_manager.get()

      map_path = filedialog.askopenfilename(
        parent=root,
        initialdir=state["map_path"] if "map_path" in state else "/",
        title="Upload a mapping PDF",
        filetypes=[("PDF File", "*.pdf")],
        defaultextension=".pdf"
      )
      root.destroy()

      if map_path:
        state_manager.update(state, { "map_path": path.dirname(map_path) })

    root.after(1, open_prompt)
    root.mainloop()

    return map_path
from os import path, remove
from tkinter import Tk, filedialog
from pathlib import Path

from win10toast import ToastNotifier

from src import variables, pdf_processor, state_manager, img_utils
from src.variables import Env
from src.pdf_processor import PdfProcessor
from src.img_utils import crop_img
from src.options_menu import OptionsMenu
from src.tk_overlay import TkOverlay

class Upload:

  def __init__(self):

    upload_dir = self.prompt_user_to_open()

    if not upload_dir:
      return None

    pdf_process = PdfProcessor(upload_dir)
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
      "size": size
    })

    OptionsMenu(TkOverlay())

    ToastNotifier().show_toast("Map extraction success",
      "You can now align the image",
      icon_path=path.join(Env.index_dir, "images/icon.ico"),
      duration=3,
      threaded=True
    )

  def prompt_user_to_open(self):

    root = Tk()
    root.withdraw()

    upload_dir = None

    def open_prompt():
      nonlocal upload_dir
      state = state_manager.get()

      upload_dir = filedialog.askopenfilename(
        initialdir=state["upload_dir"] if "upload_dir" in state else "/",
        title="Upload a mapping PDF",
        filetypes=[("PDF File", "*.pdf")],
        defaultextension=".pdf"
      )
      root.destroy()

      if upload_dir:
        state_manager.update(state, { "upload_dir": path.dirname(upload_dir) })

    root.after(1, open_prompt)
    root.mainloop()

    return upload_dir

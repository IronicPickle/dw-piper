from os import path
from tkinter import Tk, Frame, Label, LEFT, RIGHT, TOP

from PIL import Image, ImageTk

from src.extract import Extract
from src.capture import Capture
from src.align import Align
from src.map import Map

from src.menus.snap_menu import SnapMenu

from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env

class MainMenu(TkOverlay):

  def __init__(self, root = None):

    super().__init__(root)

    self.generate_frames()
    self.generate_header()
    self.generate_title("Choose an Option")

    self.resize(800, 800)

    self.root.bind("<Key>", self.key_press)

    self.source_frame = Frame(self.front_frame, bg="#212121")
    self.source_frame.pack(side=TOP, pady=(0, 20))

    self.left_frame = Frame(self.source_frame, bg="#212121")
    self.left_frame.pack(side=LEFT, padx=10)

    self.right_frame = Frame(self.source_frame, bg="#212121")
    self.right_frame.pack(side=RIGHT, padx=10)

    self.generate_sub_title(self.left_frame, "DW Source")
    self.generate_sub_title(self.right_frame, "Map Source")

    self.generate_divider(self.left_frame)
    self.generate_divider(self.right_frame)

    dw_img_path = path.join(Env.appdata_path, "images/dw_source.png")
    map_img_path = path.join(Env.appdata_path, "images/map_source.png")
    no_img_path = path.join(Env.index_dir, "images/no_image.png")

    dw_img_pil = Image.open(dw_img_path) if path.exists(dw_img_path) else Image.open(no_img_path)
    map_img_pil = Image.open(map_img_path) if path.exists(map_img_path) else Image.open(no_img_path)

    dw_img_tk = ImageTk.PhotoImage(dw_img_pil)
    map_img_tk = ImageTk.PhotoImage(map_img_pil)

    self.generate_img(self.left_frame, dw_img_tk)
    self.generate_img(self.right_frame, map_img_tk)

    self.generate_divider(self.left_frame)
    self.generate_divider(self.right_frame)

    left_button_label = Label(self.left_frame, bg="#212121")
    left_button_label.pack(side=TOP)

    right_button_label = Label(self.right_frame, bg="#212121")
    right_button_label.pack(side=TOP)

    self.generate_button("Capture", self.start_capture_dw, left_button_label)
    self.generate_button("Extract", self.start_extract_dw, left_button_label)

    self.generate_button("Capture", self.start_capture_map, right_button_label)
    self.generate_button("Extract", self.start_extract_map, right_button_label)

    self.generate_sub_title(self.front_frame, "Other Options")
    self.generate_divider(self.front_frame)

    bottom_button_label = Label(self.front_frame, bg="#212121")
    bottom_button_label.pack(side=TOP)

    self.generate_button("Auto-Align", self.root.destroy, bottom_button_label)
    self.generate_button("Cancel", self.root.destroy, bottom_button_label)


    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def generate_sub_title(self, frame, text = "Unnamed"):
    title_label = Label(
      frame, text=text,
      font=("Courier", 12),
      bg="#212121", fg="#bbb"
    )
    title_label.pack(side=TOP, pady=(20, 5))
    return title_label
  
  def generate_divider(self, frame):
    divider_frame = Frame(
      frame, bg="white",
      width=300, height=1
    )
    divider_frame.pack(side=TOP, pady=10)
    return divider_frame


  def generate_img(self, frame, img_tk):
    img_frame = Frame(
      frame,
      highlightthickness=1,
      highlightcolor="#fff"
    )
    img_frame.pack(side=TOP)
    img_label = Label(
      img_frame, bg="white",
      image=img_tk,
      borderwidth=0,
      width=250, height=250
    )
    img_label.image = img_tk
    img_label.pack(side=TOP)
    return img_label

  def start_capture_dw(self):
    self.back_frame.destroy()
    Capture(self.root, "dw")

  def start_extract_dw(self):
    self.root.destroy()
    Extract("dw")

  def start_capture_map(self):
    self.back_frame.destroy()
    Capture(self.root, "map")

  def start_extract_map(self):
    self.root.destroy()
    Extract("dw")

  def key_press(self, event):
    key_events = {
      27: self.root.destroy
    }
    try:
      key_events[event.keycode]()
    except:
      pass

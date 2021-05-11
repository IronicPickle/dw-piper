from os import path
from tkinter import Frame, Label, Checkbutton, LEFT, RIGHT, TOP, N, BooleanVar, StringVar

from PIL import Image, ImageTk

from src.extract import Extract
from src.capture import Capture

from src.menus.generate_menu import GenerateMenu

from src.lib import state_manager
from src.lib.tk_overlay import TkOverlay
from src.lib.variables import Env
from src.lib.img_utils import resize_img

class MainMenu(TkOverlay):

  def __init__(self, root = None):

    super().__init__(root)

    state = state_manager.get()
    self.auto_dw_source = BooleanVar()
    self.auto_dw_source.set(
      bool(state["auto_dw_source"]) if "auto_dw_source" in state else False
    )

    self.register_key_event(67, self.start_capture_dw) # C - Starts DW capture
    self.register_key_event(67, self.start_capture_map, "shift") # Shift + C - Starts map capture
    self.register_key_event(69, self.start_extract_dw) # E - Starts DW extract
    self.register_key_event(69, self.start_extract_map, "shift") # Shift + E - Starts map extract
    self.register_key_event(71, self.start_generate) # G - Starts pdf generator

    self.generate_frames()
    self.generate_header()
    self.generate_title("Choose an Option")

    self.resize(800, 800)

    self.source_frame = Frame(self.front_frame, bg=Env.bg)
    self.source_frame.pack(side=TOP, pady=(0, 20))

    self.left_frame = Frame(self.source_frame, bg=Env.bg)
    self.left_frame.pack(side=LEFT, anchor=N, padx=10)

    self.right_frame = Frame(self.source_frame, bg=Env.bg)
    self.right_frame.pack(side=RIGHT, anchor=N, padx=10)

    self.generate_sub_title(self.left_frame, "DW Source")
    self.generate_sub_title(self.right_frame, "Map Source")

    self.generate_divider(self.left_frame)
    self.generate_divider(self.right_frame)

    self.img_width = 300
    self.img_height = 300

    dw_img_path = path.join(Env.appdata_path, "images/dw_source.png")
    map_img_path = path.join(Env.appdata_path, "images/map_source.png")
    no_img_path = path.join(Env.index_dir, "images/no_image.png")
    auto_img_path = path.join(Env.index_dir, "images/auto_image.png")

    dw_img_pil = Image.open(dw_img_path) if path.exists(dw_img_path) else Image.open(no_img_path)
    map_img_pil = Image.open(map_img_path) if path.exists(map_img_path) else Image.open(no_img_path)
    auto_img_pil = Image.open(auto_img_path)

    dw_img_pil = resize_img(dw_img_pil, self.img_width, self.img_height)
    map_img_pil = resize_img(map_img_pil, self.img_width, self.img_height)
    auto_img_pil = resize_img(auto_img_pil, self.img_width, self.img_height)

    dw_img_tk = ImageTk.PhotoImage(dw_img_pil)
    map_img_tk = ImageTk.PhotoImage(map_img_pil)
    auto_img_tk = ImageTk.PhotoImage(auto_img_pil)

    left_img_frame, self.left_img_label = self.generate_img(self.left_frame, dw_img_tk)
    self.generate_img(self.right_frame, map_img_tk)

    self.auto_img_label = Label(
      left_img_frame,
      image=auto_img_tk,
      bg=Env.bg,
      borderwidth=0,
      width=self.img_width, height=self.img_height
    )
    self.auto_img_label.image = auto_img_tk

    self.generate_divider(self.left_frame)
    self.generate_divider(self.right_frame)

    left_button_label = Label(self.left_frame, bg=Env.bg)
    left_button_label.pack(side=TOP)

    right_button_label = Label(self.right_frame, bg=Env.bg)
    right_button_label.pack(side=TOP)

    self.left_button_capture = self.generate_button("Capture", self.start_capture_dw, left_button_label)
    self.left_button_extract = self.generate_button("Extract", self.start_extract_dw, left_button_label)

    self.update_dw_state()

    left_checkbox = Checkbutton(
      self.left_frame, text="Take DW Source from Screen",
      font=("Courier", 11),
      bg=Env.bg, fg=Env.fg,
      variable=self.auto_dw_source,
      command=self.auto_dw_source_change,
      activebackground=Env.bg,
      activeforeground=Env.fg,
      selectcolor=Env.bg
    )
    left_checkbox.pack(side=TOP, pady=(15, 0))

    self.generate_button("Capture", self.start_capture_map, right_button_label)
    self.generate_button("Extract", self.start_extract_map, right_button_label)

    self.generate_sub_title(self.front_frame, "Other Options")
    self.generate_divider(self.front_frame)

    bottom_button_label = Label(self.front_frame, bg=Env.bg)
    bottom_button_label.pack(side=TOP)

    self.generate_button("Auto-Align", self.root.destroy, bottom_button_label)
    self.generate_button("Generate", self.start_generate, bottom_button_label)
    self.generate_button("Cancel", self.root.destroy, bottom_button_label)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def generate_sub_title(self, frame, text = "Unnamed"):
    title_label = Label(
      frame, text=text,
      font=("Courier", 12),
      bg=Env.bg, fg=Env.fg
    )
    title_label.pack(side=TOP, pady=(20, 5))
    return title_label
  
  def generate_divider(self, frame):
    divider_frame = Frame(
      frame, bg=Env.div,
      width=350, height=1
    )
    divider_frame.pack(side=TOP, pady=10)
    return divider_frame


  def generate_img(self, frame, img_tk):
    img_frame = Frame(
      frame,
      highlightthickness=1,
      highlightbackground=Env.border,
      bg=Env.bg,
      width=self.img_width, height=self.img_height
    )
    img_frame.pack(side=TOP)
    img_label = Label(
      img_frame,
      image=img_tk,
      bg=Env.bg,
      borderwidth=0,
      width=self.img_width, height=self.img_height
    )
    img_label.image = img_tk
    img_label.pack(side=TOP)
    return img_frame, img_label

  def auto_dw_source_change(self):
    state_manager.update({ "auto_dw_source": self.auto_dw_source.get() })
    self.update_dw_state()

  def update_dw_state(self):
    auto_dw_source = self.auto_dw_source.get()
    state = "disabled" if auto_dw_source else "normal"
    self.left_button_capture.config(state = state)
    self.left_button_extract.config(state = state)
    self.left_img_label.pack_forget()
    self.auto_img_label.pack_forget()
    if not auto_dw_source:
      self.left_img_label.pack()
    else:
      self.auto_img_label.pack()

  def start_capture_dw(self):
    if self.auto_dw_source.get():
      return
    self.back_frame.destroy()
    Capture(self.root, "dw")

  def start_extract_dw(self):
    if self.auto_dw_source.get():
      return
    self.root.destroy()
    Extract("dw")

  def start_capture_map(self):
    self.back_frame.destroy()
    Capture(self.root, "map")

  def start_extract_map(self):
    self.root.destroy()
    Extract("map")

  def start_generate(self):
    self.back_frame.destroy()
    GenerateMenu(self.root)
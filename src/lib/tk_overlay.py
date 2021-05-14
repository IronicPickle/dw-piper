from os import path
from tkinter import Tk, Frame, TOP, LEFT, Label, Button

from PIL import Image, ImageTk
import win32api

from src.lib.tk_rightclick_menu import TkRightclickMenu
from src.lib.variables import Env

class TkOverlay:

  def __init__(self, root = None):
    
    self.root = Tk() if root is None else root
    self.log("Root > Started")

    self.cancelled = False

    self.root.attributes("-fullscreen", False)
    self.root.attributes("-alpha", 1)
    self.root.attributes("-topmost", True)
    self.root.title("Duct")
    self.root.iconbitmap(path.join(Env.index_dir, "images/icon.ico"))
    self.resize()

    self.back_frame = None
    self.front_frame = None

    self.title_frame = None
    self.title_icon = Image.open(path.join(Env.index_dir, "images/icon.ico")).resize((64, 64), Image.LANCZOS)
    self.title_icon_photoimage = ImageTk.PhotoImage(self.title_icon)
    self.title_icon_label = None
    self.title_label = None

    self.tk_rightclick_menu = None

    self.root.bind("<ButtonRelease-3>", self.generate_rightclick_menu)
    self.root.bind("<ButtonRelease-1>", lambda event: self.destroy_rightclick_menu())

    self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    self.root.bind("<Destroy>", self.on_destroy_static)
    self.root.bind("<Key>", lambda event: self.key_press(event))
    self.root.bind("<Control-Key>", lambda event: self.key_press(event, "ctrl"))
    self.root.bind("<Shift-Key>", lambda event: self.key_press(event, "shift"))

    self.key_events = {
      "none": { 27: self.root.destroy },
      "ctrl": {}, "shift": {}
    }

  def key_press(self, event, mod = "none"):
    print(f"Key Press: {mod} + {event.keycode}")
    if mod in self.key_events and event.keycode in self.key_events[mod]:
      self.key_events[mod][event.keycode]()

  def register_key_event(self, key, function, mod = "none"):
    if mod not in self.key_events:
      raise Exception(f"{mod} not a valid key modifier")
    self.key_events[mod][key] = function

  def on_close(self):
    self.cancelled = True
    self.root.destroy()

  def on_destroy_static(self, event):
    if event.widget is self.root:
      self.log("Root > Destroyed")
      self.on_destroy()
      self.back_frame.destroy()
    elif event.widget is self.back_frame:
      self.log("Back Frame > Destroyed")
      self.on_back_destroy()

  def on_destroy(self):
    pass

  def on_back_destroy(self):
    pass

  def resize(self, width = 250, height = 450):
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
    work_area = monitor_info["Work"]
    
    self.root.minsize(width, height)
    self.root.geometry('%dx%d+%d+%d' % (
      width, height,
      (work_area[2] / 2) - (width / 2),
      (work_area[3] / 2) - (height / 2)
    ))

  def log(self, text):
    print(f"{self.__class__.__name__} | {text}")

  def generate_rightclick_menu(self, event):
    self.destroy_rightclick_menu()
    self.tk_rightclick_menu = TkRightclickMenu(self.back_frame)

  def destroy_rightclick_menu(self):
    if self.tk_rightclick_menu:
      self.tk_rightclick_menu.destroy()

  def generate_frames(self):

    self.back_frame = Frame(self.root, bg=Env.bg)
    self.back_frame.pack(
      fill="both",
      expand=True
    )

    self.log("Back Frame > Started")

    self.front_frame = Frame(self.back_frame, bg=Env.bg)
    self.front_frame.place(anchor="center", relx=0.5, rely=0.5)

  def generate_header(self):

    if not self.front_frame:
      return

    self.title_frame = Frame(
      self.front_frame,
      bg=Env.bg
    )
    self.title_frame.pack(side=TOP)

    self.title_icon_label = Label(
      self.title_frame,
      image=self.title_icon_photoimage,
      bg=Env.bg,
      borderwidth=0
    )
    self.title_icon_label.pack(side=LEFT)

    self.title_label = Label(
      self.title_frame,
      text="Duct",
      font=("Courier", 20),
      pady=10,
      bg=Env.bg,
      fg=Env.fg
    )
    self.title_label.pack(side=LEFT, padx=(20, 0))

  def generate_title(self, title = "unnamed"):
    self.sub_title_label = Label(
      self.front_frame,
      text=title,
      font=("Courier", 16),
      pady=10,
      bg=Env.bg,
      fg=Env.fg
    )
    self.sub_title_label.pack(side=TOP)

    self.divider_frame = Frame(
      self.front_frame,
      bg=Env.div,
      width=120,
      height=1
    )
    self.divider_frame.pack(side=TOP, pady=(0, 10))

  def generate_button(self, name, command, frame):
    button = Button(
      frame, text=name,
      font=("Courier", 12),
      cursor="hand2",
      bd=0, bg=Env.bg, fg=Env.fg,
      command=command
    )
    button.pack(side=LEFT, padx=10)
    return button
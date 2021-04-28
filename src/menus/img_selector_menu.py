from tkinter import Label, Frame, TOP

from PIL import ImageTk

from src.lib.tk_overlay import TkOverlay

class ImgSelectorMenu(TkOverlay):
  def __init__(self, root = None, pil_imgs = []):
    super().__init__(root)

    if len(pil_imgs) == 0:
      return

    self.generate_frames()
    self.generate_header()
    self.generate_title("Choose an Image")

    self.resize(800, 800)

    self.root.bind("<Key>", self.key_press)

    self.cancelled = False

    self.img_frame = Frame(
      self.front_frame,
      highlightthickness=1,
      highlightcolor="#fff"
    )
    self.img_frame.pack(side=TOP, pady=10)

    self.current_img = 0

    self.pil_imgs = pil_imgs
    self.tk_imgs = []
    for i, pil_img in enumerate(pil_imgs):
      img_tk = ImageTk.PhotoImage(pil_img)
      self.tk_imgs.append(img_tk)

    self.total_imgs = len(self.tk_imgs)
    if self.total_imgs == 0:
      return

    self.img_label = Label(
      self.img_frame, bg="white",
      image=self.tk_imgs[self.current_img],
      borderwidth=0,
      width=300, height=300
    )
    self.img_label.image = img_tk
    self.img_label.pack(side=TOP)

    self.button_frame = Label(
      self.front_frame,
      bg="#212121"
    )
    self.button_frame.pack(side=TOP)

    self.generate_button("Previous", self.prev_img, self.button_frame)
    self.generate_button("Next", self.next_img, self.button_frame)
    self.generate_button("Select", self.select, self.button_frame)
    self.generate_button("Cancel", self.cancel, self.button_frame)

    self.root.after(1, self.root.focus_force)

    self.root.mainloop()

  def change_img(self, index):
    if index < 0:
      index = self.total_imgs - 1
    elif index > self.total_imgs - 1:
      index = 0

    img_tk = self.tk_imgs[index]
    self.img_label.config(image=img_tk)
    self.img_label.image = img_tk
    self.current_img = index

  def next_img(self):
    self.change_img(self.current_img + 1)

  def prev_img(self):
    self.change_img(self.current_img - 1)

  def select(self):
    self.selected_img_pil = self.pil_imgs[self.current_img]
    self.root.destroy()

  def cancel(self):
    self.cancelled = True
    self.root.destroy()

  def key_press(self, event):
    key_events = {
      27: self.cancel
    }
    try:
      key_events[event.keycode]()
    except:
      pass

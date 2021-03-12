from tkinter import Frame, TOP, RIGHT, BOTTOM, LEFT, X, Y

class TkResizer:

  def __init__(self, frame, on_resize, on_rotate):
    self.resizer_top_frame = Frame(frame, bg="#212121", height=10, cursor="exchange")
    self.resizer_top_frame.pack(side=TOP, fill=X)
    self.resizer_right_frame = Frame(frame, bg="#212121", width=10, cursor="exchange")
    self.resizer_right_frame.pack(side=RIGHT, fill=Y)
    self.resizer_bottom_frame = Frame(frame, bg="#212121", height=10, cursor="exchange")
    self.resizer_bottom_frame.pack(side=BOTTOM, fill=X)
    self.resizer_left_frame = Frame(frame, bg="#212121", width=10, cursor="exchange")
    self.resizer_left_frame.pack(side=LEFT, fill=Y)

    self.resizer_nw_frame = Frame(self.resizer_top_frame, bg="white", height=10, width=10, cursor="size_nw_se")
    self.resizer_nw_frame.pack(side=LEFT)
    self.resizer_ne_frame = Frame(self.resizer_top_frame, bg="white", height=10, width=10, cursor="size_ne_sw")
    self.resizer_ne_frame.pack(side=RIGHT)
    self.resizer_se_frame = Frame(self.resizer_right_frame, bg="white", height=10, width=10, cursor="size_nw_se")
    self.resizer_se_frame.pack(side=BOTTOM)
    self.resizer_sw_frame = Frame(self.resizer_bottom_frame, bg="white", height=10, width=10, cursor="size_ne_sw")
    self.resizer_sw_frame.pack(side=LEFT)

    self.resizer_nw_frame.bind("<B1-Motion>", lambda event: on_resize(event, "nw"))
    self.resizer_ne_frame.bind("<B1-Motion>", lambda event: on_resize(event, "ne"))
    self.resizer_se_frame.bind("<B1-Motion>", lambda event: on_resize(event, "se"))
    self.resizer_sw_frame.bind("<B1-Motion>", lambda event: on_resize(event, "sw"))

    self.resizer_top_frame.bind("<B1-Motion>", lambda event: on_rotate(event, "n"))
    self.resizer_right_frame.bind("<B1-Motion>", lambda event: on_rotate(event, "e"))
    self.resizer_bottom_frame.bind("<B1-Motion>", lambda event: on_rotate(event, "s"))
    self.resizer_left_frame.bind("<B1-Motion>", lambda event: on_rotate(event, "w"))

from tkinter import Frame, Button, TOP, INSERT, END

from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, CloseClipboard, GetClipboardData, CF_UNICODETEXT
from pyautogui import position

class TkRightclickMenu:
  def __init__(self, widget):

    self.should_place = False

    self.widget = widget

    self.menu_frame = Frame(
      widget,
      bg="#212121",
      padx=10,
      pady=10,
      highlightthickness=1,
      highlightbackground="white"
    )

    self.selected_widget = widget.winfo_containing(position()[0], position()[1])
    self.selected_widget_class = self.selected_widget.winfo_class()

    if self.selected_widget_class == "Entry":
      self.generate_button("Select", self.select)
      self.generate_button("Cut", self.cut)
      self.generate_button("Copy", self.copy)
      self.generate_button("Paste", self.paste)

    root_x = position()[0] - widget.winfo_rootx()
    root_y = position()[1] - widget.winfo_rooty()

    widget.update_idletasks()
    overflow_x = widget.winfo_width() - (root_x + self.menu_frame.winfo_reqwidth())
    overflow_y = widget.winfo_height() - (root_y + self.menu_frame.winfo_reqheight())
    if overflow_x < 0:
      root_x = widget.winfo_width() - self.menu_frame.winfo_reqwidth()
    if overflow_y < 0:
      root_y = widget.winfo_height() - self.menu_frame.winfo_reqheight()

    if self.should_place:
      self.menu_frame.place(
        x=root_x,
        y=root_y
      )

  def generate_button(self, name, command):
    self.should_place = True
    Button(
      self.menu_frame,
      text=name,
      font=("Courier", 12),
      command=command,
      cursor="hand2",
      bd=0,
      bg="#212121",
      fg="white"
    ).pack(side=TOP)

  def select(self):
    selected_widget = self.widget.focus_get()
    selected_widget.selection_range(0, END)

  def cut(self):
    self.copy()
    selected_widget = self.widget.focus_get()
    if selected_widget.selection_present():
      self.remove_selection(selected_widget)

  def copy(self):
    selected_widget = self.widget.focus_get()
    selection_text = ""
    if selected_widget.selection_present():
      selection_text = selected_widget.selection_get()

    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(selection_text)
    CloseClipboard()

  def paste(self):
    selected_widget = self.widget.focus_get()
    if selected_widget.selection_present():
      self.remove_selection(selected_widget)

    OpenClipboard()
    try:
      selected_widget.insert(INSERT, GetClipboardData(CF_UNICODETEXT))
    except:
      pass
    CloseClipboard()

  def remove_selection(self, widget):
    selection = (widget.index("sel.first"), widget.index("sel.last"))
    widget_string = widget.get()
    new_widget_string = widget_string[:selection[0]] + widget_string[selection[1]:]
    widget.delete(0, END)
    widget.insert(0, new_widget_string)
    widget.selection_clear()
    
  def destroy(self):
    self.menu_frame.destroy()

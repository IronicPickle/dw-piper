import sys
import tkinter as tk
import pyautogui
from win10toast import ToastNotifier
from capture import main as capture_main
from align import select as align_select

res = pyautogui.size()
toaster = ToastNotifier()

def main():
    
  root = tk.Tk()

  def cancel():
    root.destroy()

  def capture():
    cancel()
    capture_main(root)

  def align():
    cancel()
    align_select(root)

  def key_press(event):
    try:
      key_events[event.keycode]()
    except:
      pass

  key_events = {
    27: cancel,
    67: capture,
    65: align
  }

  root.bind("<Key>", key_press)

  root.attributes("-alpha", 0.75)
  root.attributes("-fullscreen", True)
  root.attributes("-topmost", True)
  root.config(bg="black")

  back_frame = tk.Frame(root, bg="black")
  back_frame.pack(
    fill="both",
    expand=True
  )

  front_frame = tk.Frame(back_frame, bg="black")
  front_frame.place(anchor="center", relx=0.5, rely=0.5)

  button_label = tk.Label(
    front_frame,
    text="Choose an Option",
    font=("Courier", 16),
    pady=10,
    bg="black",
    fg="white"
  )
  button_label.pack(side=tk.TOP)

  button_frame = tk.Label(
    front_frame,
    bg="black",
    fg="white"
  )
  button_frame.pack(side=tk.TOP)

  capture_button = tk.Button(
    button_frame,
    text="Capture",
    font=("Courier", 12),
    command=capture,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  capture_button.pack(side=tk.LEFT, padx=10)

  align_button = tk.Button(
    button_frame,
    text="Align",
    font=("Courier", 12),
    command=align,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  align_button.pack(side=tk.LEFT, padx=10)

  cancel_button = tk.Button(
    button_frame,
    text="Cancel",
    font=("Courier", 12),
    command=cancel,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  cancel_button.pack(side=tk.LEFT, padx=10)

  root.after(1, root.focus_force)
  root.mainloop()

if __name__ == "__main__": main()

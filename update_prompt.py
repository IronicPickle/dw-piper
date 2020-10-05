import sys
from os import path
import tkinter as tk
import pyautogui
import win32api

res = pyautogui.size()
index_dir = path.abspath(path.dirname(sys.argv[0]))

def main(latest_version, download_version):

  latest_version_number = latest_version["version"]

  print("Starting update prompt")

  root = tk.Tk()

  def destroy_root():
    root.destroy()

  def destroy_back_frame():
    back_frame.destroy()
    print("Destroyed update prompt")

  def update():
    button_label.config(text="Downloading update...")
    button_frame.destroy()
    button_label.update()
    download_version(latest_version["version"], on_download_finish)

  def on_download_finish():
    destroy_root()

  def cancel():
    destroy_root()

  def key_press(event):
    try:
      key_events[event.keycode]()
    except:
      pass

  key_events = {
    27: destroy_root
  }

  root.bind("<Key>", key_press)

  root.overrideredirect(1)

  monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
  work_area = monitor_info["Work"]

  root.attributes("-topmost", True)
  root.attributes("-alpha", 0.9)
  root.config(bg="black", highlightthickness=1, highlightbackground="white")
  root.minsize(450, 200)
  root.geometry('%dx%d+%d+%d' % (450, 200, work_area[2] - 450, work_area[3] - 200))
  root.title("DW Piper")
  root.iconbitmap(path.join(index_dir, "icon.ico"))

  back_frame = tk.Frame(root, bg="black")
  back_frame.pack(
    fill="both",
    expand=True
  )

  front_frame = tk.Frame(back_frame, bg="black")
  front_frame.place(anchor="center", relx=0.5, rely=0.5)

  title_label = tk.Label(
    front_frame,
    text="DW Piper",
    font=("Courier", 16, "underline"),
    bg="black",
    fg="white"
  )
  title_label.pack(side=tk.TOP)

  version_label = tk.Label(
    front_frame,
    text=f"Version: {latest_version_number}",
    font=("Courier", 12),
    bg="black",
    fg="white"
  )
  version_label.pack(side=tk.TOP, pady=(0, 5))

  button_label = tk.Label(
    front_frame,
    text=f"An update is available\nWould you like to install it?",
    font=("Courier", 16),
    bg="black",
    fg="white"
  )
  button_label.pack(side=tk.TOP, pady=10)

  button_frame = tk.Label(
    front_frame,
    bg="black",
    fg="white"
  )
  button_frame.pack(side=tk.TOP)

  update_button = tk.Button(
    button_frame,
    text="Update",
    font=("Courier", 12),
    command=update,
    cursor="hand2",
    bd=0,
    bg="black",
    fg="white"
  )
  update_button.pack(side=tk.LEFT, padx=10)

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
  print("Root destroyed")

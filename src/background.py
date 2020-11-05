from threading import Timer

import keyboard

from src import tk_overlay, main_menu
from src.tk_overlay import TkOverlay
from src.main_menu import MainMenu
from src.update_checker import compare_versions

class Background:

  def __init__(self):

    thread = Timer(5, lambda: self.update_check_scheduler(None))
    thread.start()

    keyboard.on_release(self.key_on_release)
    print("Listening for 'CTRL + ALT + D' or 'Print Screen' key release")
    keyboard.wait()

  def key_on_release(self, key):
    if key.name == "d" and keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl"):
      print("Detected 'CTRL + ALT + D' key release")
      MainMenu(TkOverlay())
    elif key.name == "print screen":
      print("Detected 'Print Screen' key release")
      MainMenu(TkOverlay())

  def update_check_scheduler(self, latest_version_known):
    print("Performing update check...")
    latest_version_known = compare_versions(latest_version_known)
    thread = Timer(60 * 15, lambda: self.update_check_scheduler(latest_version_known))
    thread.start()

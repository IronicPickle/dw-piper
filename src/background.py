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

    keyboard.on_release_key("print screen", self.key_print_screen)
    print("Listening for 'print screen' key release")
    keyboard.wait()

  def key_print_screen(self, key):
    if key.name == "print screen":
      print("Detected print screen")
      MainMenu(TkOverlay())

  def update_check_scheduler(self, latest_version_known):
    print("Performing update check...")
    latest_version_known = compare_versions(latest_version_known)
    thread = Timer(60 * 15, lambda: self.update_check_scheduler(latest_version_known))
    thread.start()

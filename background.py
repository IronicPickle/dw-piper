import sys
from os import path, getenv

import keyboard

from main_menu import main as main_menu_main

index_dir = path.abspath(path.dirname(sys.argv[0]))
appdata_path = path.join(getenv('APPDATA'), "DW-Piper")

def main():

  def key_print_screen(key):
    if key.name == "print screen":
      print("Detected print screen")
      main_menu_main()

  keyboard.on_release_key("print screen", key_print_screen)
  print("Listening for 'print screen' key release")
  keyboard.wait()

if __name__ == "__main__": main()

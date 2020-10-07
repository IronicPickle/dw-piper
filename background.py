import sys
from os import path

import keyboard
import zc.lockfile as lockfile

from main_menu import main as main_menu_main

index_dir = path.abspath(path.dirname(sys.argv[0]))

def main():

  try:
    lock = lockfile.LockFile(path.join(index_dir, "dw-background"))
  except lockfile.LockError:
    print("DW Piper Background already running")
    sys.exit()

  def key_print_screen(key):
    if key.name == "print screen":
      print("Detected print screen")
      main_menu_main()

  keyboard.on_release_key("print screen", key_print_screen)
  print("Listening for 'print screen' key release")
  keyboard.wait()
  lock.close()

if __name__ == "__main__": main()

from os import path
from threading import Timer
from subprocess import Popen

import keyboard
import zc.lockfile as lockfile
from win10toast import ToastNotifier

from src import variables, update_checker
from src.variables import Env
from src.update_checker import compare_versions

def main():

  try:
    lock = lockfile.LockFile(path.join(Env.appdata_path, "duct-background"))
  except lockfile.LockError:
    ToastNotifier().show_toast("Duct Background is already running",
      "You can only have one instance of Duct Background running at any time",
      icon_path=path.join(Env.index_dir, "images/icon.ico"),
      duration=3
    )
    return print("Duct Background is already running")

  thread = Timer(5, lambda: update_check_scheduler(None))
  thread.start()

  keyboard.on_release(key_on_release)
  print("Listening for 'CTRL + ALT + D' or 'Print Screen' key release")
  ToastNotifier().show_toast(f"Duct Background is now running",
    "You can now use either 'CTRL + ALT + D' or 'Print Screen' to summon the Duct interface",
    icon_path=path.join(Env.index_dir, "images/icon.ico"),
    duration=5,
    threaded=True
  )
  keyboard.wait()
  lock.close()

def key_on_release(key):
  if key.name == "d" and keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl"):
    print("Detected 'CTRL + ALT + D' key release")
    Popen(path.join(Env.index_dir, "Duct Background.exe"))
  elif key.name == "print screen":
    print("Detected 'Print Screen' key release")
    Popen(path.join(Env.index_dir, "Duct Background.exe"))

def update_check_scheduler(latest_version_known):
  print("Performing update check...")
  latest_version_known = compare_versions(latest_version_known)
  thread = Timer(60 * 15, lambda: update_check_scheduler(latest_version_known))
  thread.start()


if __name__ == "__main__": main()

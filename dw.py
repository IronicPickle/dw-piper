from os import path, mkdir
from sys import argv, exit
from threading import Timer

import zc.lockfile as lockfile

from src.tk_overlay import TkOverlay
from src.main_menu import MainMenu
from src.vars import Environment

def main():

  if not path.exists(Environment.appdata_path):
    mkdir(Environment.appdata_path)

  background_arg = 0
  try:
    background_arg = argv.index("--launch-background")
    try:
      lock = lockfile.LockFile(path.join(Environment.appdata_path, "dw-background"))
    except lockfile.LockError:
      print("DW Piper Background already running")
      exit()
    thread = Timer(5, lambda: update_check_scheduler(None))
    thread.start()
    background_main()
    lock.close()
  except:
    pass
  if background_arg > 0:
    exit()

  try:
    lock = lockfile.LockFile(path.join(Environment.appdata_path, "dw"))
  except lockfile.LockError:
    print("DW Piper already running")
    exit()


  MainMenu(TkOverlay())
  lock.close()

def update_check_scheduler(latest_version_known):
  print("Performing update check...")
  latest_version_known = compare_versions(latest_version_known)
  thread = Timer(60 * 15, lambda: update_check_scheduler(latest_version_known))
  thread.start()

if __name__ == "__main__": main()

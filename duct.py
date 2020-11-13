from os import path, mkdir
from sys import argv

import zc.lockfile as lockfile

from src.tk_overlay import TkOverlay
from src.main_menu import MainMenu
from src.background import Background
from src.variables import Env

def main():

  if not path.exists(Env.appdata_path):
    mkdir(Env.appdata_path)

  background_arg = 0
  try:
    background_arg = argv.index("--launch-background")
    try:
      lock = lockfile.LockFile(path.join(Env.appdata_path, "duct-background"))
    except lockfile.LockError:
      print("Duct Background already running")
      exit()
    Background()
    lock.close()
  except:
    pass
  if background_arg > 0:
    exit()

  try:
    lock = lockfile.LockFile(path.join(Env.appdata_path, "duct"))
  except lockfile.LockError:
    print("Duct already running")
    exit()


  MainMenu(TkOverlay())
  lock.close()

if __name__ == "__main__": main()

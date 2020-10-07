from os import path, getenv, mkdir
import sys, threading

import zc.lockfile as lockfile

from background import main as background_main
from main_menu import main as main_menu_main
from update_check import compare_versions as compare_versions

appdata_path = path.join(getenv('APPDATA'), "DW-Piper")

def main():

  if not path.exists(appdata_path):
    mkdir(appdata_path)

  background_arg = 0
  try:
    background_arg = sys.argv.index("--launch-background")
    try:
      lock = lockfile.LockFile(path.join(appdata_path, "dw-background"))
    except lockfile.LockError:
      print("DW Piper Background already running")
      sys.exit()
    thread = threading.Timer(5, lambda: update_check_scheduler(None))
    thread.start()
    background_main()
    lock.close()
  except:
    pass
  if background_arg > 0:
    sys.exit()

  try:
    lock = lockfile.LockFile(path.join(appdata_path, "dw"))
  except lockfile.LockError:
    print("DW Piper already running")
    sys.exit()
  main_menu_main()
  lock.close()

def update_check_scheduler(latest_version_known):
  print("Performing update check...")
  latest_version_known = compare_versions(latest_version_known)
  thread = threading.Timer(60 * 15, lambda: update_check_scheduler(latest_version_known))
  thread.start()

if __name__ == "__main__": main()

import sys, threading

from background import main as background_main
from main_menu import main as main_menu_main
from update_check import compare_versions as compare_versions

def main():

  background_arg = 0
  try:
    background_arg = sys.argv.index("--launch-background")
    thread = threading.Timer(5, lambda: update_check_scheduler(None))
    thread.start()
    background_main()
  except:
    pass
  if background_arg > 0:
    sys.exit()

  main_menu_main()

def update_check_scheduler(latest_version_known):
  print("Performing update check...")
  latest_version_known = compare_versions(latest_version_known)
  thread = threading.Timer(60 * 15, lambda: update_check_scheduler(latest_version_known))
  thread.start()

if __name__ == "__main__": main()

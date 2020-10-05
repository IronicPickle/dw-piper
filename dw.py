import sys, threading
from background import main as background_main
from menu import main as menu_main
from update_check import compare_versions as compare_versions

def main():

  background_arg = 0
  try:
    background_arg = sys.argv.index("--launch-background")
    thread = threading.Timer(30, update_check_scheduler)
    thread.start()
    background_main()
  except:
    pass
  if background_arg > 0:
    sys.exit()

  menu_main()

def update_check_scheduler():
  compare_versions()
  thread = threading.Timer(60 * 60, update_check_scheduler)
  thread.start()

if __name__ == "__main__": main()

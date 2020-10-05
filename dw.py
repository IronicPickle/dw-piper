import sys, threading
sys.path.append("./src")
from src.background import main as background_main
from src.menu import main as menu_main
from src.update_check import compare_versions as compare_versions

def main():

  background_arg = 0
  try:
    background_arg = sys.argv.index("--launch-background")
    thread = threading.Timer(30, compare_versions)
    thread.start()
    background_main()
  except:
    pass
  if background_arg > 0:
    sys.exit()

  menu_main()

if __name__ == "__main__": main()

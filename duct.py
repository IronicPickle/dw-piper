from os import path, mkdir
from sys import argv
import sys
import json

from urllib.parse import unquote
from urllib.request import urlopen
import requests

import zc.lockfile as lockfile
from win10toast import ToastNotifier

from src.tk_overlay import TkOverlay
from src.main_menu import MainMenu
from src.background import Background
from src.variables import Env
from src.upload import Upload
from src.form import Form

def duct_except_hook(exctype, value, traceback):
  crash_path = path.join(Env.appdata_path, "crash.txt")
  with open(crash_path, "w+") as file:
    file.write(str(value))
    file.close()
  sys.exit(0)
  return

def main():

  should_exit = handle_args(argv)
  if should_exit: sys.exit(0)

  if not path.exists(Env.appdata_path):
    mkdir(Env.appdata_path)

  try:
    lock = lockfile.LockFile(path.join(Env.appdata_path, "duct"))
  except lockfile.LockError:
    already_open_error("Duct")
    return print("Duct is already running")

  MainMenu(TkOverlay())
  lock.close()

def already_open_error(name):
  ToastNotifier().show_toast(f"{name} is already running",
    f"You can only have one instance of {name} running at any time",
    icon_path=path.join(Env.index_dir, "images/icon.ico"),
    duration=3
  )

def handle_args(args):
  
  if "--dev" not in args:
    sys.excepthook = duct_except_hook

  if "--parse-url" in args:

    index = args.index("--parse-url")
    try:
      param = args[index + 1]
    except:
      print("'parse-url' option must have a parsable url")
    parse_url(param)
    return True

  if "--launch-background" in args:

    try:
      lock = lockfile.LockFile(path.join(Env.appdata_path, "duct-background"))
    except lockfile.LockError:
      already_open_error("Duct Background")
      print("Duct Background is already running")
      return True
    Background()
    lock.close()

  return False

def parse_url(url):
  queries = ()
  try:
    protocol, path = url.split("://")
    if "?" in path:
      address, query_string = path.split("?")
      queries = query_string.split("&")
    else:
      address = path
  except:
    return print("'parse-url' could not parse url")

  if protocol != "duct":
    return print(f"'parse-url' protocol not found")
  if not protocols.keys().__contains__(address):
    return print(f"'parse-url' address not found")

  options = {}
  for query in queries:
    try:
      key, value = query.split("=")
      options[key] = unquote(value)
    except:
      continue

  protocols[address](options)

def upload(options):

  url = None
  ref = None
  if "url" in options: url = options["url"]
  if "ref" in options: ref = options["ref"]

  map_path = None
  if url: map_path = get_mapping(url)

  Upload(map_path, ref)

def get_mapping(url):
  map_path = path.join(Env.appdata_path, "mapping.pdf")
  try:
    with urlopen(url) as urlFile:
      with open(map_path, "w+") as file:
        file.write(urlFile.read().decode())
        file.close()
        return map_path
  except:
    print(f"Could not download mapping from: {url}")
    mapping_download_error(url)
    return None

def mapping_download_error(url):
  ToastNotifier().show_toast("Map download failed",
    f"Could not download mapping from: {url}",
    icon_path=path.join(Env.index_dir, "images/icon.ico"),
    duration=3,
    threaded=True
  )

def form(options):

  form_type = None
  data = None
  if "type" in options: form_type = options["type"]
  if "data" in options: data = options["data"]

  try:
    data = json.loads(data)
  except Exception:
    None

  Form(form_type, data)

protocols = {
  "upload/": upload,
  "form/": form
}


if __name__ == "__main__": main()

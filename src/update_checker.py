import sys
from os import path, getenv, remove
import subprocess
import json

import requests

from src import tk_overlay, update_prompt
from src.tk_overlay import TkOverlay
from src.update_prompt import UpdatePrompt

index_dir = path.abspath(path.dirname(sys.argv[0]))
appdata_path = path.join(getenv('APPDATA'), "DW-Piper")

def check_latest_version():

  url = "https://lykosgc.uk:81/api/latestVersion"

  try:
    res = requests.get(url, timeout=10)
  except:
    print("Update check failed")
    return None

  if res.status_code == 200:
    return json.loads(res.content)
  else:
    print(f"Response Error: {res.status_code}")

def compare_versions(latest_version_known):

  with open(path.join(index_dir, "version")) as version_file:
    current_version_int = version_to_int(version_file.read())
    version_file.close()

  latest_version = check_latest_version()
  if not latest_version:
    return

  if latest_version["versionInt"] > current_version_int:
    print("Update available")
    if latest_version_known == latest_version:
      print("Already notified user, skipping...")
      return latest_version
    changelog = get_changelog(latest_version["version"])["changelog"]
    print("Prompting user...")
    UpdatePrompt(TkOverlay(), latest_version, changelog, download_version)

  return latest_version

def version_to_int(version):
  version_parts = version.split(".")
  return int("".join(version_parts))

def get_changelog(version):

  url = f"https://lykosgc.uk:81/api/changelog?v={version}"

  try:
    res = requests.get(url, timeout=10)
  except:
    print("Changelog download failed")
    return None

  if res.status_code == 200:
    return json.loads(res.content)

  else:
    print(f"Response Error: {res.status_code}")

def download_version(version, download_finish_callback):

  url = f"https://lykosgc.uk:81/api/download?v={version}"

  try:
    res = requests.get(url, timeout=10)
  except:
    print("Update download failed")
    return None

  if res.status_code == 200:
    setup_path = path.join(appdata_path, "DW Piper Setup.exe")
    with open(setup_path, "wb") as file:
      file.write(res.content)
      file.close()
      download_finish_callback()
      subprocess.call(f"\"{setup_path}\"", shell=False)
      remove(setup_path)

  else:
    print(f"Response Error: {res.status_code}")

from os import getenv, path
from sys import argv

from pyautogui import size

class Env:
  appdata_path = path.join(getenv("APPDATA"), "Duct")
  index_dir = path.abspath(path.dirname(argv[0]))
  res_x = size()[0]
  res_y = size()[1]
  update_server_address = "https://update.lykos.uk/"
  bg="#212121"
  fg="#ffffff"
  div="#ffffff"
  border="#ffffff"

WATER_COMPANIES = {
  "United Utilities": {
    "drainage": {
      "combined": [0, 0, 255, 255],
      "foul": [0, 76, 115, 255],
      "surface": [137, 101, 68, 255],
      "overflow": [168, 0, 132, 255],
      "sludge": [0, 168, 112, 255]
    }, "clean": {
      "water_main": [235, 70, 0, 255],
      "comms": [255, 112, 0, 255],
      "trunk_main": [0, 0, 255, 255],
      "proposed": [122, 245, 165, 255],
      "concessionary": [255, 122, 0, 255],
      "water_meter": [214, 0, 11, 255],
      "commercial_meter": [214, 14, 0, 255]
    }
  }, "Wessex Water": {
    "drainage": {
      "combined": ([255, 0, 255, 255], [255, 200, 255, 255]),
      "foul": ([0, 0, 255, 255], [100, 100, 255, 255]),
      "surface": ([255, 112, 0, 255], [255, 165, 95, 255])
    }, "clean": {}
  }, "Bristol Water": {
    "drainage": {},
    "clean": {
      "water_main_1-meter_in_use": [255, 0, 0, 255],
      "water_main_2": [255, 255, 0, 255],
      "supply_pipe-private_main": [0, 0, 255, 255],
      "abandoned": [157, 157, 157, 255],
      "common_pipe": [245, 0, 122, 255],
      "hydrant": [0, 178, 0, 255],
      "fire_hydrant": [211, 0, 255, 255],
      "meter_not_in_use": [84, 0, 255, 255]
    }
  }
}
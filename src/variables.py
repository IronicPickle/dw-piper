from os import getenv, path
from sys import argv
import numpy as np

from pyautogui import size
import cv2

class Env:
  appdata_path = path.join(getenv("APPDATA"), "DW-Piper")
  index_dir = path.abspath(path.dirname(argv[0]))
  res_x = size()[0]
  res_y = size()[1]

class Bounds:
  united_utilities = {
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
      "water_meter": [214, 0, 11, 255]
    }
  }

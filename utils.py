import cv2
import numpy as np

def apply_mask(img, bgra_bound):
  mask = cv2.inRange(
    img,
    np.asarray(bgra_bound),
    np.asarray(bgra_bound)
  )
  return cv2.bitwise_and(
    img,
    img,
    mask=mask
  )
bgra_bounds = {
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

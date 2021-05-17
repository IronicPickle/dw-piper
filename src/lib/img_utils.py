import cv2
from PIL import Image

def crop_img(img_path, crop_x, crop_y, crop_dx, crop_dy):
  map_img = cv2.imread(img_path)
  map_img = map_img[crop_x:crop_dx, crop_y:crop_dy]
  cv2.imwrite(img_path, map_img)

def calculate_dims(img_pil, width, height, mode = "fit"):
  initial_width, initial_height = img_pil.size
  new_width, new_height = ( width, height )

  initial_ratio = initial_width / initial_height
  new_ratio = new_width / new_height
  if mode == "fit": # Resizes an image to fit within the given boundary (args: width & height)
    if initial_ratio > 1: # Initial width is greater than height, so new height is scaled
      new_height = new_width / initial_ratio
    elif initial_ratio < 1: # Initial height is greater than width, so new width is scaled
      new_width = new_height * initial_ratio
    else: # Initial width and height are equal, so new the smallest of the new values are used
      if new_ratio > 1: # New height is smaller, so it's used
        new_width = new_height
      elif new_ratio < 1: # New width is smaller, so it's used
        new_height = new_width
  
  return int(new_width), int(new_height)

def resize_img(img_pil, width, height):
  return img_pil.resize(( int(width), int(height) ), Image.LANCZOS)

def rotate_img(img_pil, rotation):
  return img_pil.rotate(rotation, Image.BILINEAR, expand=True)

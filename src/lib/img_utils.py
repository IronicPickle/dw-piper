import cv2
from PIL import Image

def crop_img(img_path, crop_x, crop_y, crop_dx, crop_dy):
  map_img = cv2.imread(img_path)
  map_img = map_img[crop_x:crop_dx, crop_y:crop_dy]
  cv2.imwrite(img_path, map_img)

def resize_img(img_pil, width, height, mode = "fit"):
  initial_width, initial_height = img_pil.size

  ratio = initial_width / initial_height
  new_ratio = width / height
  print(ratio, new_ratio)

  new_width, new_height = ( width, height )
  if mode == "fit":
    if ratio > 1:
      new_height = new_height / ratio
    elif ratio < 1:
      new_width = new_width * ratio
  
  return img_pil.resize(( int(new_width), int(new_height) ), Image.LANCZOS)

def rotate_img(img_pil, rotation):
  return img_pil.rotate(rotation, Image.BILINEAR, expand=True)

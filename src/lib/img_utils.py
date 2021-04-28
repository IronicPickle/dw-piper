import cv2
from PIL import Image

def crop_img(img_path, crop_x, crop_y, crop_dx, crop_dy):
  map_img = cv2.imread(img_path)
  map_img = map_img[crop_x:crop_dx, crop_y:crop_dy]
  cv2.imwrite(img_path, map_img)

def resize_img(img_pil, width, height, mode = "cover"):
  initial_width, initial_height = img_pil.size

  ratio = initial_width / initial_height

  new_width, new_height = ( width, height )
  if mode == "cover":
    if initial_width > initial_height:
      new_height = int(new_height / ratio)
    elif initial_height > initial_width:
      new_width = int(new_width * ratio)
  
  return img_pil.resize(( int(new_width), int(new_height) ), Image.LANCZOS)
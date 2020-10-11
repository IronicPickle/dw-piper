import cv2

def crop_img(img_path, crop_x, crop_y, crop_dx, crop_dy):
  map_img = cv2.imread(img_path)
  map_img = map_img[crop_x:crop_dx, crop_y:crop_dy]
  cv2.imwrite(img_path, map_img)

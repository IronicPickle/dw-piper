import fitz
import cv2


def extract_map_img(pdf_path):

  try:
    pdf = fitz.open(pdf_path)
    map_pix = fitz.Pixmap(pdf, 16)
    return map_pix
  except:
    return False

def reprocess_map_img(img_path):
  map_img = cv2.imread(img_path)
  height, width, channels = map_img.shape
  map_img = map_img[1:height, 1:width]
  cv2.imwrite(img_path, map_img)


def insert_map_img(template_path, map_img_path, copyright_img_path):

  pdf_template = fitz.open(template_path)
  x, y, size = 60, 46, 472
  map_rect = fitz.Rect(x, y, x + size, y + size)


  x, y, width, height = x, y + size - 8, 210, 9
  copyright_rect = fitz.Rect(x, y, x + width, y + height)

  for page in pdf_template:
    page.insertImage(map_rect, filename=map_img_path)
    page.insertImage(copyright_rect, filename=copyright_img_path)

  return pdf_template

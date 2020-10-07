import fitz


def extract_map_img(pdf_path):

  try:
    pdf = fitz.open(pdf_path)
    map_pix = fitz.Pixmap(pdf, 16)
    return map_pix
  except:
    return False

def insert_map_img(template_path, img_path):

  pdf_template = fitz.open(template_path)
  x, y, size = 60, 46, 472
  rectangle = fitz.Rect(x, y, x + size, y + size)

  for page in pdf_template:
    page.insertImage(rectangle, filename=img_path)

  return pdf_template

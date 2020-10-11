import fitz

class PdfProcessor:

  def __init__(self, pdf_path):
    self.pdf = fitz.open(pdf_path)

  def extract_img(self, xref):
    try:
      map_pix = fitz.Pixmap(self.pdf, xref)
      return map_pix
    except:
      return False

  def insert_img(self, img_path, rect_dims, page_no):
    map_rect = fitz.Rect((
      rect_dims[0], rect_dims[1],
      rect_dims[2] + rect_dims[0],
      rect_dims[3] + rect_dims[1]
    ))

    self.pdf[page_no].insertImage(map_rect, filename=img_path)

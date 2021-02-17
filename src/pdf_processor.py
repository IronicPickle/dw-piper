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

  def find_text(self, text, page_no=0, index=0):
    rects = self.pdf[page_no].searchFor(text)
    try:
      return rects[index]
    except Exception:
      return None
  def insert_text(self, text, point, page_no=0, fontsize=8):

    self.pdf[page_no].insertText(point, text, fontsize=fontsize)

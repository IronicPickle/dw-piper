import tkinter as tk
from tkinter import filedialog as fd
import fitz
from pathlib import Path

def replace_img(template_path, img_path, pipe_type):
  pdf_template = fitz.open(template_path)
  x, y, size = 60, 46, 472
  rectangle = fitz.Rect(x, y, x + size, y + size)

  for page in pdf_template:
    page.insertImage(rectangle, filename=img_path)

  root = tk.Tk()
  root.withdraw()

  def open_file_dialog():
    output_path = fd.asksaveasfilename(
      initialdir="/",
      title=f"Save {pipe_type} PDF file",
      filetypes=[("PDF File", "*.pdf")],
      defaultextension=".pdf",
      initialfile="CC" if pipe_type == "clean" else "DD"
    )
    root.destroy()

    pdf_template.save(output_path)

  root.after(1, open_file_dialog)
  root.mainloop()

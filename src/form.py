from os import path
from datetime import datetime

from win10toast import ToastNotifier

from src import variables, pdf_processor, state_manager, img_utils
from src.variables import Env
from src.pdf_processor import PdfProcessor
from src.tk_overlay import TkOverlay

class Form:

  def __init__(self, form_type=None, data=None):

    if not form_type:
      return None

    if not data:
      return None

    if form_type == "con29r":
      self.generate_con29r(data)

  def generate_con29r(self, data):

    pdf_path = path.join(Env.index_dir, f"pdf_templates/con29r_template.pdf")
    pdf_process = PdfProcessor(pdf_path)

    fields = (
      { "document_id": "Search No:", "value": data["reference"], "location": "after" },
      { "document_id": "Dated:", "value": datetime.today().strftime("%d/%m/%Y"), "location": "after" },

      { "document_id": "Local Authority Name and Address", "value": data["council"], "location": "below" },

      { "document_id": "Address of Land/Property", "value": self.format_address(data["property"]), "location": "below" },
      { "document_id": "UPRN:", "value": data["property"]["uprn"], "location": "below" }
    )

    self.insert_fields(fields, pdf_process)

    save_dir = f"C:/Users/test/Desktop/CON29R {data['reference']}.pdf"
    pdf_process.pdf.save(save_dir, deflate=True)
    self.form_generated_notification("Con29R", save_dir)

  address_keys = (
    "flatNumber", "houseName", "houseNumber", "street", "addressLine2", "locality", "town", "county", "postCode"
  )

  def insert_fields(self, fields, pdf_process):
    for _, field in enumerate(fields):
      document_id = field["document_id"]
      value = field["value"].upper()
      location = field["location"]

      rect = pdf_process.find_text(document_id)
      if rect is None:
        continue

      point = ( rect.x1 + 2, rect.y1 - 3 )
      if location == "below":
        point = ( rect.x0, rect.y1 + rect.height - 5 )

      pdf_process.insert_text(value, point)

  def format_address(self, propertyInfo):
    address = ""
    for _, address_key in enumerate(self.address_keys):
      value = propertyInfo[address_key]
      if(len(value) > 0):
        if(("flatNumber", "houseName", "houseNumber", "street").__contains__(address_key)):
          address += f"{value} "
        else:
          address += f"{value},\n"

    return address[:-3]

  def form_generated_notification(self, form_type, save_dir):
    ToastNotifier().show_toast(f"Generated {form_type} Form",
      save_dir,
      icon_path=path.join(Env.index_dir, "images/icon.ico"),
      duration=3
    )

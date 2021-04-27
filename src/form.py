from os import path
from datetime import datetime
from tkinter import Tk, filedialog

from win10toast import ToastNotifier
import fitz

from src.menus.con29r_menu import Con29RMenu
from src.menus.confirm_menu import ConfirmMenu

from src.lib.variables import Env
from src.lib.pdf_processor import PdfProcessor
from src.lib.tk_overlay import TkOverlay

class Form:

  def __init__(self, form_type=None, data=None):

    if not form_type:
      return None

    if not data:
      return None

    self.form_type = form_type
    self.data = data

    confirm_menu = ConfirmMenu(TkOverlay(), f"Generate {form_type.upper()} Form")
    if confirm_menu.cancelled: return None

    if form_type == "con29r":
      street = data["property"]["street"]
      form_menu = Con29RMenu(TkOverlay(), street)
      if form_menu.cancelled: return None
      roads = (
        form_menu.road1.get(),
        form_menu.road2.get(),
        form_menu.road3.get()
      )
      self.generate_con29r(roads)
    elif form_type == "llc1":
      self.generate_llc1()
    elif form_type == "con29o":
      self.generate_con29o()
      

  def generate_con29r(self, roads):

    pdf_path = path.join(Env.index_dir, "pdf_templates/con29r_template.pdf")
    self.PdfProcess = PdfProcessor(pdf_path)

    data = self.data

    uprn = data["property"]["uprn"]
    if uprn == "Not validated": uprn = ""

    fields = (
      { "document_id": "Reference:", "value": f"  {data['reference']}", "location": "after" },
      { "document_id": "Dated:", "value": f"  {datetime.today().strftime('%d/%m/%Y')}", "location": "after", "index": 1 },

      { "document_id": "Local Authority Name and Address", "value": self.get_spliced_council_name(), "location": "below" },

      { "document_id": "Address of Land/Property", "value": self.format_address(data["property"]), "location": "below" },
      { "document_id": "UPRN:", "value": uprn, "location": "below" },
      { "document_id": "enquiries 2.1 & 3.6 are required (max 3)", "value": "\n".join(roads), "location": "below" }
    )

    self.insert_fields(fields, "con29r", self.PdfProcess)

    self.save_pdf()

  def generate_llc1(self):

    pdf_path = path.join(Env.index_dir, "pdf_templates/llc1_template.pdf")
    self.PdfProcess = PdfProcessor(pdf_path)

    data = self.data

    fields = (
      { "document_id": "Reference:", "value": f"  {data['reference']}", "location": "after" },
      { "document_id": "Date:", "value": f"  {datetime.today().strftime('%d/%m/%Y')}", "location": "after" },

      { "document_id": "Insert name and address of registering authority in space below", "value": self.get_spliced_council_name(), "location": "below" },

      { "document_id": "Description of land sufficient to enable it to be identified.", "value": self.format_address(data["property"]), "location": "below" }
    )

    self.insert_fields(fields, "llc1", self.PdfProcess)

    self.save_pdf()
      
  def generate_con29o(self):

    pdf_path = path.join(Env.index_dir, "pdf_templates/con29o_template.pdf")
    self.PdfProcess = PdfProcessor(pdf_path)

    data = self.data

    fields = [
      { "document_id": "Reference:", "value": f"        {data['reference']}", "location": "after" },
      { "document_id": "Dated:", "value": f"               {datetime.today().strftime('%d/%m/%Y')}", "location": "after", "index": 1 },

      { "document_id": "Local authority name and address:", "value": self.get_spliced_council_name(), "location": "below" },

      { "document_id": "Address of the land/property:", "value": self.format_address(data["property"]), "location": "below" }
    ]

    for _, enquiry in enumerate(data["enquiries"]):
      fields.append({
        "document_id": f"{enquiry}.", "value": "X     ", "location": "before"
      })

    self.insert_fields(fields, "con29o", self.PdfProcess)

    self.save_pdf()

  def get_spliced_council_name(self):
    name = self.data["council"]
    if name.lower().__contains__("(formerly"):
      index = name.index("(formerly")
      name = name[0:index]
    return name

  def save_pdf(self):
    save_dir = self.prompt_user_to_save()
    if len(save_dir) == 0: return None
    self.PdfProcess.pdf.save(save_dir, deflate=True)
    self.form_generated_notification(self.form_type.upper(), save_dir)

  def prompt_user_to_save(self):

    root = Tk()
    root.withdraw()

    output_path = None

    def open_prompt():
      nonlocal output_path

      output_path = filedialog.asksaveasfilename(
        parent=root,
        title=f"Save {self.form_type.upper()} PDF file",
        filetypes=[("PDF File", "*.pdf")],
        defaultextension=".pdf",
        initialfile=f"{self.data['reference']} {self.form_type.upper()}"
      )

    open_prompt()

    return output_path

  address_keys = (
    "flatNumber", "houseName", "houseNumber", "street", "addressLine2", "locality", "town", "county", "postCode"
  )

  def insert_fields(self, fields, form_type, PdfProcess):
    for _, field in enumerate(fields):
      document_id = field["document_id"]
      value = field["value"].upper()
      location = field["location"]
      index = field["index"] if "index" in field else 0

      rect = PdfProcess.find_text(document_id, index=index)

      if rect is None:
        continue

      max_width = 0
      if form_type == "con29r":
        max_width = 200
      elif form_type == "llc1":
        max_width = 200
      elif form_type == "con29o":
        max_width = 175
      
      point = ( rect.x1 + 2, rect.y0 )
      if location == "below":
        point = ( rect.x0, rect.y0 + rect.height )
      elif location == "before":
        text_length = fitz.getTextlength(value, fontsize=9)
        point = ( rect.x1 - rect.width - text_length, rect.y0 - 1 )

      rect = fitz.Rect(point[0], point[1], point[0] + max_width, point[1] + 200)
      PdfProcess.insert_textbox(value, rect, fontsize=9)

  def format_address(self, propertyInfo):
    address = ""
    for _, address_key in enumerate(self.address_keys):
      value = propertyInfo[address_key]
      if(len(value) > 0):
        if(("flatNumber", "houseName", "houseNumber").__contains__(address_key)):
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

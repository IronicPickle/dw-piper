from tkinter import Tk, filedialog

class FilePrompt:
  def __init__(self, after_function):
    self.root = Tk()
    self.root.withdraw()
    self.root.after(1, after_function)
    
class FilePromptOpen(FilePrompt):
  def __init__(self, initial_dir = "/", title = "Unnamed"):
    super().__init__(self.open_file_prompt)

    self.initial_dir = initial_dir
    self.title = title
    self.path = None
    self.root.mainloop()

  def open_file_prompt(self):
    self.path = filedialog.askopenfilename(
      parent=self.root,
      initialdir=self.initial_dir,
      title=self.title,
      filetypes=[("PDF File", "*.pdf")],
      defaultextension=".pdf"
    )
    self.root.destroy()


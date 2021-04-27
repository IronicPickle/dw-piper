from tkinter import Tk, filedialog

class FilePrompt:
  def __init__(self, after_function):
    self.root = Tk()
    self.root.withdraw()
    self.root.after(1, after_function)
    
class FilePromptOpen(FilePrompt):
  def __init__(self, title = "Unnamed", initial_dir = "/", file_types = []):
    super().__init__(self.open_file_prompt)

    self.title = title
    self.initial_dir = initial_dir
    self.file_types = file_types

    self.path = None
    self.root.mainloop()

  def open_file_prompt(self):
    self.path = filedialog.askopenfilename(
      parent=self.root,
      title=self.title,
      initialdir=self.initial_dir,
      filetypes=self.file_types
    )
    self.root.destroy()

class FilePromptSave(FilePrompt):
  def __init__(self, title = "Unnamed", initial_dir = "/", file_types = [],
    file_extension = "", initial_file = "Unnamed"):

    super().__init__(self.open_file_prompt)

    self.title = title
    self.initial_dir = initial_dir
    self.file_types = file_types
    self.file_extension = file_extension
    self.initial_file = initial_file

    self.path = None
    self.root.mainloop()

  def open_file_prompt(self):
    self.path = filedialog.asksaveasfilename(
      parent=self.root,
      title=self.title,
      initialdir=self.initial_dir,
      filetypes=self.file_types,
      defaultextension=self.file_extension,
      initialfile=self.initial_file
    )
    self.root.destroy()
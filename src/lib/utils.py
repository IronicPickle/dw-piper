from os import path

from win10toast import ToastNotifier

from src.lib.variables import Env

notifier = ToastNotifier()

class Utils:

  def send_toast(title, sub_title, duration = 3, threaded = True):
    notifier.show_toast(title,
      sub_title,
      icon_path=path.join(Env.index_dir, "images/icon.ico"),
      duration=3,
      threaded=threaded
    )

  
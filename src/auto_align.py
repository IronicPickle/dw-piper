import cv2
import numpy as np

def auto_align(img, template, move_x, move_y, resize, root, callback):

  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

  img_w, img_h = img.shape

  largest_bound = img_w if (img_w < img_h) else img_h
  template = cv2.resize(template, (largest_bound, largest_bound), cv2.INTER_CUBIC)

  template_w, template_h = template.shape

  def loop(i, img, template, best_result=( 0, 0, None, None )):
    i -= 5
    if(i < 300): return callback()

    print(f"Performing match at: ({i} x {i})")
    result = align(img, cv2.resize(template, (i, i), cv2.INTER_AREA))
    if(result[0] > best_result[0]):
      best_result = result

      move_x(result[1][0] - 1)
      move_y(result[1][1] - 1)
      resize(i, True)
    
    root.after(1, lambda: loop(i, img, template, best_result))
  
  loop(template_w, img, template)

def align(img, template):

  img = img.copy()
  method = cv2.TM_CCOEFF

  # Apply template Matching
  res = cv2.matchTemplate(img,template,method)
  _, max_val, _, max_loc = cv2.minMaxLoc(res)

  return ( max_val, max_loc, img, template )
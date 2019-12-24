import cv2
import os
from gnutools.utils import listfiles, name, parent
import numpy as np

__NEXT_CASE__ = 82
__PREVIOUS_IMG__ = 81
__VALIDATE_IMG__ = 13
__NEXT_IMG__ = 83
__PREVIOUS_CASE__ = 84

def process_dir(dir):
   def reload_annotations(dir, imgs, ann_file='annotation.txt'):
      try:
         assert os.path.exists(ann_file)
         my_case = name(dir)
         lines = open(ann_file, 'r').readlines()[::-1]
         lines = [line.split('\n')[0] for line in lines]
         for line in lines:
            case, img = line.split(",")
            if case==my_case:
               return int(np.argwhere(imgs==img).reshape(-1, )[0]), True
         return 0, False
      except AssertionError:
         return 0, False

   def print_validate(img):
      img[:10] = [0, 255, 0]
      img[-10:] = [0, 255, 0]
      img[:, :10] = [0, 255, 0]
      img[:, -10:] = [0, 255, 0]
      return img

   imgs = np.array(listfiles(dir))
   indices = [int(name(img).split('_')[0]) for img in imgs]
   imgs = imgs[np.argsort(indices)]
   k, validated = reload_annotations(dir, imgs)
   print(validated, dir)
   while True:
      img = cv2.imread(imgs[k])
      img = print_validate(img) if validated else img
      cv2.imshow("", img)
      key = cv2.waitKey()
      if key == __VALIDATE_IMG__:
         img = print_validate(img)
         cv2.imshow("", img)
         key = cv2.waitKey()
         if key == __VALIDATE_IMG__:
            return __VALIDATE_IMG__, imgs[k]
         else:
            validated=False
      elif key == __NEXT_IMG__:
         k = k + 1
         if k == len(imgs):
            k = 0
         validated = False
      elif key == __PREVIOUS_IMG__:
         k = k-1
         if k<0:
            k = len(imgs)-1
         validated = False
      elif key == __NEXT_CASE__:
         return __NEXT_CASE__, None
      elif key == __PREVIOUS_CASE__:
         return __PREVIOUS_CASE__, None

if __name__ == '__main__':
   root = '/mnt/miniIYOProjects/MITSUI/mitsui-prepare/imgs'
   cases = os.listdir(root)
   k = 0
   while True:
      result, img = process_dir(os.path.join(root, cases[k]))
      if result == __PREVIOUS_CASE__:
         k=k-1
         if k<0:
            k = len(cases)-1
      elif result==__NEXT_CASE__:
         k = k + 1
         if k == len(cases):
            print('finished')
            break
      else:
         with open('annotation.txt', 'a') as f:
            f.write(",".join([name(parent(img)), img]) + '\n')
         print(img,' is validated')
         k = k + 1
         if k == len(cases):
            k = 0


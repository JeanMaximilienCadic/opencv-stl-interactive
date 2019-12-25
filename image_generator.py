from gnutools.utils import listfiles, name
import cv2
import numpy as np
from iyo.cad import NMesh
from math import pi

class ImageGenerator(dict):
    def __init__(self, root):
        super(ImageGenerator, self).__init__()
        # Load the files
        files = dict([(name(file).split('_')[0], file) for file in listfiles(root)])
        prepa = NMesh(files['preparationscan'])
        crown = NMesh(files['crown'])
        # Set the color
        prepa.set_color([0, 200, 200])
        crown.set_color([255, 255, 0])
        setmesh = NMesh(list=[crown, prepa])
        _img = setmesh.shot()
        img_master = np.zeros((800, 800, 3), np.uint8)
        img_master[200:-200, 200:-200] = 255 - _img
        shape = img_master.shape
        for theta in np.arange(0, 2*pi, 2*pi / 360):
            deg = int((theta / pi) * 180)
            img = self.rotateImage(img_master, deg)
            img[shape[0] // 2:, :] = cv2.flip(img[shape[0] // 2:, :], 0)
            img[shape[0] // 2:, :] = cv2.flip(img[shape[0] // 2:, :], 0)
            self.setdefault('{root}/{deg}_None.None'.format(root=root, deg=str(deg).zfill(3)), img)

    @staticmethod
    def rotateImage(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

if __name__=='__main__':
    for img_path, img in ImageGenerator('/mnt/9DWNas-02/MITSUI/crown/crown_valid_dataset/2019/USB3/test000252').items():
        cv2.imshow('', img)
        cv2.waitKey(10)
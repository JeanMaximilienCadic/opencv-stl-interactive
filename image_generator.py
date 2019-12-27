from gnutools.utils import listfiles, name
import cv2
import numpy as np
from iyo.cad import NMesh
from math import pi

class ImageGenerator(dict):
    def __init__(self, root):
        super(ImageGenerator, self).__init__()
        def add_text(string, img):
            font = cv2.FONT_HERSHEY_SIMPLEX
            # org
            org = (50, 50)
            # fontScale
            fontScale = 1
            # Blue color in BGR
            color = (255, 255, 255)
            # Line thickness of 2 px
            thickness = 2
            # Using cv2.putText() method
            return cv2.putText(img, string, org, font, fontScale, color, thickness, cv2.LINE_AA)
        # Load the files
        self.files = dict([(name(file), file) for file in listfiles(root)])
        setmesh = NMesh(self.files['model'])
        # Set the color
        setmesh.set_color([0, 200, 200])

        _img0 = setmesh.shot()
        setmesh.rotate(axis_rotation=0, theta=pi)
        _img1 = setmesh.shot()
        _img1 = cv2.flip(_img1, 0)
        img_master0 = np.zeros((800, 800, 3), np.uint8)
        img_master0[200:-200, 200:-200] = 255 - _img0
        img_master1 = np.zeros((800, 800, 3), np.uint8)
        img_master1[200:-200, 200:-200] = 255 - _img1

        for theta in np.arange(0, 2*pi, 2*pi / 360):
            deg = int((theta / pi) * 180)
            img0 = self.rotateImage(img_master0, deg)
            img0 = add_text(name(root), img0)
            img1 = self.rotateImage(img_master1, deg)
            img = np.zeros((800, 1600, 3), np.uint8)
            img[:, :800] = img0
            img[:, 800:] = img1
            self.setdefault('{root}/{deg}_None.None'.format(root=root, deg=str(deg).zfill(3)), img)

    def export(self, img, plyfile):
        # Load the files
        setmesh = NMesh(self.files['model'])
        setmesh.set_color([0, 200, 200])
        # Set the color
        deg = int(name(img).split("_")[0])
        theta = (deg/360)*2*pi
        setmesh.rotate(axis_rotation=2, theta=theta)
        setmesh.export(plyfile)

    @staticmethod
    def rotateImage(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

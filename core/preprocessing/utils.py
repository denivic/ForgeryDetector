import cv2
from matplotlib import pyplot as plt


class ImageUtilities():
    def __init__(self):
        pass

    def load(self, path: str, flag=None):
        """Loads an image.

        Args:
            path (str): The path to the image.
            flag (int): How to load the image. See below.

        Returns:
            Image.

        Flags:
            - cv2.IMREAD_COLOR: It specifies to load a color image. Any transparency of image will be
            neglected. It is the default flag. Alternatively, we can pass integer value 1 for this flag.
            - cv2.IMREAD_GRAYSCALE: It specifies to load an image in grayscale mode. Alternatively, we
            can pass integer value 0 for this flag.
            - cv2.IMREAD_UNCHANGED: It specifies to load an image as such including alpha channel.
            Alternatively, we can pass integer value -1 for this flag.
        """
        if flag is None:
            flag = 1

        return cv2.imread(path, flag)

    def save(self, image, path):
        """Saves an image.

        Args:
            img (numpy.ndarray): The image to be saved.
            path (str): The path of the image to be saved.
        """
        cv2.imwrite(f'{path}.png', image)

    def showcv(self, image, img_desc=None):
        """Shows the given image using OpenCV.

        Args:
            img (numpy.ndarray): The image to be shown
            img_desc (str, optional): A description of the image. Defaults to None.
        """
        if img_desc is None:
            cv2.imshow('', image)
        else:
            cv2.imshow(img_desc, image)

        cv2.waitKey(0)
        cv2.destroyAllWindows

    def show(self, image):
        """Shows the image using PyPlot.

        Args:
            image (numpy.ndarray): The image to show.
        """
        plt.imshow(image)
        plt.show()

import cv2


class ImageUtilities():
    def __init__(self):
        pass

    def load_image(self, path: str, flag: int = None):
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

        return cv2.imread(path, flag), path.split('\\')[-1][:-4]

    def save_image(self, img, path):
        cv2.imwrite(f'{path}.png', img)

    def show_image(self, img, img_desc: str = None) -> None:
        if img_desc is None:
            cv2.imshow('', img)
        else:
            cv2.imshow(img_desc, img)

        cv2.waitKey(0)
        cv2.destroyAllWindows

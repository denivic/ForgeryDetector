import cv2


class ImageUtilities():
    def __init__(self):
        pass

    def load_image(self, path):
        return cv2.imread(path), path.split('\\')[-1][:-3]

    def save_image(self, img, path):
        cv2.imwrite(f'{path}.png', img)

    def show_image(self, img, img_desc: str = None) -> None:
        if img_desc is None:
            cv2.imshow('', img)
        else:
            cv2.imshow(img_desc, img)

        cv2.waitKey(0)
        cv2.destroyAllWindows

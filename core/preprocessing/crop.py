import cv2
import numpy as np
import typing


class ImageCropper():
    def __init__(self):
        pass

    def crop_rectangle(self, img, bands: int, rec_width: int) -> typing.Any:
        results = []
        step_value = round((img.shape[0] / 8)) + 72

        for columns in range(0, img.shape[1], step_value):
            results.append(img[:, columns:columns + rec_width, :])

        return results

    def find_contours(self, img):
        if img is None:
            print('No image has been loaded.')
            return 0

        # Converting to grayscale is necessary for finding the contours
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray_img, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        rect_contours = []
        for cont in contours:
            x_max, y_max = np.max(cont, axis=0)[0]
            x_min, y_min = np.min(cont, axis=0)[0]
            rect_contours.append(np.array([[[x_min, y_min]],
                                           [[x_min, y_max]],
                                           [[x_max, y_max]],
                                           [[x_max, y_min]]]))

        return rect_contours

    def draw_contours(self, img, contours):
        return cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

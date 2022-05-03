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
            results.append(img[:, columns:columns + rec_width, :rec_width])

        return results

    def find_contours(self, img):
        if img is None:
            print('No image has been loaded.')
            return 0

        # Converting to grayscale is necessary for finding the contours
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(img, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        moments = []
        rect_contours = []
        for cont in contours[1::]:
            m = cv2.moments(cont)

            # Find centroid using moments
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])

            # Find borders/corners of rectangle
            x_max, y_max = np.max(cont, axis=0)[0]
            x_min, y_min = np.min(cont, axis=0)[0]

            # Save results
            moments.append(cv2.circle(gray_img, (cx, cy), 5, (255, 255, 255), -1))
            rect_contours.append(np.array([[[x_min - 2, y_min - 2]],
                                           [[x_min - 2, y_max + 2]],
                                           [[x_max + 2, y_max + 2]],
                                           [[x_max + 2, y_min - 2]]]))

        return rect_contours, moments

    def draw_contours(self, img, contours, contourid):
        return cv2.drawContours(img, contours, contourid, (0, 255, 0), 2)

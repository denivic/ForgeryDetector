import cv2
import numpy as np


class ImageMatcher():
    def __init__(self):
        pass

    def match_image(self, image, template):
        """
            Matcher objekter i et billede givet et template.add()
            Fundet her: https://answers.opencv.org/question/165740/template-matching-multiple-objects/
        """
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # run template matching, get minimum val
        res = cv2.matchTemplate(gray_image, gray_template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # create threshold from min val, find where sqdiff is less than thresh
        min_thresh = (min_val + 1e-6) * 1.5
        match_locations = np.where(res <= min_thresh)

        # draw template match boxes
        _, w, h = template.shape[::-1]
        for (x, y) in zip(match_locations[1], match_locations[0]):
            cv2.rectangle(image, (x, y), (x + w, y + h), [0, 255, 255], 2)

        # display result
        cv2.imshow('', image)
        cv2.waitKey(0)

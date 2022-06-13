import cv2
import numpy as np
from scipy.signal import convolve2d, correlate2d
from skimage.metrics import structural_similarity as ssim


class ImageMatcher():
    def __init__(self):
        pass

    def match_image(self, image, template, method, show=None):
        """Matches an image given a template.

        Args:
            image (numpy.ndarray): The image to use as a reference.
            template (numpy.ndarray): The image to use as a template and match against the reference image.
            method (cv2.type): The type of method to use.
        """
        if show is None:
            show = False

        # If the image has 3 channels then it's a colored image
        # so we have to convert to grayscale, which has 2 channels.
        if len(image.shape) == 3:
            print('Converting image to grayscale.')
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image

        if len(template.shape) == 3:
            print('Converting image to grayscale.')
            gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        else:
            gray_template = template

        # Get image width and height
        w, h = template.shape[::-1]

        # Run template matching using the given type.
        res = cv2.matchTemplate(gray_image, gray_template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            # Create threshold based on minimum value
            thresh = (min_val + 0.001)
            match_locations = np.where(res <= thresh)
        elif method in [cv2.TM_CCORR, cv2.TM_CCORR_NORMED]:
            # Create threshold based on maximum value for correlation
            thresh = (max_val - 0.001)
            match_locations = np.where(res >= thresh)

        # draw template match boxes
        for (x, y) in zip(match_locations[1], match_locations[0]):
            cv2.rectangle(image, (x, y), (x + w, y + h), [0, 255, 0], 2)

        if show:
            cv2.imshow('Detected locations', image)
            cv2.waitKey(0)
        else:
            return image

    def mse(self, image, template):
        """Finds the mean squared difference between two images.

        Args:
            image (numpy.ndarray): The main image.
            template (numpy.ndarray): The template to match against the image.

        Returns:
            int: The MSE value. The higher this value is, the lower the similarity.
                 0 indicates a perfect match.
        """
        return np.square(np.subtract(image, template)).mean()

    def ssim(self, image_one, image_two):
        """Finds the SSIM value of two images.

        Args:
            image_one (numpy.ndarray): The reference image.
            image_two (numpy.ndarray): The image to match against.

        Returns:
            int: The SSIM value for the two images.
        """
        return ssim(image_one, image_two)

    def correlate(self, image, template):
        """Returns the correlation matrix for the given image
           and template.

        Args:
            image (numpy.ndarray): The reference image.
            template (numpy.ndarray): The template/kernel.

        Returns:
            numpy.ndarray: Correlation matrix.
        """
        image = image - image.mean()
        template = image - template.mean()

        return correlate2d(image, template, mode='full')

    def convolve(self, image, template):
        """Returns the convolution matrix for the given image
           and template.

        Args:
            image (numpy.ndarray): The reference image.
            template (numpy.ndarray): The template/kernel.

        Returns:
            numpy.ndarray: Convolution matrix.
        """
        image = image - image.mean()
        template = template - template.mean()

        return convolve2d(image, template, mode='full')

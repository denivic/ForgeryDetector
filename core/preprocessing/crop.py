import cv2
from imutils import contours

# Preprocessing constants
FILTERED_BLOTS_PATH = r'Data\Blot data\Filtered blots'
CROPPED_BLOTS_PATH = r'Data\Blot data\Cropped blots'


class ImageCropper():
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = FILTERED_BLOTS_PATH

        self.data_dir = data_dir

    def crop_image(self, image, conts, path=None):
        """Crops the contours found within an image into separate entities.

        Args:
            image (numpy.ndarray): The image to be cropped.
            conts (list[numpy.ndarray]): The contours of interest that will be cropped.
            path (str): Where to save the images.
        """
        if path is None:
            path = CROPPED_BLOTS_PATH

        # Sort contours such that crops are happening from top to bottom
        (conts, _) = contours.sort_contours(conts, method="top-bottom")

        for index, cont in enumerate(conts, start=1):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(cont)

            # Save image to path
            cv2.imwrite(fr'{path}\img_{index}.jpg', image[y:y + h, x:x + w])

    def find_contours(self, image):
        """Finds the contours of an image.

        Args:
            img (numpy.ndarray): The image to find contours for.

        Returns:
            list[numpy.ndarry]: A list of countours.
            numpy.ndarray: The hierarchy for the contours.
        """
        if image is None:
            print('No image has been loaded because it could not be found.')
            return

        # Converting to grayscale is necessary for finding the contours
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, gray_img = cv2.threshold(gray_img, 127, 255, 0)
        contours, hierarchy = cv2.findContours(gray_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        return contours, hierarchy

    def draw_contours(self, img, contours, contourid=None):
        """Draws contours given an ID.

        Args:
            img (numpy.ndarray): The image to draw contours on.
            contours (numpy.ndarray): The contours to draw.
            contourid (int): Which contour to draw. Use -1 to draw all. Defaults to none.

        Returns:
            numpy.ndarray: Returns an image object with the contours drawn.
        """
        if contourid is None:
            contourid = -1  # Flag to draw all contours

        return cv2.drawContours(img, contours, contourid, (0, 255, 0), 2)


# External
import numpy as np
import cv2
import pylab as pl

# Custom
from core.preprocessing.utils import ImageUtilities


# Normalized Cross Correlation formula
def normcorr(roi, target):
    # Normalised Cross Correlation Equation
    cor = np.sum(roi * target)
    nor = np.sqrt((np.sum(roi ** 2))) * np.sqrt(np.sum(target ** 2))

    return cor / nor


# Template matching
def template_matching(img, target):
    # initial parameter
    height, width = img.shape
    tar_height, tar_width = target.shape
    (maxy, maxx) = (0, 0)
    maxval = 0

    # Set image, target and result value matrix
    img = np.array(img, dtype="int")
    target = np.array(target, dtype="int")
    nccvalue = np.zeros((height - tar_height, width - tar_width))

    # calculate value using filter-kind operation from top-left to bottom-right
    for y in range(0, height - tar_height):
        for x in range(0, width - tar_width):
            # image roi
            roi = img[y:y + tar_height, x:x + tar_width]
            # calculate ncc value
            nccvalue[y, x] = normcorr(roi, target)
            # find the most match area
            if nccvalue[y, x] > maxval:
                maxval = nccvalue[y, x]
                (maxy, maxx) = (y, x)

    return (maxx, maxy)


if __name__ == '__main__':
    utils = ImageUtilities()
    image = utils.load_image(r'C:\Users\Dumbledorf\Dropbox\Universitet\8. Semester (2022)\Bachelorprojekt\Kode\Data\Chunks\strip1._chunk1.png')
    template = utils.load_image(r'C:\Users\Dumbledorf\Dropbox\Universitet\8. Semester (2022)\Bachelorprojekt\Kode\Data\Strips\strip1.png')

    height, width = template.shape

    # function
    top_left = template_matching(image, template)
    # draw rectangle on the result region
    cv2.rectangle(image, top_left, (top_left[0] + width, top_left[1] + height), 0, 3)

    # show result
    pl.subplot(111)
    pl.imshow(image)
    pl.title('result')
    pl.show()

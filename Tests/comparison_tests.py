import numpy as np
from scipy.signal import argrelextrema
from ForgeryDetector.core.preprocessing.utils import ImageUtilities
from ForgeryDetector.core.classifying.match import ImageMatcher

match = ImageMatcher()
utils = ImageUtilities()

# Load single chunks
image_one = utils.load(r'Test_data\Chunks\strip1_chunk1.png', 0)
image_two = utils.load(r'Test_data\Chunks\strip1_chunk2.png', 0)

# Load for correlation/convolution.
image = utils.load(r'Test_data\Strips\strip_1.png', 0)
template = utils.load(r'Test_data\Chunks\strip1_chunk3.png', 0)

# MSE
same_img = match.mse(image_one, image_one)
diff_img = match.mse(image_one, image_two)
print(f'MSE for same pic: {same_img}')
print(f'MSE for different pic: {round(diff_img, 2)}')

# SSIM
same_pic = match.ssim(image_one, image_one)
diff_pic = match.ssim(image_one, image_two)
print(f'SSIM for same pic: {same_pic}')
print(f'SSIM for different pic: {round(diff_pic, 2)}')

# Get correlation
correlation_matrix = match.correlate(image, template)
# maxima_indices = argrelextrema(correlation_matrix, np.greater)
# print(correlation_matrix[maxima_indices])
utils.show(correlation_matrix)

# Get convolution
convolution_matrix = match.convolve(image, template)
# minima_indices = argrelextrema(convolution_matrix, np.less)
# print(convolution_matrix[minima_indices])
utils.show(convolution_matrix)

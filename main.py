import core.preprocessing
import core.classifying
from skimage.metrics import structural_similarity as ssim
import cv2


def main():
    # classifier = core.classifying.ImageClassifier()
    cropper = core.preprocessing.ImageCropper()
    # extractor = core.preprocessing.ImageExtractor()
    matcher = core.preprocessing.ImageMatcher()

    # Original images
    imgx, imgx_name = cropper.load_image(r'/home/dumbledorf/Dropbox/Universitet/8. Semester (2022)/Bachelorprojekt/Kode/Preprocessing/Data/Chunks/strip1._chunk7.png')
    imgy, imgy_name = cropper.load_image(r'/home/dumbledorf/Dropbox/Universitet/8. Semester (2022)/Bachelorprojekt/Kode/Preprocessing/Data/Chunks/strip4._chunk2.png')

    images = []
    for i in range(1, 6):
        (image, img_name) = cropper.load_image(rf'/home/dumbledorf/Dropbox/Universitet/8. Semester (2022)/Bachelorprojekt/Kode/Preprocessing/Data/Strips/strip{i}.png')
        images.append((image, img_name))

    # Test 1: Crop strips into chunks
    for image, img_name in images:
        bands = len(cropper.find_contours(image))
        cropped_image = cropper.crop_rectangle(image, bands, 80)

        for index, img in enumerate(cropped_image[:-1], start=1):
            cropper.save_image(img, rf'/home/dumbledorf/Dropbox/Universitet/8. Semester (2022)/Bachelorprojekt/Kode/Preprocessing/Data/Chunks/{img_name}_chunk{index}')

    # Test 2: Find, draw, and show contours
    # contours = cropper.find_contours(image)
    # img_contours = cropper.draw_contours(image, contours)
    # cropper.show_image(image)

    # Test 3: Calculate SSIM
    ssimx = ssim(cv2.cvtColor(imgx, cv2.COLOR_BGR2GRAY), cv2.cvtColor(imgx, cv2.COLOR_BGR2GRAY))
    ssimy = ssim(cv2.cvtColor(cv2.resize(imgx, (80, 49)), cv2.COLOR_BGR2GRAY), cv2.cvtColor(imgy, cv2.COLOR_BGR2GRAY))
    print(f'SSIM for comparison of the same image ({imgx_name}): {ssimx}')
    print(f'SSIM for comparison of two different images ({imgx_name}, {imgy_name}): {ssimy}')

    # Test 4: Match a template (chunk) with a strip where the chunk appears at least twice
    template, temp_name = cropper.load_image(r'/home/dumbledorf/Dropbox/Universitet/8. Semester (2022)/Bachelorprojekt/Kode/Preprocessing/Data/Chunks/strip1._chunk2.png')
    image, img_name = cropper.load_image(r'/home/dumbledorf/Dropbox/Universitet/8. Semester (2022)/Bachelorprojekt/Kode/Preprocessing/Data/Strips/strip1forged.png')
    matcher.match_image(image, template, cv2.TM_SQDIFF_NORMED)


if __name__ == "__main__":
    main()

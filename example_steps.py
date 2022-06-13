# Custom
import cv2
from ForgeryDetector.core.classifying.match import ImageMatcher
from ForgeryDetector.core.classifying.classify import ImageClassifier
from ForgeryDetector.core.preprocessing.crop import ImageCropper
from ForgeryDetector.core.preprocessing.download import DownloadManager
from ForgeryDetector.core.preprocessing.utils import ImageUtilities

if __name__ == '__main__':
    matcher = ImageMatcher()
    classifier = ImageClassifier()
    cropper = ImageCropper()
    utils = ImageUtilities()
    download = DownloadManager(threads=8)

    ########################################################################################
    # Step 1: Download articles, extract images, and filter them using ML model (optional) #
    ########################################################################################
    '''Pubmed
       for best results of western blots look up biomaterial journals e.g.:
       (("Biomaterials Research"[Journal]) AND western blot[Body - All Words]) OR western blots[Body - All Words]
       However as of now, there is an issue with advanced searches like the one above and I have
       not been able to fix it.
    '''
    parameters = {'db': 'pmc',
                  'retmax': 200,
                  'datetype': 'pdat',
                  'mindate': '2000/01/01',
                  'maxdate': '2021/01/01',
                  'term': 'western blot[Body - All Words] OR western blots[Body - All Words]',
                  'usehistory': 'y'}

    articles, _ = download.PubMed.get_links(**parameters)        # Get links given search terms
    download.PubMed.download(articles, rm=True)                  # Download said articles

    '''Pubpeer'''
    soup = download.PubPeer.get_soup('western blot', 10)        # Get PubPeer page content
    articles = download.PubPeer.get_links(soup)                 # Get links for the content
    download.PubPeer.download(articles)                         # Download the images

    '''Filter images'''
    classifier.filter(classifier.DatabaseType.PubMed, delete=True)
    classifier.filter(classifier.DatabaseType.PubPeer, delete=False)

    ####################################################
    # Step 2: Preprocess images into chunks and strips #
    ####################################################
    image = utils.load(r"Data\Unprocessed blots\Filtered blots\10.png")

    # Find contours
    contours, _ = cropper.find_contours(image)

    # Crop image into pieces
    cropper.crop_image(image, contours, r'Data\Unprocessed blots\Cropped images')

    ############################################################################
    # Step 3: Compare chunks to strips (MSE, SSD, SSIM, normcorr, convolution) #
    ############################################################################
    image = utils.load(r'Tests\Data\Strips\strip_1.png', 0)
    template = utils.load(r'Tests\Data\Chunks\strip1_chunk3.png', 0)
    result = matcher.match_image(image, template, method=cv2.TM_CCORR_NORMED)
    utils.show(result)

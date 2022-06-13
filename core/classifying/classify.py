# System modules
import os
from shutil import copy
from multiprocessing.pool import ThreadPool

# External modules
import numpy as np
from enum import Enum
from keras.models import load_model
from keras.preprocessing import image

# Model path
WESTERN_RECOGNIZE_MODEL_PATH = r'Data\Models\western_ResNet.h5'

# The default location for PubPeer/PubMed images.
PUBMED_IMAGE_PATH = r'Data\Blot data\Pubmed'
PUBPEER_IMAGE_PATH = r'Data\Blot data\Pubpeer'

# The default location for saving the filtered blots
FILTERED_BLOT_PATH = r'Data\Blot data\Filtered blots'

# Disable annoying TensorFlow messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class ImageClassifier():
    class DatabaseType(Enum):
        PubMed = PUBMED_IMAGE_PATH
        PubPeer = PUBPEER_IMAGE_PATH

    def __init__(self, model=None, threads=None):
        if model is None:
            model = WESTERN_RECOGNIZE_MODEL_PATH

        if threads is None:
            self.threads = 8
        else:
            self.threads = threads

        print('Loading pre-trained model.')
        self.model = load_model(model)
        print('The model has been successfully loaded.')

    def filter(self, img_folder_path, filtered_path=None, delete=None):
        """Filters through images and removes the images
        that are not reminiscent of western, southern or nothern blots.
        This method acts as a wrapper for _filter so as to enable
        multiproccesing.

        Args:
            img_folder_path (str): Path of the folder to look in.
            delete (bool, optional): If true non-electrophoresis images are deleted. Defaults to None.
        """
        if delete is None:
            delete = True

        # Check type of argument given
        if img_folder_path is ImageClassifier.DatabaseType.PubPeer:
            img_folder_path = PUBPEER_IMAGE_PATH
        elif img_folder_path is ImageClassifier.DatabaseType.PubMed:
            img_folder_path = PUBMED_IMAGE_PATH

        # listdir doesn't guarantee order, so the indexes have to be
        # sorted to match the way they are sorted in the folder itself.
        image_files = [(img_folder_path, img_path) for img_path in sorted(os.listdir(img_folder_path))]

        try:
            with ThreadPool(self.threads) as tp:
                tp.starmap(self._filter, image_files)
        except Exception as e:
            print(f'Exception occurred: {e}')

    def _filter(self, img_folder_path, image_file, delete=None):
        """Filters through images and removes the images
        that are not reminiscent of western, southern or nothern blots.

        Args:
            img_folder_path (str): Path of the folder to look in.
            delete (bool, optional): If true non-electrophoresis images are deleted. Defaults to None.
        """
        if delete is None:
            delete = True

        if image_file == 'PDFs':
            return

        # Loop through images, load them and use the model to recognize
        name, ext = os.path.splitext(image_file)
        img = image.load_img(img_folder_path + '/' + image_file, target_size=(224, 224))
        x = image.img_to_array(img) / 255.0
        x = np.expand_dims(x, axis=0)
        features = self.model.predict(x)

        if features[0][0] >= 0.90:
            print(f'Found a match for \'{image_file.lower()}\' ({round(features[0][0]*100)}% sure)')
            self.move(fr'{img_folder_path}\{name}{ext}', fr'{FILTERED_BLOT_PATH}\{name}{ext}', delete)
        else:
            if delete:
                os.remove(fr'{img_folder_path}\{image_file}')

    def move(self, first, second, delete):
        """Moved the file at 'first' (path) to 'second' (path)

        Args:
            first (str): The path of the file to be moved.
            second (str): The destination path for the file.
        """
        if delete:
            if os.path.exists(second):
                os.rename(first, f'copy_{second}')
            else:
                os.replace(first, second)
            print(f'File at: {first}\nMoved to: {second}.')
        else:
            copy(first, f'{second}_copy')
            print(f'File at: {first}\nCopied to: {second}.')

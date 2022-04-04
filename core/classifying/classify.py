import matplotlib.pyplot as plt  # For plotting
import numpy as np  # For transformation
import torch  # PyTorch package
import torchvision as tv  # For loading dataset and using various utilities
# import torch.nn as nn  # For building the neural network
# import torch.nn.functional as nn_func  # For convolution functions
# import torch.optim as optimizer  # For implementing optimization algorithms such as Stochastic Gradient Descent (SGD)


class ImageClassifier():
    classes = ()

    def __init__(self, data_dir, image_size, batch_size, num_workers):
        self.data_dir = data_dir
        self.image_size = image_size
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.load_data(self.data_dir, self.image_size, self.batch_size, self.num_workers)

    def load_data(self, data_dir, image_size, batch_size, num_workers):
        # Transform functions to transform the data to tensors
        transform = tv.transforms.Compose([tv.transforms.Resize(image_size),
                                           tv.transforms.ToTensor(),
                                           tv.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        # Set the dataset directory
        trainset = tv.datasets.ImageFolder(data_dir, transform=transform)

        # load train data
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                  shuffle=True, num_workers=num_workers)

        return trainloader

    def set_classes(self, classes):
        self.classes = classes

    def get_classes(self):
        if len(self.classes) == 0:
            print('No classes have been set.')
        else:
            return self.classes


# classifier = WesternClassifier(r'Training dataset', (64, 64), 4, 0)
# classifier.set_classes('western blot', 'other')


def imshow(img):
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()  # convert to numpy objects
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


# # get random training images with iter function
# dataiter = iter(trainloader)
# images, labels = dataiter.next()

# # call function on our images
# imshow(tv.utils.make_grid(images))

# # print the class of the image
# print(' '.join('%s' % classes[labels[j]] for j in range(batch_size)))

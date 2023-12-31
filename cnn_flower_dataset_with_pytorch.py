# -*- coding: utf-8 -*-
"""CNN_Flower Dataset_with_PyTorch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FBb0gc4RWedWIzsNdlnghUuNKFjKHrHP

# 3. CNN

**Why CNNs are Commonly Used in Computer Vision？/ Why not use machine learning in image?/**

● Scalability: High dimension of visual data \
● Local connectivity \
● Parameter sharing \
● Hierarchical feature learning \
● Translation invariance

# Dataset
102 Category Flower Dataset
https://www.robots.ox.ac.uk/~vgg/data/flowers/102/

Nilsback, M-E. and Zisserman, A.
Automated flower classification over a large number of classes  
Proceedings of the Indian Conference on Computer Vision, Graphics and Image Processing (2008)
"""

import torch
import torch.nn.functional as F
import numpy as np
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets, transforms
from matplotlib import pyplot as plt

transform = transforms.Compose(
    [
        transforms.CenterCrop((500, 500)),
        transforms.Resize(224),
        transforms.ToTensor(),
     ])
train_dataset = datasets.Flowers102('data', split = 'train', download=True, transform=transform)
validation_dataset = datasets.Flowers102('data', split = 'val', download=True, transform=transform)
test_dataset = datasets.Flowers102('data', split = 'test', download=True, transform=transform)

phases = {
    'train': train_dataset,
    'valid': validation_dataset,
    'test': test_dataset
    }
loader = {
    phase: DataLoader(ds, batch_size=32, shuffle=(phase=='train'))
    for phase, ds in phases.items()
}

train_dataset[0][0].shape

def visualize(image, label):
  plt.figure()
  plt.imshow(image)
  plt.title(str(label))
  plt.xticks([])
  plt.yticks([])

train_examples = [train_dataset[i] for i in range(5)]
for image, label in train_examples:
  image = torch.permute(image, (2, 1, 0)).numpy()
  visualize(image, f'Test: {label}')

class AlexNet(nn.Module):
  def __init__(self, num_classes=1000):
    super().__init__()
    self.features = nn.Sequential(
            #TODO: Implement the backbone of the model
        )
    self.flatten = nn.Flatten(start_dim=1)
    self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes)
        )

  def forward(self, x):
    x = self.features(x)
    x = self.flatten(x)
    x = self.classifier(x)
    return x

class AlexNet(nn.Module):
  def __init__(self, num_classes=1000):
    super().__init__()
    self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2)
        )
    self.adaptive_avg_pool2d = nn.AdaptiveAvgPool2d((6, 6))
    self.flatten = nn.Flatten(start_dim=1)
    self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, num_classes)
        )

  def forward(self, x):
    x = self.features(x)
    x = self.adaptive_avg_pool2d(x)
    x = self.flatten(x)
    x = self.classifier(x)
    return x

model = AlexNet(102)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

def evaluate(model, loader, device, criterion, mode='validation'):
  model.eval()
  total_correct = 0
  total_loss = 0
  total = 0
  for i, (images, labels) in enumerate(loader[mode]):
    images = images.to(device)
    labels = labels.to(device)
    with torch.no_grad():
      outputs = model(images)
      loss = criterion(outputs, labels)
      total_loss += loss.item() * images.size(0)
      total += images.size(0)
      _, predictions = outputs.max(1)
      total_correct += (labels == predictions).sum()
  loss = total_loss / total
  accuracy = total_correct / total
  print(f'{mode} epoch {epoch}: Loss({loss:6.4f}) Accuracy ({accuracy:6.4f})')

model = model.to(device)
epochs = 200
for epoch in range(epochs):
  model.train()
  total = 0
  total_correct = 0
  total_loss = 0
  for i, (images, labels) in enumerate(loader['train']):
    images = images.to(device)
    labels = labels.to(device)
    optimizer.zero_grad()
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    total += images.size(0)
    _, predictions = outputs.max(1)
    total_correct += (predictions == labels).sum()
    total_loss += loss.item() * images.size(0)
  accuracy = total_correct / total
  loss = total_loss / total
  print(f'Train epoch {epoch}: Loss({loss:6.4f}) Accuracy ({accuracy:6.4f})')
  evaluate(model, loader, device, criterion, mode='valid')

evaluate(model, loader, device, criterion, mode='test')

from IPython.display import Image, display
image_path = '/content/drive/MyDrive/PyTorch/Tensors in PyTorch.jpg'
display(Image(filename=image_path))

"""## 1. Import The Data

- Utilize the MNIST dataset.
- Transform the data into tensors using the transforms module from PyTorch.
- Employ DataLoader to construct efficient data loaders, commonly known as iterators. This facilitates the seamless and efficient feeding of batched data to deep learning models.
- Configure the batch sizes by adjusting the batch_size parameter within the data loader. I experimented with batch sizes of 32 and 64.
"""

BATCH_SIZE = 64

## transformations
transform = transforms.Compose(
    [transforms.ToTensor()])

## download and load training dataset
trainset = torchvision.datasets.MNIST(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=BATCH_SIZE,
                                          shuffle=True, num_workers=2)

## download and load testing dataset
testset = torchvision.datasets.MNIST(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=BATCH_SIZE,
                                         shuffle=False, num_workers=2)

from IPython.display import Image, display
image_path = '/content/drive/MyDrive/PyTorch/size stride.jpg'
display(Image(filename=image_path))

"""## Purpose of shuffle:

- **Prevents Pattern Learning:** Ensures the model doesn't learn any inherent order or pattern from the training data.
- **Aids Convergence:** Random data order provides varied gradient information, potentially leading to faster convergence.
- **Mitigates Overfitting:** Seeing data in different orders every epoch helps the model generalize better.
During Evaluation:

- **Turn Off shuffle:** For validation or testing data, it's common practice to set shuffle=False as the order of data doesn't influence evaluation metrics, and consistent order simplifies result analysis.

## Convergence:
- **Optimization Stability:** As models train, loss values decrease. When the loss stops changing significantly, the optimization process is said to have "converged".
- **Parameter Stability:** Model parameters (e.g., neural network weights) adjust during training. Convergence occurs when these adjustments become minor and the parameters stabilize.
Indication: Convergence suggests the model has learned primary patterns from the data and further training might not yield significant improvements.

## 2. Exploring the Data
"""

import matplotlib.pyplot as plt
import numpy as np

## functions to show an image
def imshow(img):
    #img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

## get some random training images
images, labels = next(iter(trainloader))

## show images
imshow(torchvision.utils.make_grid(images))

# Check the dimensions of a batch
for images, labels in trainloader:
    print("Image batch dimensions:", images.shape)
    print("Image label dimensions:", labels.shape)
    break

"""## OneLayerCNN model
**Model Structure:**

- Using the classical deep learning framework pipeline, I will build 1 convolutional layer model.

- Initialization `__init__()`:
Contains layers/components of the neural network.

- Convolutional Layer (nn.Conv2d(...)): \
 - in_channels=1: Grayscale images, so only one channel. \
 - out_channels=32: Desired representation depth. \
 - kernel_size=3: Convolutional kernel size. \
 - Default parameters are available in the PyTorch documentation \
 (https://pytorch.org/docs/stable/nn.html?highlight=linear#conv2d).

- Linear (Dense) Layers:
 - d1 layer:
Output size: 128.
Input dimension: 26*26*32 (influenced by the convolutional layer).
 - d2 layer:
Input: 128 (from the previous linear layer).
Output: 10 (corresponding to the number of classes).
Activation Functions:

- Post-layer activation: ReLU.
- Prediction: Uses softmax to obtain class probabilities.







"""

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()

        # 28x28x1 => 26x26x32
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3)
        self.d1 = nn.Linear(26 * 26 * 32, 128)
        self.d2 = nn.Linear(128, 10)

    def forward(self, x):
        # 32x1x28x28 => 32x32x26x26
        x = self.conv1(x)
        x = F.relu(x)

        # flatten => 32 x (32*26*26)
        x = x.flatten(start_dim = 1)

        # 32 x (32*26*26) => 32x128
        x = self.d1(x)
        x = F.relu(x)

        # logits => 32x10
        logits = self.d2(x)
        out = F.softmax(logits, dim=1)
        return out

# Test the model with 1 batch
model = MyModel()
for images, labels in trainloader:
    print("batch size:", images.shape)
    out = model(images)
    print(out.shape)
    break

"""## Training the Model

Before training the model, I will setup a loss function, an optimizer and a function to compute accuracy of the model.
"""

learning_rate = 0.001
num_epochs = 5

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = MyModel()
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Compute accuracy
def get_accuracy(logit, target, batch_size):
    ''' Obtain accuracy for training round '''
    corrects = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
    accuracy = 100.0 * corrects/batch_size
    return accuracy.item()

"""Now it's time for training."""

# Commented out IPython magic to ensure Python compatibility.
for epoch in range(num_epochs):
    train_running_loss = 0.0
    train_acc = 0.0

    model = model.train()

    ## training step
    for i, (images, labels) in enumerate(trainloader):

        images = images.to(device)
        labels = labels.to(device)

        ## forward + backprop + loss
        logits = model(images)
        loss = criterion(logits, labels)
        optimizer.zero_grad()
        loss.backward()

        ## update model params
        optimizer.step()

        train_running_loss += loss.detach().item()
        train_acc += get_accuracy(logits, labels, BATCH_SIZE)

    model.eval()
    print('Epoch: %d | Loss: %.4f | Train Accuracy: %.2f' \
#           %(epoch, train_running_loss / i, train_acc/i))

"""### Observations:

- Loss: Dropped from 1.6367 to 1.4754.
- Accuracy: Rose from 82.67% to 98.75%.
- Convergence: Model is stabilizing as accuracy gain slows.
- Overall: Achieved nearly 99% accuracy in 5 epochs.\
The basic CNN model is performing very well on the MNIST classification task.
"""

test_acc = 0.0
for i, (images, labels) in enumerate(testloader, 0):
    images = images.to(device)
    labels = labels.to(device)
    outputs = model(images)
    test_acc += get_accuracy(outputs, labels, BATCH_SIZE)

print('Test Accuracy: %.2f'%( test_acc/i))

"""The model's test accuracy is 98.32%, showing it performs well not only on training data but also on new, unseen data.

# Multilayer NN
"""

from IPython.display import Image, display
image_path = '/content/drive/MyDrive/PyTorch/multilayer NN.jpg'
display(Image(filename=image_path))



"""# Learning Process"""

from IPython.display import Image, display
image_path = '/content/drive/MyDrive/PyTorch/learning process.jpg'
display(Image(filename=image_path))
















import matplotlib.pyplot as plt
import numpy as np
from torch import nn, optim
from torch.autograd import Variable

import torch
from torchvision import datasets, transforms

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = datasets.FashionMNIST("F_MNIST", download=True, train=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True)

testset = datasets.FashionMNIST("F_MNIST", download=True, train=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=True)


def test_network(net, trainloader):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    
    dataiter = iter(trainloader)
    images, labels = dataiter.next()
    
    # Create Variables for the inputs and targets
    inputs = Variable(images)
    targets = Variable(images)
    
    # Clear the gradients from all Variables
    optimizer.zero_grad()
    
    # Forward pass, then backward pass, then update weights
    output = net.forward(inputs)
    loss = criterion(output, targets)
    loss.backward()
    optimizer.step()
    
    return True


def imshow(image, ax=None, title=None, normalize=True):
    """Imshow for Tensor."""
    if ax is None:
        fig, ax = plt.subplots()
    image = image.numpy().transpose((1, 2, 0))
    
    if normalize:
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = std * image + mean
        image = np.clip(image, 0, 1)
    
    ax.imshow(image)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', length=0)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
    
    return ax


def view_recon(img, recon):
    """ Function for displaying an image (as a PyTorch Tensor) and its
        reconstruction also a PyTorch Tensor
    """
    
    fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    axes[0].imshow(img.numpy().squeeze())
    axes[1].imshow(recon.data.numpy().squeeze())
    for ax in axes:
        ax.axis('off')
        ax.set_adjustable('box-forced')


def view_classify(img, ps, version="MNIST"):
    ''' Function for viewing an image and it's predicted classes.
    '''
    ps = ps.data.numpy().squeeze()
    
    fig, (ax1, ax2) = plt.subplots(figsize=(6, 9), ncols=2)
    ax1.imshow(img.resize_(1, 28, 28).numpy().squeeze())
    ax1.axis('off')
    ax2.barh(np.arange(10), ps)
    ax2.set_aspect(0.1)
    ax2.set_yticks(np.arange(10))
    if version == "MNIST":
        ax2.set_yticklabels(np.arange(10))
    elif version == "Fashion":
        ax2.set_yticklabels(['T-shirt/top',
                             'Trouser',
                             'Pullover',
                             'Dress',
                             'Coat',
                             'Sandal',
                             'Shirt',
                             'Sneaker',
                             'Bag',
                             'Ankle Boot'], size='small');
    ax2.set_title('Class Probability')
    ax2.set_xlim(0, 1.1)
    
    plt.tight_layout()


import torch.nn.functional as F


class FashionMNISTModel(nn.Module):
    def __init__(self, specd=None):
        super().__init__()
        
        if specd is not None and len(specd) >= 3 and isinstance(specd, np.ndarray):
            self.input = nn.Linear(specd[0], specd[1])
            
            self.hidden = []
            for idx in range(1, specd.size - 1):
                self.hidden.append(nn.Linear(specd[idx], specd[idx + 1]))
            
            self.output = nn.Linear(specd[-2], specd[-1])
        else:
            self.input = nn.Linear(784, 500)
            
            self.hidden = [
                nn.Linear(500, 500),
                nn.Linear(500, 500),
            ]
            
            self.output = nn.Linear(500, 10)
    
    def forward(self, x):
    
        x = F.sigmoid(self.input(x))
        
        for hidden in self.hidden:
            x = F.sigmoid(hidden(x))
        
        x = self.output(x)
        
        return x


class MNISTModel(nn.Module):
    def __init__(self, specd=None):
        super().__init__()
        
        if specd is not None and len(specd) >= 3 and isinstance(specd, np.ndarray):
            self.input = nn.Linear(specd[0], specd[1])
            
            self.hidden = []
            for idx in range(1, specd.size - 1):
                self.hidden.append(nn.Linear(specd[idx], specd[idx + 1]))
            
            self.output = nn.Linear(specd[-2], specd[-1])
        else:
            self.input = nn.Linear(784, 500)
            
            self.hidden = [
                nn.Linear(500, 500),
                nn.Linear(500, 500),
            ]
            
            self.output = nn.Linear(500, 10)
    
    def forward(self, x):
        
        x = F.sigmoid(self.input(x))
        
        for hidden in self.hidden:
            x = F.sigmoid(hidden(x))
        
        x = self.output(x)
        
        return x


def train_net(n_epochs=20, optimizer=optim.SGD, criterion=nn.CrossEntropyLoss):
    net = FashionMNISTModel()
    optimizer = optimizer(net.parameters(), lr=0.001)
    
    net.train()
    
    for epoch in range(n_epochs):  # loop over the dataset multiple times
        # loss_per_10_batch = []
        # loss_per_epoch = []
        running_loss = 0.0
        # train on batches of data, assumes you already have train_loader
        for batch_i, data in enumerate(trainloader):
            # get the input images and their corresponding labels
            images, labels = data
            
            # convert variables to floats for regression loss
            labels = labels.type(torch.FloatTensor)
            images = images.type(torch.FloatTensor)
            
            # forward pass to get outputs
            output = net(images)
            
            # calculate the loss between predicted and target keypoints
            loss = criterion(output, labels)
            
            # zero the parameter (weight) gradients
            optimizer.zero_grad()
            
            # backward pass to calculate the weight gradients
            loss.backward()
            
            # update the weights
            optimizer.step()
            
            # print loss statistics
            # erery_loss = loss.item()
            running_loss += loss.item()
            # loss_per_epoch.append(erery_loss)
            
            if batch_i % 10 == 9:  # print every 10 batches
                print('Epoch: {}, Batch: {}, Avg. Loss: {}'.format(epoch + 1, batch_i + 1, running_loss / 10))
                # running_loss = 0.0
                
                # loss_per_10_batch.append(running_loss / 10)
                # last_loss=running_loss
                running_loss = 0.0

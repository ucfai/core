import torch
from torch import nn
from torch import optim
import torch.nn.init as I
# ^ source code: https://pytorch.org/docs/stable/_modules/torch/nn/init.html
import torch.nn.functional as F
# ^ source code: https://pytorch.org/docs/stable/_modules/torch/nn/functional.html

from torchvision import datasets, transforms

import math
import tqdm

import utils

device = "cuda:0" if torch.cuda.is_available() else "cpu:0"
torch.device(device)

from IPython.display import display, Markdown


class MnistModel(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.x_ = nn.Linear(784, 512)
        self.h1 = nn.Linear(512, 256)
        self.h2 = nn.Linear(256, 128)
        self.o_ = nn.Linear(128, 10)
        
        self.apply(MnistModel.__init_weights)
        
        self.loader_train = None
        self.loader_test = None
        
        self.optimizer = None
        self.criterion = None
        
        self.total_loss = []
        self.total_accy = []
    
    def forward(self, x):
        
        x = torch.sigmoid(self.x_(x))
        
        x = torch.sigmoid(self.h1(x))
        
        x = torch.sigmoid(self.h2(x))
        
        x = F.log_softmax(self.o_(x), dim=1)
        
        return x
    
    def validate(self):
        test_loss = 0
        accuracy  = 0
        
        for images, labels in self.loader_test:
            
            images.resize_(images.shape[0], 784)
            
            output = self.forward(images)
            test_loss = self.criterion(output, labels).item()
            
            preds = torch.exp(output)
            equality = (labels.data == preds.max(dim=1)[1])
            accuracy += equality.type(torch.FloatTensor).mean()
        
        return test_loss, accuracy
    
    @staticmethod
    def __init_weights(m):
        if type(m) == nn.Linear:
            I.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)
    
    def fit(self, lr=0.001, n_epochs=10):
        self.apply(MnistModel.__init_weights)
        
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.criterion = nn.NLLLoss()

        self.total_loss = []
        self.total_accy = []
        
        for epoch in tqdm.tnrange(n_epochs):
            torch.device(device)
            self.train()
            acc_epoch_loss = 0
            
            steps = 0
            for images, labels in self.loader_train:
                steps += 1
                
                images.resize_(images.size()[0], 784)
                
                self.optimizer.zero_grad()

                output = self.forward(images)
                loss = self.criterion(output, labels)
                loss.backward()
                self.optimizer.step()

                acc_epoch_loss += loss.item()

            self.eval()
            with torch.no_grad():
                _, accuracy = self.validate()
                
            self.total_loss.append(acc_epoch_loss / steps)
            self.total_accy.append(accuracy / len(self.loader_test))
                
            print(f"Epoch: {(epoch + 1):2d}, Average Loss: "
                  f"{self.total_loss[-1]:.3f}, Accuracy: "
                  f"{self.total_accy[-1]:.3f}")
            
    def plot(self):
        utils.plot_loss_acc(self.total_loss, self.total_accy)
    
    def test(self):
        self.eval()
        
        images, labels = next(iter(self.loader_test))
        image = images[0].view(1, 784)

        with torch.no_grad():
            output = self.forward(image)

        preds = torch.exp(output)

        utils.view_classify(image.view(1, 28, 28), preds, version="MNIST")
    
    def prepare(self, batch_size=256, shuffle=True):
        
        transform = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        
        data_train = datasets.MNIST("data/MNIST", train=True,
                                    transform=transform, download=True)
        self.loader_train = torch.utils.data.DataLoader(data_train,
                                                        batch_size=batch_size,
                                                        shuffle=shuffle)
        
        data_test = datasets.MNIST("data/MNIST", train=False,
                                   transform=transform, download=True)
        self.loader_test = torch.utils.data.DataLoader(data_test,
                                                       batch_size=batch_size,
                                                       shuffle=shuffle)

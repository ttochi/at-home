import sys
import os
import argparse
from datetime import datetime

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


def loadDataBase(path=os.path.join('.', 'mnist_data')):
    trans = transforms.ToTensor()
    train_db = datasets.MNIST(path,
                              train=True,
                              download=True,
                              transform=trans)
    test_db = datasets.MNIST(path,
                             train=False,
                             download=True,
                             transform=trans)
    return train_db, test_db


def train(net, device, train_loader, optimizer):
    net.train()  # set the network in training mode

    train_loss = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)  # convert data type
        optimizer.zero_grad()  # clears gradients
        output = net(data)  # forwards layers in the network
        loss = torch.nn.functional.nll_loss(output, target)  # compute loss
        train_loss += loss.item()
        loss.backward()  # compute gradient
        optimizer.step()  # gradient back-propagation

    train_loss /= len(train_loader)
    return train_loss


def test(net, device, test_loader):
    net.eval()  # sets the network in test mode
    test_loss, true_positives = 0, 0

    with torch.no_grad():  # do not compute backward (gradients)
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = net(data)
            test_loss += torch.nn.functional.nll_loss(
                output, target, reduction='sum').item()
            pred = output.argmax(dim=1, keepdim=True)
            true_positives += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    accuracy = 100. * true_positives / len(test_loader.dataset)
    return test_loss, accuracy


class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 20, 5, stride=1, padding=0)
        self.conv2 = torch.nn.Conv2d(20, 50, 5, stride=1, padding=0)
        self.conv3 = torch.nn.Conv2d(50, 500, 4, stride=1, padding=0)
        self.fc1 = torch.nn.Conv2d(500, 10, 1, stride=1, padding=0)

    def forward(self, img):
        x = self.conv1(img)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.max_pool2d(x, 2, 2)

        x = self.conv2(x)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.max_pool2d(x, 2, 2)

        x = self.conv3(x)
        x = torch.nn.functional.relu(x)

        x = self.fc1(x)

        return torch.nn.functional.log_softmax(x.squeeze(), dim=1)


def main():
    # Set arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, default=64,
                        help='input batch size for training (default: 64)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    args = parser.parse_args()

    batch = args.batch
    epochs = args.epochs
    lr = args.lr

    # Set experiment environments
    torch.manual_seed(3)  # random seed for reproducability
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load MNIST database
    print('# TTOCHI Load dataset')
    train_db, test_db = loadDataBase()
    train_loader = torch.utils.data.DataLoader(train_db,
                                               batch_size=batch,
                                               shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_db,
                                              batch_size=batch,
                                              shuffle=True)

    # Initialize the network architecture and training optimizer
    print('# TTOCHI Init network')
    net = SimpleNN().to(device)
    optimizer = optim.SGD(net.parameters(), lr=lr)

    # Start training and validation
    print('# TTOCHI Start training')
    for epoch in range(1, epochs + 1):
        train_loss = train(net, device, train_loader, optimizer)  # train
        test_loss, accuracy = test(net, device, test_loader)  # validate
        print(' =TTOCHI= Epoch %02d ' % (epoch))
        print('  Train/Test Loss: %.6f /  %.6f' % (train_loss, test_loss))
        print('  Test Accuracy: %.2f' % (accuracy))

    # Save trained weights and the model
    torch.save(net.state_dict(), "mnist_cnn.pt")


if __name__ == "__main__":
    main()

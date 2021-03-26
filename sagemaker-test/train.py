from torchvision.datasets import CIFAR10
import numpy as np
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch
from network import Model

import os

# Data set setting

max_val_acc = 0
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.247, 0.243, 0.261))])
transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.247, 0.243, 0.261))])

model_num = int(os.environ.get('model', 1))
num_epochs = int(os.environ.get('epoch', 3))
batch_size = int(os.environ.get('batch', 128))
learning_rate = float(os.environ.get('lr', 1e-2))
weight = float(os.environ.get('weight', 4e-5))

print("\n Hyper parameter: epochs: %d, batch size: %4f, learning rate: %4f, weight decay: %4f".format(
    num_epochs, batch_size, learning_rate, weight))

trainset = CIFAR10("/home/user", transform=transform_train,
                   download=True, train=True)
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=batch_size, shuffle=True, num_workers=2)
testset = CIFAR10("/home/user", transform=transform_test,
                  download=True, train=False)
testloader = torch.utils.data.DataLoader(
    testset, batch_size=64, shuffle=False, num_workers=2)

model = Model()
model.cuda()
criterion = nn.CrossEntropyLoss()

i = 0
correct, total = 0, 0
train_loss, counter = 0, 0

for epoch in range(num_epochs):
    optimizer = optim.SGD(model.parameters(), lr=learning_rate,
                          weight_decay=weight, momentum=0.9)

    # iteration over all train data
    for data in trainloader:
        # shift to train mode
        model.train()

        # get the inputs
        inputs, labels = data
        inputs = inputs.cuda()
        labels = labels.cuda()

        # forward + backward + optimize
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # count acc,loss on trainset
        _, predicted = torch.max(outputs.data, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        train_loss += loss.item()
        counter += 1

        acc = correct / total
        train_loss /= counter

        if i % 100 == 0:
            print('iteration: %d, epoch: %d,  loss: %.4f, acc: %.4f'
                  % (i, epoch, train_loss, acc))
        i += 1

    torch.save(model.state_dict(), 'model.pth')

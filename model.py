from scraper import get_data

import numpy as np
import torch
import torch.utils.data as data_utils
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable

data = get_data()
batch_size = 1

# extract features
features = np.zeros(shape=(len(data),2))
for j in range(len(data)):
	features[j][0] = data[j][2]
	features[j][1] = data[j][3]

# extract targets
targets = np.zeros(shape=(len(data)))
for j in range(len(data)):
	targets[j] = data[j][1]

# split into test and train
split = int(.7 * len(data))

train_features = features[:split]
train_targets = targets[:split]

test_features = features[split:]
test_targets = targets[split:]

print(test_targets)

# make tensors
train = data_utils.TensorDataset(torch.from_numpy(train_features), torch.from_numpy(train_targets))
test = data_utils.TensorDataset(torch.from_numpy(test_features), torch.from_numpy(test_targets))

# Dataset Loader (Input Pipline)
train_loader = torch.utils.data.DataLoader(dataset=train, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test, batch_size=batch_size, shuffle=False)

# hyperparameters
input_size = 2
num_classes = 100
learning_rate = 0.001
num_epochs = 50


# Model
class LogisticRegression(nn.Module):
	def __init__(self, input_size, num_classes):
		super(LogisticRegression, self).__init__()
		self.linear = nn.Linear(input_size, num_classes)
	
	def forward(self, x):
		out = self.linear(x)
		return out

model = LogisticRegression(input_size, num_classes)

# Loss and Optimizer
# Softmax is internally computed.
# Set parameters to be updated.
#criterion = nn.CrossEntropyLoss() 
criterion = nn.NLLLoss()	 
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)  

# Training the Model
for epoch in range(num_epochs):
	for i, (features, labels) in enumerate(train_loader):
		features = Variable(features).float()
		#print("features: ", features)
		labels = Variable(labels).long()
		#print("label shape", labels)		
		# Forward + Backward + Optimize
		optimizer.zero_grad()
		outputs = model(features)

		#print("output shape", outputs)
		#print("label shape", labels.shape)
		loss = criterion(outputs, labels)
		loss.backward()
		optimizer.step()
		
		if (i+1) % 100 == 0:
			print ('Epoch: [%d/%d], Step: [%d/%d], Loss: %.4f' 
				   % (epoch+1, num_epochs, i+1, len(train_dataset)//batch_size, loss.data[0]))

# Test the Model
correct = 0
total = 0
for features, labels in test_loader:
	features = Variable(features).float()
	outputs = model(features)
	print("features", features)
	print("outputs", outputs)
	_, predicted = torch.max(outputs.data, 1)
	total += labels.size(0)
	print("PREDCITES: ", predicted, " LABELS: ", labels)
	for j in range(len(labels)):
		if predicted[j] - labels[j] <= 10:
			correct += 1
	
print('Accuracy of the model on the 10000 test images: %d %%' % (100 * correct / total))

# input data
# extract features
features = np.zeros(shape=(1,2))
features[0][0] = 51.1
features[0][1] = 78378


features = Variable(torch.from_numpy(features)).float()
outputs = model(features)
print("features", features)
_, predicted = torch.max(outputs.data, 1)
print("SAN FRANCISCO PREDCITES: ", predicted, " LABELS: ", labels)



# Save the Model
torch.save(model.state_dict(), 'model.pkl')

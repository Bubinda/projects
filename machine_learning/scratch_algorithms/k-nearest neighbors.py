# The intuition behind the K-Nearest Neighbors Algorithm

# In K-Nearest Neighbors there is no learning required as the model stores the entire dataset and classifies data points based on the points that are similar to it. It makes predictions based on the training data only.



# Step 1. Figure out an appropriate distance metric to calculate the distance between the data points.

# Step 2. Store the distance in an array and sort it according to the ascending order of their distances (preserving the index i.e. can use NumPy argsort method).

# Step 3. Select the first K elements in the sorted list.

# Step 4. Perform the majority Voting and the class with the maximum number of occurrences will be assigned as the new class for the data point to be classified.


import numpy as np
from scipy.stats import mode

#distance calculation
def eucledian(a,b):
    return np.sqrt(np.sum((a-b)**2))


#calculate the KNN
def predict(x_train, y, x_input, k):
    op_labels = []

    for i in x_input:

        # get the list of distances for the train data
        distances_of_points = np.array([eucledian(np.array(x_train[j,:]), i) for j in range(len(x_train))])

        # for j in range(len(x_train)):
        #     distances = eucledian(np.array(x_train[j,:]), i)
        #     distances_of_points.append(distances)

        # sort the array first
        # get the first k datapoints of the distances
        distance = np.argsort(distances_of_points)[:k]

        labels = y[distance]

        lab = mode(labels, keepdims=True)
        lab = lab.mode[0]
        op_labels.append(lab)

    return op_labels







#Importing the required modules
#Importing required modules
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from numpy.random import randint
import seaborn as sns 
import matplotlib.pyplot as plt
 
#Loading the Data
iris= load_iris()
 
# Store features matrix in X
X_data = iris.data
#Store target vector in 
y_data = iris.target
 
 
#Creating the training Data
train_idx = randint(0,150,100)
X_train = X_data[train_idx]
y_train = y_data[train_idx]
#print(len(X_train))
#print(len(y_train))

#plt.scatter(X_train,y_train)
#plt.show()

# sns.set_style('whitegrid')
# sns.FacetGrid(iris, hue ="species",
#               height = 6).map(plt.scatter,
#                               'sepal_length',
#                               'petal_length').add_legend()
 
#Creating the testing Data
test_idx = randint(0,150,50) #taking 50 random samples
X_test = X_data[test_idx]
y_test = y_data[test_idx]
 
#Applying our function 
y_pred = predict(X_train,y_train,X_test , 7)
 
#Checking the accuracy
print(accuracy_score(y_test, y_pred))
# It is used to predict the value of a variable based on the value of another variable. The variable we want to predict is called the dependent variable.

# The variable we are using to predict the dependent variable’s value is called the independent variable. 

# The simplest form of the regression equation with one dependent and one independent variable.

# This equation might look like y = m * x + b where: 
# y is the predicted value for the given values -> dependent variable
# x is the independent varibale
# m is the regression coefficient
# b is the bias or a constant 

# for this aglorithm whe need a few steps:


import numpy as np

# 1. loss function
def loss_function(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# 2. gradient descent
def gradient_descent(X, y, learning_rate, num_iterations):
    num_samples, num_features = X.shape
    weights = np.zeros(num_features)
    for _ in range(num_iterations):
        y_pred = np.dot(X, weights)
        gradient = np.dot(X.T, (y_pred - y)) / num_samples
        weights -= learning_rate * gradient
        
    return weights

# 3. linear regression model
class LinearRegression:
    def __init__(self, learning_rate=0.01, num_iterations=1000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
    
    def fit(self, X, y):
        X = np.insert(X, 0, 1, axis=1)  # Add bias term
        self.weights = gradient_descent(X, y, self.learning_rate, self.num_iterations)
    
    def predict(self, X):
        X = np.insert(X, 0, 1, axis=1)  # Add bias term
        y_pred = np.dot(X, self.weights)
        return y_pred

# 4. usage example
X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])
y_train = np.array([0, 0, 1, 1, 1])

model = LinearRegression()
model.fit(X_train, y_train)

X_test = np.array([[6, 7], [7, 8], [8, 9]])
y_pred = model.predict(X_test)

print(y_pred)



# alternate implementation:

import numpy as np
import matplotlib.pyplot as plt
 
#Defining the class
class LinearRegression:
    def __init__(self, x , y):
        self.data = x
        self.label = y
        self.m = 0
        self.b = 0
        self.n = len(x)
         
    def fit(self , epochs , lr):
         
        #Implementing Gradient Descent
        for i in range(epochs):
            y_pred = self.m * self.data + self.b
             
            #Calculating derivatives w.r.t Parameters
            D_m = (-2/self.n)*sum(self.data * (self.label - y_pred))
            D_b = (-1/self.n)*sum(self.label-y_pred)
             
            #Updating Parameters
            self.m = self.m - lr * D_m
            self.b = self.b - lr * D_b # fixed a varibale error
             
    def predict(self , inp):
        y_pred = self.m * inp + self.b 
        return y_pred



# Generate larger dataset
X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11]])
y_train = np.array([0, 0, 1, 1, 1, 2, 2, 3, 3, 4])

# Create an instance of LinearRegression
model = LinearRegression(X_train[:, 0], y_train)

# Fit the model
model.fit(epochs=1000, lr=0.01)

# Generate test data
X_test = np.linspace(0, 12, 100)
y_pred = model.predict(X_test)

# Generate a larger test set
X_test_large = np.linspace(0, 15, 200)
y_pred_large = model.predict(X_test_large)

# Plot the training data and the predicted line
plt.scatter(X_train[:, 0], y_train, color='blue', label='Training Data')
plt.plot(X_test, y_pred, color='red', label='Linear Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression')

# Plot the larger test set and the predicted line
plt.scatter(X_test_large, y_pred_large, color='green', label='Test Data')
plt.legend()
plt.show()


# some other test data

#importing Matplotlib for plotting
import matplotlib.pyplot as plt
import pandas as pd
 
#Loding the data
df = pd.read_csv('data_LinearRegression.csv')
 
#Preparing the data
x = np.array(df.iloc[:,0])
y = np.array(df.iloc[:,1])
 
#Creating the class object
regressor = LinearRegression(x,y)
 
#Training the model with .fit method
regressor.fit(1000 , 0.0001) # epochs-1000 , learning_rate - 0.0001
 
#Prediciting the values
y_pred = regressor.predict(x)
 
#Plotting the results
plt.figure(figsize = (10,6))
plt.scatter(x,y , color = 'green')
plt.plot(x , y_pred , color = 'k' , lw = 3)
plt.xlabel('x' , size = 20)
plt.ylabel('y', size = 20)
plt.show()